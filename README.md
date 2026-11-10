# AI-Powered Loan Approval Prediction System

## Project Overview

The **AI-Powered Loan Approval Prediction System** is an end-to-end machine learning application developed to evaluate loan applicant information and predict the risk of loan default.

Traditional loan assessment involves examining several factors, including an applicant's income, employment history, loan amount, interest rate, home ownership, and credit history. An automated prediction system can help analyze these factors consistently and provide an initial risk assessment.

This project uses machine learning classification algorithms to identify patterns in historical loan data and estimate whether an applicant is likely to default on a loan.

The system uses a **Random Forest Classifier** as its final prediction model. It provides a YES/NO loan eligibility recommendation along with an estimated loan default probability.

The machine learning model is integrated with a **FastAPI backend** and a **Streamlit frontend**, allowing users to enter applicant details and receive predictions through a web interface.

**MLflow** is used for experiment tracking and model comparison, while **Docker and Docker Compose** are used to containerize and run the application.

The project demonstrates the complete machine learning development lifecycle, from data preparation to application integration and containerization.

---

## Problem Statement

Loan default is a significant risk in the financial sector. Financial institutions must evaluate applicant information carefully before making lending decisions.

Manual evaluation of applications can be time-consuming, particularly when dealing with large numbers of applicants and multiple financial attributes.

The goal of this project is to build a machine learning-based system that analyzes applicant details and estimates the likelihood of loan default.

The system is intended to support preliminary risk assessment. Its predictions are not substitutes for actual lending decisions.

---

## Project Objectives

- Analyze loan applicant data to identify factors associated with loan default.
- Clean and preprocess the dataset to improve data quality.
- Perform Exploratory Data Analysis (EDA) to understand feature distributions and relationships.
- Create additional features using financial and credit information.
- Apply feature selection to identify relevant predictors.
- Train and evaluate multiple machine learning classification algorithms.
- Handle class imbalance using SMOTE.
- Track machine learning experiments using MLflow.
- Select a suitable model based on evaluation metrics.
- Develop a FastAPI backend for real-time predictions.
- Build an interactive Streamlit application.
- Containerize the backend and frontend using Docker.
- Publish the Docker images to Docker Hub.

---

## Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Data Analysis | Pandas, NumPy |
| Data Visualization | Matplotlib, Seaborn |
| Machine Learning | Scikit-learn |
| Class Imbalance Handling | Imbalanced-learn, SMOTE |
| Model Serialization | Joblib |
| Experiment Tracking | MLflow |
| Backend Development | FastAPI |
| Data Validation | Pydantic |
| Frontend Development | Streamlit |
| API Communication | Requests |
| Containerization | Docker |
| Container Management | Docker Compose |
| Development Environment | VS Code, Jupyter Notebook |
| Version Control | Git, GitHub |
| Container Registry | Docker Hub |

---

## Dataset Description

The project uses a loan applicant dataset containing personal, employment, financial, and credit-related information.

### Input Features

| Feature | Description |
|---|---|
| `person_age` | Age of the loan applicant |
| `person_income` | Annual income of the applicant |
| `person_home_ownership` | Applicant's home ownership status |
| `person_emp_length` | Employment experience in years |
| `loan_intent` | Purpose of the loan |
| `loan_grade` | Assigned loan grade |
| `loan_amnt` | Requested loan amount |
| `loan_int_rate` | Loan interest rate |
| `loan_percent_income` | Loan amount as a proportion of annual income |
| `cb_person_default_on_file` | Whether the applicant has a recorded previous default |
| `cb_person_cred_hist_length` | Length of the applicant's credit history |

### Target Variable

**`loan_status`**

The target variable represents the loan default outcome:

- **0 — No Default:** Applicant belongs to the non-default class.
- **1 — Default:** Applicant belongs to the default class.

The model learns patterns from these outcomes to estimate default risk for new applicant records.

---

## Project Workflow

The project follows a structured machine learning workflow:

**Data Collection → Data Cleaning → EDA → Feature Engineering → Feature Selection → Model Training → Model Evaluation → MLflow Tracking → FastAPI → Streamlit → Docker → Docker Hub**

