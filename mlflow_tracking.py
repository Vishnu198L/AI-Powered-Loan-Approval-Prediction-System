
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
import joblib

from pathlib import Path
from mlflow.tracking import MlflowClient
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE

# =====================================================
# 1. PROJECT PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = (
    BASE_DIR / "data" / "processed"
    / "loan_approval_final_features.csv"
)

MODELS_DIR = BASE_DIR / "models"
MLFLOW_DB = BASE_DIR / "mlflow.db"

EXPERIMENT_NAME = "AI-Powered Loan Approval Prediction"

# =====================================================
# 2. CONFIGURE MLFLOW
# =====================================================

mlflow.set_tracking_uri(
    f"sqlite:///{MLFLOW_DB.as_posix()}"
)

mlflow.set_experiment(EXPERIMENT_NAME)

client = MlflowClient()

experiment = client.get_experiment_by_name(
    EXPERIMENT_NAME
)

if experiment is None:
    raise ValueError("MLflow experiment not found.")

print("MLflow Configured Successfully!")
print("Experiment:", EXPERIMENT_NAME)
print("Experiment ID:", experiment.experiment_id)

# =====================================================
# 3. LOAD PROCESSED DATASET
# =====================================================

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_PATH}"
    )

df = pd.read_csv(DATA_PATH)

required_columns = {"loan_status", "dataset_split"}

if not required_columns.issubset(df.columns):
    raise ValueError(
        "Required columns are missing."
    )

train_df = df[
    df["dataset_split"] == "train"
].copy()

test_df = df[
    df["dataset_split"] == "test"
].copy()

X_train = train_df.drop(
    columns=["loan_status", "dataset_split"]
)

y_train = train_df["loan_status"]

X_test = test_df.drop(
    columns=["loan_status", "dataset_split"]
)

y_test = test_df["loan_status"]

if X_train.empty or X_test.empty:
    raise ValueError("Training or testing data is empty.")

if (
    X_train.isnull().any().any()
    or X_test.isnull().any().any()
):
    raise ValueError("Processed data contains missing values.")

if not np.isfinite(X_train.to_numpy(dtype=float)).all():
    raise ValueError("Training data contains invalid values.")

if not np.isfinite(X_test.to_numpy(dtype=float)).all():
    raise ValueError("Testing data contains invalid values.")

print("\nDataset Loaded Successfully!")
print("Training Features:", X_train.shape)
print("Testing Features:", X_test.shape)

# =====================================================
# 4. DEFINE FIVE TRAINED MODELS
# =====================================================

model_files = {
    "Logistic Regression": "logistic_regression.pkl",
    "Decision Tree": "decision_tree.pkl",
    "Random Forest": "random_forest.pkl",
    "Gradient Boosting": "gradient_boosting.pkl",
    "AdaBoost": "ada_boost.pkl"
}

print("\nChecking Saved Model Files...")

for model_name, filename in model_files.items():

    model_path = MODELS_DIR / filename

    if not model_path.exists():
        raise FileNotFoundError(
            f"{model_name} file not found: {model_path}"
        )

    print(f"{model_name}: File Found")

# =====================================================
# 5. FIND EXISTING MLFLOW RUNS
# =====================================================

existing_runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    max_results=1000
)

print("\nExisting Runs Found:", len(existing_runs))

def find_existing_run(model_name):

    matching_runs = [
        run for run in existing_runs
        if (
            run.data.tags.get("mlflow.runName") == model_name
            and "f1_score" in run.data.metrics
            and run.info.lifecycle_stage == "active"
        )
    ]

    if not matching_runs:
        raise ValueError(
            f"No existing evaluated run found for {model_name}"
        )

    # Prefer most recent evaluated run
    matching_runs.sort(
        key=lambda run: run.info.start_time or 0,
        reverse=True
    )

    return matching_runs[0]

# =====================================================
# 6. LOG MODELS INTO EXISTING RUNS
# =====================================================

print("\nLogging Models Into Existing MLflow Runs...")

for model_name, filename in model_files.items():

    print("\n====================================")
    print("Processing:", model_name)
    print("====================================")

    # Find original run
    existing_run = find_existing_run(model_name)

    run_id = existing_run.info.run_id

    print("Existing Run ID:", run_id)

    # Model name inside MLflow
    logged_model_name = (
        model_name.lower().replace(" ", "_") + "_model"
    )

    # Check if already logged
    logged_models = mlflow.search_logged_models(
        experiment_ids=[experiment.experiment_id],
        filter_string=f"source_run_id = '{run_id}'",
        output_format="list"
    )

    already_logged = any(
        item.name == logged_model_name
        for item in logged_models
    )

    if already_logged:

        print("Model already logged in this run.")
        print("Skipping duplicate model logging.")
        continue

    # Load trusted locally trained SMOTE pipeline
    model_path = MODELS_DIR / filename
    model = joblib.load(model_path)

    # Verify SMOTE pipeline
    if not isinstance(model, ImbPipeline):
        raise TypeError(
            f"{model_name} is not an ImbPipeline."
        )

    if "smote" not in model.named_steps:
        raise ValueError(
            f"{model_name} does not contain SMOTE."
        )

    if not isinstance(model.named_steps["smote"], SMOTE):
        raise TypeError(
            f"{model_name} has an invalid SMOTE step."
        )

    if model.n_features_in_ != X_train.shape[1]:
        raise ValueError(
            f"{model_name} has an incorrect feature count."
        )

    # Reopen the EXISTING run
    with mlflow.start_run(run_id=run_id):

        # Log as a proper MLflow Model
        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            name=logged_model_name,
            input_example=X_train.head(3),
            serialization_format="cloudpickle"
        )

        mlflow.set_tag(
            "balancing_method",
            "SMOTE"
        )

        mlflow.set_tag(
            "model_logged",
            "True"
        )

    print(f"{model_name} logged successfully!")
    print("Model URI:", model_info.model_uri)

# =====================================================
# 7. DISPLAY EXISTING MODEL COMPARISON
# =====================================================

results = []

for model_name in model_files:

    run = find_existing_run(model_name)

    metrics = run.data.metrics

    results.append({
        "Model": model_name,
        "Accuracy": metrics.get("accuracy"),
        "Precision": metrics.get("precision"),
        "Recall": metrics.get("recall"),
        "F1-Score": metrics.get("f1_score"),
        "ROC-AUC": metrics.get("roc_auc")
    })

model_results = pd.DataFrame(results)

model_results = model_results.sort_values(
    by="F1-Score",
    ascending=False
).reset_index(drop=True)

print("\n====================================")
print("MODEL COMPARISON RESULTS")
print("====================================")

print(
    model_results.round(4).to_string(index=False)
)

# =====================================================
# 8. DISPLAY TOP-SCORING MODEL
# =====================================================

top_model_name = model_results.iloc[0]["Model"]

top_f1_score = model_results.iloc[0]["F1-Score"]

print("\n====================================")
print("HIGHEST F1-SCORE")
print("====================================")

print("Model:", top_model_name)
print("F1-Score:", round(top_f1_score, 4))

# =====================================================
# 9. FINAL SUMMARY
# =====================================================

print("\n====================================")
print("MLFLOW MODEL LOGGING COMPLETED!")
print("====================================")

print("Total Models:", len(model_files))
print("Balancing Method: SMOTE")
print("Experiment:", EXPERIMENT_NAME)

print("\nNo new experiment runs intentionally created.")
print("No best_model.pkl created.")
print("No model_comparison.csv created.")

print("\nRefresh the MLflow dashboard.")
