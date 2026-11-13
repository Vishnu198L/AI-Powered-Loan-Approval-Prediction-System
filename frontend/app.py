
import os
import requests
import streamlit as st

# ======================================================
# 1. PAGE CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="Loan Decision System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================================
# 2. FASTAPI CONFIGURATION
# ======================================================

API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000"
).rstrip("/")

PREDICT_URL = f"{API_URL}/predict"

# ======================================================
# 3. SESSION STATE
# ======================================================

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

if "submitted_data" not in st.session_state:
    st.session_state.submitted_data = None


# ======================================================
# 4. CUSTOM CSS
# ======================================================

st.markdown(
    """
    <style>

    /* Main application */
    .stApp {
        background: #f3f6fb;
        color: #17243b;
    }

    .block-container {
        max-width: 1120px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Hide default decoration */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Main banner */
    .hero {
        background: linear-gradient(
            120deg,
            #0c2340,
            #124a68,
            #087e85
        );
        padding: 34px 38px;
        border-radius: 20px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 12px 28px rgba(16, 45, 76, 0.12);
    }

    .hero-label {
        color: #a9edf0;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .hero-title {
        font-size: 34px;
        font-weight: 800;
        line-height: 1.2;
        margin: 0 0 12px 0;
        color: #ffffff;
    }

    .hero-subtitle {
        font-size: 15px;
        line-height: 1.7;
        max-width: 760px;
        color: #dbeaf1;
        margin: 0;
    }

    /* Section titles */
    .section-heading {
        font-size: 18px;
        font-weight: 750;
        color: #102b47;
        margin-top: 12px;
        margin-bottom: 4px;
    }

    .section-description {
        font-size: 13px;
        color: #66788c;
        margin-bottom: 15px;
    }

    .step-tag {
        display: inline-block;
        background: #d7f2f2;
        color: #087d84;
        border-radius: 7px;
        padding: 5px 10px;
        margin-right: 8px;
        font-weight: 800;
        font-size: 12px;
    }

    /* Metric / information cards */
    .info-card {
        background: #ffffff;
        border: 1px solid #dfe8f1;
        border-radius: 14px;
        padding: 18px 20px;
        margin: 12px 0;
    }

    .info-card-label {
        font-size: 12px;
        color: #697c8e;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .info-card-value {
        font-size: 25px;
        font-weight: 800;
        color: #087f87;
        margin-top: 7px;
    }

    /* Result cards */
    .result-success {
        background: #e9f9f2;
        border: 1px solid #a5e2c3;
        border-left: 6px solid #16a36d;
        border-radius: 16px;
        padding: 28px;
        margin-top: 12px;
        margin-bottom: 18px;
    }

    .result-failure {
        background: #fff0f0;
        border: 1px solid #f1b1b5;
        border-left: 6px solid #d74756;
        border-radius: 16px;
        padding: 28px;
        margin-top: 12px;
        margin-bottom: 18px;
    }

    .result-title {
        font-size: 25px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .result-description {
        font-size: 14px;
        line-height: 1.7;
        color: #405166;
    }

    /* Buttons */
    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button {
        background: linear-gradient(
            90deg,
            #0b777f,
            #0d98a2
        ) !important;
        color: white !important;
        border: none !important;
        border-radius: 11px !important;
        min-height: 48px;
        font-weight: 700;
        letter-spacing: 0.3px;
    }

    div.stButton > button[kind="primary"]:hover,
    div.stFormSubmitButton > button:hover {
        background: #09656d !important;
        color: white !important;
    }

    /* Input styling */
    div[data-baseweb="input"] {
        border-radius: 9px;
    }

    div[data-baseweb="select"] > div {
        border-radius: 9px;
    }

    /* Footer */
    .custom-footer {
        text-align: center;
        color: #8492a2;
        font-size: 12px;
        padding-top: 22px;
        line-height: 1.9;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
# 5. HEADER
# ======================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-label">
            AI-POWERED FINANCIAL INTELLIGENCE
        </div>
        <div class="hero-title">
            🏦 Loan Decision System
        </div>
        <p class="hero-subtitle">
            A smart machine learning application that evaluates
            applicant information, estimates loan default risk,
            and provides an instant eligibility recommendation.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ======================================================
# 6. BACKEND STATUS
# ======================================================

try:
    health_response = requests.get(
        f"{API_URL}/health",
        timeout=5
    )
    health_response.raise_for_status()
    backend_connected = True

except requests.exceptions.RequestException:
    backend_connected = False

if backend_connected:
    st.success("✅ Prediction service is connected and ready.")
else:
    st.error(
        "FastAPI backend is unavailable. "
        "Check the backend container and API connection."
    )

st.write("")

# ======================================================
# 7. MAIN APPLICATION FORM
# ======================================================

st.markdown(
    '<div class="section-heading">Loan Application</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Complete the following information to generate your risk assessment.'
    '</div>',
    unsafe_allow_html=True
)

with st.form("loan_application_form"):

    # --------------------------------------------------
    # SECTION 1 - PERSONAL DETAILS
    # --------------------------------------------------

    st.markdown(
        """
        <div class="section-heading">
            <span class="step-tag">01</span>
            Personal & Employment Details
        </div>
        <p class="section-description">
            Tell us about the applicant's financial background.
        </p>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        person_age = st.number_input(
            "Applicant Age *",
            min_value=18,
            max_value=100,
            value=30,
            step=1,
            help="Applicant's age in years"
        )

        person_income = st.number_input(
            "Annual Income *",
            min_value=1.0,
            value=50000.0,
            step=1000.0,
            format="%.2f",
            help="Applicant's annual income"
        )

    with col2:
        person_home_ownership = st.selectbox(
            "Home Ownership *",
            [
                "RENT",
                "OWN",
                "MORTGAGE",
                "OTHER"
            ]
        )

        person_emp_length = st.number_input(
            "Employment Experience (Years) *",
            min_value=0.0,
            max_value=80.0,
            value=5.0,
            step=1.0,
            help="Total employment experience"
        )

    st.divider()

    # --------------------------------------------------
    # SECTION 2 - LOAN INFORMATION
    # --------------------------------------------------

    st.markdown(
        """
        <div class="section-heading">
            <span class="step-tag">02</span>
            Loan Information
        </div>
        <p class="section-description">
            Enter the requested loan details.
        </p>
        """,
        unsafe_allow_html=True
    )

    col3, col4 = st.columns(2, gap="large")

    with col3:
        loan_intent = st.selectbox(
            "Purpose of Loan *",
            [
                "PERSONAL",
                "EDUCATION",
                "MEDICAL",
                "VENTURE",
                "HOMEIMPROVEMENT",
                "DEBTCONSOLIDATION"
            ]
        )

        loan_amnt = st.number_input(
            "Requested Loan Amount *",
            min_value=1.0,
            value=10000.0,
            step=1000.0,
            format="%.2f"
        )

    with col4:
        loan_grade = st.selectbox(
            "Loan Grade *",
            [
                "A",
                "B",
                "C",
                "D",
                "E",
                "F",
                "G"
            ]
        )

        loan_int_rate = st.number_input(
            "Loan Interest Rate (%) *",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=0.5
        )

    loan_percent_income = (
        loan_amnt / person_income
    )

    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-card-label">
                Loan-to-Income Ratio
            </div>
            <div class="info-card-value">
                {loan_percent_income * 100:.2f}%
            </div>
            <div style="font-size:12px;color:#718096;margin-top:5px;">
                Requested loan amount compared with annual income.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # --------------------------------------------------
    # SECTION 3 - CREDIT INFORMATION
    # --------------------------------------------------

    st.markdown(
        """
        <div class="section-heading">
            <span class="step-tag">03</span>
            Credit Information
        </div>
        <p class="section-description">
            Provide the applicant's credit background.
        </p>
        """,
        unsafe_allow_html=True
    )

    col5, col6 = st.columns(2, gap="large")

    with col5:
        previous_default = st.selectbox(
            "Previous Loan Default *",
            ["No", "Yes"]
        )

    with col6:
        cb_person_cred_hist_length = st.number_input(
            "Credit History (Years) *",
            min_value=0,
            max_value=100,
            value=5,
            step=1
        )

    cb_person_default_on_file = (
        "Y" if previous_default == "Yes" else "N"
    )

    st.write("")

    # --------------------------------------------------
    # SUBMIT BUTTON
    # --------------------------------------------------

    submitted = st.form_submit_button(
        "🔍 Check Loan Eligibility",
        use_container_width=True,
        disabled=not backend_connected
    )


# ======================================================
# 8. PREDICTION
# ======================================================

if submitted:

    input_data = {
        "person_age": int(person_age),
        "person_income": float(person_income),
        "person_home_ownership": person_home_ownership,
        "person_emp_length": float(person_emp_length),
        "loan_intent": loan_intent,
        "loan_grade": loan_grade,
        "loan_amnt": float(loan_amnt),
        "loan_int_rate": float(loan_int_rate),
        "loan_percent_income": float(loan_percent_income),
        "cb_person_default_on_file": cb_person_default_on_file,
        "cb_person_cred_hist_length": int(
            cb_person_cred_hist_length
        )
    }

    try:
        with st.spinner("Analyzing applicant information..."):

            response = requests.post(
                PREDICT_URL,
                json=input_data,
                timeout=30
            )

            response.raise_for_status()

            prediction_result = response.json()

        st.session_state.prediction_result = prediction_result
        st.session_state.submitted_data = input_data

    except requests.exceptions.ConnectionError:
        st.session_state.prediction_result = None
        st.error(
            "Unable to connect to the FastAPI server."
        )

    except requests.exceptions.Timeout:
        st.session_state.prediction_result = None
        st.error(
            "The prediction request timed out."
        )

    except requests.exceptions.HTTPError:
        st.session_state.prediction_result = None

        st.error(
            f"API Error: HTTP {response.status_code}"
        )

        st.code(response.text)

    except requests.exceptions.RequestException as error:
        st.session_state.prediction_result = None
        st.error(f"API error: {error}")

    except ValueError as error:
        st.session_state.prediction_result = None
        st.error(f"Invalid API response: {error}")


# ======================================================
# 9. PREDICTION RESULT DASHBOARD
# ======================================================

result = st.session_state.prediction_result

if result is not None:

    st.divider()

    st.markdown(
        '<div class="section-heading">'
        '📊 Loan Risk Assessment'
        '</div>',
        unsafe_allow_html=True
    )

    loan_approved = result.get(
        "loan_approved"
    )

    default_probability = result.get(
        "default_probability"
    )

    if loan_approved == "YES":

        st.markdown(
            """
            <div class="result-success">
                <div class="result-title" style="color:#137f53;">
                    ✓ Loan Approved: YES
                </div>
                <div class="result-description">
                    The machine learning model predicts the
                    non-default class for this applicant.
                    This indicates a lower predicted default risk.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif loan_approved == "NO":

        st.markdown(
            """
            <div class="result-failure">
                <div class="result-title" style="color:#c33547;">
                    ✕ Loan Approved: NO
                </div>
                <div class="result-description">
                    The machine learning model predicts
                    the default class for this applicant.
                    This indicates a higher predicted default risk.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.warning(
            "Unexpected prediction value returned by the API."
        )
        st.json(result)

    # --------------------------------------------------
    # PROBABILITY DISPLAY
    # --------------------------------------------------

    if default_probability is not None:

        probability = float(default_probability)

        st.markdown("#### Default Risk Probability")

        metric_col1, metric_col2 = st.columns(2)

        with metric_col1:
            st.metric(
                "Estimated Default Probability",
                f"{probability * 100:.2f}%"
            )

        with metric_col2:
            st.metric(
                "Estimated Non-Default Probability",
                f"{(1 - probability) * 100:.2f}%"
            )

        if 0 <= probability <= 1:

            st.progress(probability)

            st.caption(
                "The risk estimate is based on the "
                "trained Random Forest classifier."
            )

    # --------------------------------------------------
    # APPLICANT DATA SUMMARY
    # --------------------------------------------------

    with st.expander("📋 View Submitted Application"):

        st.json(
            st.session_state.submitted_data
        )

    st.info(
        "This prediction is an educational risk assessment "
        "and does not represent an official lending decision."
    )

# ======================================================
# 10. CLEAR FORM / RESULTS
# ======================================================

st.write("")

if st.button(
    "↻ Clear Prediction Result",
    use_container_width=True
):

    st.session_state.prediction_result = None
    st.session_state.submitted_data = None

    st.rerun()


# ======================================================
# 11. FOOTER
# ======================================================

st.markdown(
    """
    <div class="custom-footer">
        <strong>AI-Powered Loan Approval Prediction System</strong>
        <br>
        Built with Python · Random Forest · FastAPI · Streamlit · Docker
        <br>
        Educational machine learning project
    </div>
    """,
    unsafe_allow_html=True
)