### Phase 1 — Data Collection and Cleaning

The initial dataset is loaded using Pandas.

The data cleaning process includes:

- Inspecting dataset shape, column names, and data types.
- Identifying missing values.
- Handling missing numerical values using suitable imputation techniques.
- Checking duplicate records.
- Reviewing numerical and categorical feature distributions.
- Preparing a cleaned dataset for further analysis.

The cleaned dataset is saved as:

`data/processed/loan_approval_cleaned.csv`

### Phase 2 — Exploratory Data Analysis (EDA)

EDA is performed to understand the dataset and identify patterns related to loan default.

The analysis includes:

- Loan status distribution.
- Applicant income distribution.
- Age and employment experience analysis.
- Loan amount and interest rate analysis.
- Home ownership analysis.
- Loan grade and loan intent comparisons.
- Relationships between numerical features and loan status.
- Identification of potential class imbalance.

Libraries used:

- Pandas
- NumPy
- Matplotlib
- Seaborn

Notebook:

`notebooks/eda.ipynb`

### Phase 3 — Feature Engineering

Feature engineering is used to create additional variables from existing applicant attributes.

The following features are generated:

**1. Loan-to-Income Ratio**

```python
df["loan_to_income_ratio"] = (
    df["loan_amnt"] / df["person_income"]
)
```

This feature measures the requested loan amount relative to the applicant's annual income.

**2. Employment-to-Age Ratio**

```python
df["employment_to_age_ratio"] = (
    df["person_emp_length"] / df["person_age"]
)
```

This feature represents employment experience relative to applicant age.

**3. Credit-History-to-Age Ratio**

```python
df["credit_history_to_age_ratio"] = (
    df["cb_person_cred_hist_length"] / df["person_age"]
)
```

This feature represents the relative length of an applicant's credit history.

These features are intended to provide additional information about applicant financial and credit characteristics.

### Phase 4 — Data Preprocessing

The preprocessing workflow prepares raw input features for machine learning.

It includes:

- Missing value imputation.
- Categorical feature encoding using OneHotEncoder.
- Numerical feature scaling using StandardScaler.
- Column-wise transformations using ColumnTransformer.

The fitted preprocessing object is saved as:

`models/preprocessor.pkl`

This ensures that the same transformations can be applied to new applicant data during prediction.

### Phase 5 — Feature Selection

Feature selection is performed using **SelectKBest** from Scikit-learn.

The project selects **15 transformed features** for model prediction.

The fitted feature selector is stored as:

`models/feature_selector.pkl`

Notebook:

`notebooks/feature_engineering_selection.ipynb`

### Phase 6 — Model Training

Five machine learning classification algorithms are trained and evaluated.

| Model | Description |
|---|---|
| Logistic Regression | Linear classification model |
| Decision Tree | Tree-based classification algorithm |
| Random Forest | Ensemble of multiple decision trees |
| Gradient Boosting | Sequential ensemble learning algorithm |
| AdaBoost | Adaptive boosting classification algorithm |

SMOTE is used in the training workflow to address class imbalance.

The trained models are saved using Joblib.

### Saved Models

```text
models/
├── logistic_regression.pkl
├── decision_tree.pkl
├── random_forest.pkl
├── gradient_boosting.pkl
├── ada_boost.pkl
├── preprocessor.pkl
└── feature_selector.pkl
```

### Final Selected Model

**Random Forest Classifier**

Random Forest is used for predictions in the deployed application.

Random Forest combines predictions from multiple decision trees to produce a classification result.

It can capture nonlinear relationships and interactions between applicant features.

---

## Model Evaluation

The classification models are evaluated using standard metrics.

### Evaluation Metrics

**Accuracy**

Measures the proportion of correctly classified observations.

**Precision**

Measures how many predicted positive cases are actually positive.

**Recall**

Measures how many actual positive cases are successfully identified.

**F1-Score**

Combines precision and recall into a single measure.

**Confusion Matrix**

Shows the distribution of correct and incorrect predictions across the two classes.

