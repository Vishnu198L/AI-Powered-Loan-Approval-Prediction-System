
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pathlib import Path

import pandas as pd
import numpy as np
import joblib

from backend.schemas import LoanInput


# =====================================================
# 1. PROJECT PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "random_forest.pkl"

PREPROCESSOR_PATH = BASE_DIR / "models" / "preprocessor.pkl"

SELECTOR_PATH = BASE_DIR / "models" / "feature_selector.pkl"

DATA_PATH = (
    BASE_DIR / "data" / "processed"
    / "loan_approval_final_features.csv"
)


# =====================================================
# 2. MODEL VARIABLES
# =====================================================

model = None
preprocessor = None
selector = None
selected_features = None


# =====================================================
# 3. LOAD MODEL AND PREPROCESSING
# =====================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    global model, preprocessor, selector, selected_features

    # Check required files
    required_files = [
        MODEL_PATH,
        PREPROCESSOR_PATH,
        SELECTOR_PATH,
        DATA_PATH
    ]

    for file_path in required_files:

        if not file_path.exists():
            raise FileNotFoundError(
                f"Required file not found: {file_path}"
            )

    # Load trusted files saved during training
    model = joblib.load(MODEL_PATH)

    preprocessor = joblib.load(PREPROCESSOR_PATH)

    selector = joblib.load(SELECTOR_PATH)

    # Get processed feature names
    feature_names = preprocessor.get_feature_names_out()

    # Get selected 15 features
    selected_features = feature_names[
        selector.get_support()
    ].tolist()

    # Compare with saved training dataset
    training_features = pd.read_csv(
        DATA_PATH,
        nrows=0
    ).drop(
        columns=["loan_status", "dataset_split"]
    ).columns.tolist()

    if selected_features != training_features:

        raise ValueError(
            "Saved feature selection does not match "
            "the training dataset."
        )

    if model.n_features_in_ != len(selected_features):

        raise ValueError(
            "Model feature count does not match."
        )

    if hasattr(model, "feature_names_in_"):

        if list(model.feature_names_in_) != selected_features:

            raise ValueError(
                "Model feature order does not match."
            )

    print("Random Forest loaded successfully!")
    print("Preprocessor loaded successfully!")
    print("Feature selector loaded successfully!")
    print("Selected Features:", len(selected_features))

    yield


# =====================================================
# 4. CREATE FASTAPI APPLICATION
# =====================================================

app = FastAPI(
    title="AI-Powered Loan Approval Prediction System",
    description="Loan default risk prediction API",
    version="1.0.0",
    lifespan=lifespan
)


# =====================================================
# 5. FEATURE ENGINEERING
# =====================================================

def feature_engineering(df):

    df = df.copy()

    # Loan to Income Ratio
    df["loan_to_income_ratio"] = (
        df["loan_amnt"] /
        df["person_income"].replace(0, np.nan)
    )

    # Employment to Age Ratio
    df["employment_to_age_ratio"] = (
        df["person_emp_length"] /
        df["person_age"].replace(0, np.nan)
    )

    # Credit History to Age Ratio
    df["credit_history_to_age_ratio"] = (
        df["cb_person_cred_hist_length"] /
        df["person_age"].replace(0, np.nan)
    )

    # Handle infinite values
    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    return df


# =====================================================
# 6. DATA PREPROCESSING
# =====================================================

def preprocess_input(df):

    # Apply saved preprocessing pipeline
    processed_data = preprocessor.transform(df)

    processed_names = preprocessor.get_feature_names_out()

    processed_df = pd.DataFrame(
        processed_data,
        columns=processed_names,
        index=df.index
    )

    # Apply saved feature selection
    selected_data = selector.transform(processed_df)

    final_df = pd.DataFrame(
        selected_data,
        columns=selected_features,
        index=df.index
    )

    return final_df


# =====================================================
# 7. HOME ENDPOINT
# =====================================================

@app.get("/")
def home():

    return {
        "message": "Loan Prediction API is running",
        "status": "success"
    }


# =====================================================
# 8. HEALTH CHECK ENDPOINT
# =====================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model": "Random Forest"
    }


# =====================================================
# 9. LOAN PREDICTION ENDPOINT
# =====================================================

@app.post("/predict")
def predict_loan(data: LoanInput):

    try:

        # Convert applicant details to DataFrame
        input_df = pd.DataFrame(
            [data.model_dump()]
        )

        # Apply feature engineering
        engineered_df = feature_engineering(input_df)

        # Apply preprocessing and feature selection
        final_df = preprocess_input(engineered_df)

        # Predict loan default status
        prediction = int(
            model.predict(final_df)[0]
        )

        # Get default probability
        classes = list(model.classes_)

        default_class_index = classes.index(1)

        default_probability = float(
            model.predict_proba(final_df)[
                0, default_class_index
            ]
        )

        # Risk-based approval recommendation
        # 0 = No predicted default -> YES
        # 1 = Predicted default -> NO

        loan_approved = (
            "YES" if prediction == 0 else "NO"
        )

        # Return only required output
        return {
            "loan_approved": loan_approved,
            "default_probability": round(
                default_probability, 4
            )
        }

    except (ValueError, KeyError) as error:

        raise HTTPException(
            status_code=422,
            detail=str(error)
        )

    except Exception as error:

        print("Prediction Error:", error)

        raise HTTPException(
            status_code=500,
            detail="Prediction failed. Check backend terminal."
        )