The models are compared to assess their classification performance, particularly their ability to identify loan default risk.

The final application uses the Random Forest Classifier.

Notebook:

`notebooks/model_training_evaluation.ipynb`

---

## MLflow Experiment Tracking

MLflow is used to organize and track machine learning experiments.

The project uses MLflow to record:

- Machine learning model runs.
- Evaluation metrics.
- Experiment parameters.
- Model artifacts.
- Model comparisons.

### Start the MLflow Server

From the project root, run:

```powershell
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 127.0.0.1 --port 5000
```

Open the MLflow dashboard:

http://127.0.0.1:5000

**Note:** The original local `mlflow.db` and `mlruns/` files are excluded from GitHub. The recorded experiment history is therefore not included in a fresh repository clone.

---

## FastAPI Backend

FastAPI is used to develop a REST API for loan default risk prediction.

The backend loads the saved machine learning components, processes applicant input, performs predictions, and returns a JSON response.

### Backend Components

- `backend/main.py` — FastAPI application and prediction endpoint.
- `backend/schemas.py` — Request data validation.
- `models/random_forest.pkl` — Trained classification model.
- `models/preprocessor.pkl` — Fitted preprocessing transformations.
- `models/feature_selector.pkl` — Fitted feature selector.

### API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check API status |
| GET | `/health` | Check application health |
| POST | `/predict` | Generate a loan prediction |

### Example Prediction Request

```json
{
  "person_age": 35,
  "person_income": 120000,
  "person_home_ownership": "OWN",
  "person_emp_length": 10,
  "loan_intent": "EDUCATION",
  "loan_grade": "A",
  "loan_amnt": 5000,
  "loan_int_rate": 5.5,
  "loan_percent_income": 0.042,
  "cb_person_default_on_file": "N",
  "cb_person_cred_hist_length": 10
}
```

### Example Prediction Response

```json
{
  "loan_approved": "YES",
  "default_probability": 0.04
}
```

The response above is illustrative. Actual prediction results depend on the trained model.

### Run FastAPI

```powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Open Swagger API documentation:

http://127.0.0.1:8000/docs

---

## Streamlit Frontend

Streamlit is used to develop an interactive web application called **Loan Decision System**.

The frontend allows users to enter applicant information and request a prediction from the FastAPI backend.

### Frontend Features

- Applicant information form.
- Personal and employment detail inputs.
- Loan amount and interest rate inputs.
- Credit history inputs.
- FastAPI integration.
- Loan eligibility recommendation display.
- Predicted default probability display.

### Run Streamlit

Open a separate terminal and execute:

```powershell
python -m streamlit run frontend/app.py
```

Open the application:

http://localhost:8501

The FastAPI backend must be running for the frontend to retrieve predictions.

---

## Prediction Output

The system returns two primary values.

### Loan Eligibility Recommendation

**Loan Approved: YES**

The model predicts the non-default class.

**Loan Approved: NO**

The model predicts the default class.

### Default Probability

The application also displays the model's estimated probability of loan default.

**Important:** The YES/NO result represents a machine learning-based recommendation. It does not constitute a bank approval or rejection decision.

---

## Dockerization

Docker is used to package the application and its dependencies into containers.

The project uses two containers:

**Container 1 — FastAPI Backend**

Responsible for loading the machine learning model, processing applicant data, and returning predictions.

**Container 2 — Streamlit Frontend**

Responsible for displaying the user interface, collecting applicant information, and communicating with FastAPI.

Docker Compose is used to manage both services together.

### Docker Architecture

```text
             User
               |
               v
       Streamlit Frontend
               |
               v
         FastAPI Backend
               |
               v
       Data Preprocessing
               |
               v
        Feature Selection
               |
               v
       Random Forest Model
               |
               v
      Default Risk Prediction
               |
               v
         YES / NO Result
```

### Start the Application with Docker

Make sure Docker Desktop is running.

```powershell
docker compose up -d --build
```

### Check Container Status

```powershell
docker compose ps
```

### View Docker Logs

```powershell
docker compose logs -f
```

### Stop Docker Containers

```powershell
docker compose down
```

### Application URLs

| Service | Local URL |
|---|---|
| FastAPI | http://localhost:8000/docs |
| Streamlit (Docker) | http://localhost:8502 |
| MLflow (separate local server) | http://localhost:5000 |

The Docker-based Streamlit URL assumes the frontend port mapping is `8502:8501` in `compose.yaml`.

---

## Docker Hub

The backend and frontend Docker images have been published separately on Docker Hub.

### Backend Repository

https://hub.docker.com/r/vishnu178l/loan-approval-backend

### Frontend Repository

https://hub.docker.com/r/vishnu178l/loan-approval-frontend

### Pull Backend Image

```powershell
docker pull vishnu178l/loan-approval-backend:latest
```

### Pull Frontend Image

```powershell
docker pull vishnu178l/loan-approval-frontend:latest
```

The Docker Hub images can be downloaded and used in a compatible container environment.

---

## Project Structure

```text
AI-Powered-Loan-Approval-Prediction-System/
│
├── backend/
│   ├── main.py
│   ├── schemas.py
│   └── Dockerfile
│
├── frontend/
│   ├── app.py
│   └── Dockerfile
│
├── data/
│   ├── raw/
│   │   └── loan_approval_dataset.csv
│   └── processed/
│       ├── loan_approval_cleaned.csv
│       └── loan_approval_final_features.csv
│
├── models/
│   ├── logistic_regression.pkl
│   ├── decision_tree.pkl
│   ├── random_forest.pkl
│   ├── gradient_boosting.pkl
│   ├── ada_boost.pkl
│   ├── preprocessor.pkl
│   └── feature_selector.pkl
│
├── notebooks/
│   ├── eda.ipynb
│   ├── feature_engineering_selection.ipynb
│   └── model_training_evaluation.ipynb
│
├── mlflow_tracking.py
├── requirements.txt
├── compose.yaml
├── .dockerignore
├── .gitignore
└── README.md
```

---

## Installation and Local Setup

### Step 1 — Clone the Repository

```powershell
git clone https://github.com/Vishnu198L/AI-Powered-Loan-Approval-Prediction-System.git
```

Enter the project directory:

```powershell
cd AI-Powered-Loan-Approval-Prediction-System
```

### Step 2 — Create a Virtual Environment

```powershell
python -m venv venv
```

### Step 3 — Activate the Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4 — Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 5 — Start FastAPI

```powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### Step 6 — Start Streamlit

Open a new terminal:

```powershell
python -m streamlit run frontend/app.py
```

### Step 7 — Test the Application

Open:

http://localhost:8501

Enter applicant details and submit a prediction.

---

## Limitations

- Predictions depend on the quality and representativeness of the training dataset.
- The model may not generalize equally well to all applicant populations.
- Incorrect or incomplete applicant information may reduce prediction reliability.
- Historical biases in lending-related data may influence model behavior.
- The model does not implement a complete banking loan approval process.
- Model performance may change when new financial or economic conditions arise.

---

## Future Enhancements

1. **Cloud Deployment:** Deploy the application to a cloud hosting platform.
2. **Explainable AI:** Integrate SHAP or other explanation techniques to interpret predictions.
3. **Model Monitoring:** Monitor prediction performance and identify data drift.
4. **Automated Retraining:** Update the model using new and validated datasets.
5. **Enhanced User Interface:** Add richer prediction visualizations and interactive reports.
6. **Model Fairness Evaluation:** Evaluate potential differences in performance across applicant groups.
7. **Improved Data Validation:** Add additional checks for invalid and inconsistent applicant information.

---

## Conclusion

The **AI-Powered Loan Approval Prediction System** demonstrates the development of an end-to-end machine learning application for loan default risk prediction.

The project includes data cleaning, exploratory analysis, feature engineering, feature selection, multiple classification algorithms, MLflow experiment tracking, FastAPI integration, Streamlit interface development, and Docker containerization.

The completed backend and frontend Docker images are available on Docker Hub, and the source code is maintained on GitHub.

This project demonstrates practical experience with machine learning development, REST API integration, containerization, and end-to-end application deployment preparation.