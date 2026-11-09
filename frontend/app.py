
import os
import requests
import streamlit as st


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Loan Decision System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


# =====================================================
# 2. SESSION STATE
# =====================================================

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

if "application_summary" not in st.session_state:
    st.session_state.application_summary = None


def clear_application():
    """Clear the form and its previous prediction."""
    for key in list(st.session_state.keys()):
        if key.startswith("field_"):
            del st.session_state[key]

    st.session_state.prediction_result = None
    st.session_state.application_summary = None


# =====================================================
# 3. CUSTOM STYLING
# =====================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #F4F7FB;
        color: #172D45;
    }

    .block-container {
        max-width: 1240px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Application header */

    .hero {
        background: linear-gradient(
            115deg,
            #10263F 0%,
            #183B53 55%,
            #087D80 100%
        );
        border-radius: 22px;
        padding: 34px 40px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(16, 38, 63, 0.10);
    }

    .hero-tag {
        color: #8BE4D6;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }

    .hero-title {
        font-size: clamp(28px, 4vw, 42px);
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 10px;
        line-height: 1.2;
    }

    .hero-text {
        color: #D8E9F0;
        font-size: 14px;
        line-height: 1.8;
        max-width: 700px;
    }

    /* Text and form section headings */

    .section-heading {
        color: #142D45;
        font-size: 21px;
        font-weight: 800;
        margin-bottom: 7px;
    }

    .section-description {
        color: #607389;
        font-size: 13px;
        line-height: 1.7;
        margin-bottom: 18px;
    }

    .form-heading {
        color: #17364B;
        font-size: 16px;
        font-weight: 800;
        padding-top: 8px;
        padding-bottom: 10px;
    }

    .step-number {
        color: #087F7C;
        font-weight: 800;
        padding-right: 8px;
    }

    /* Fix unreadable input labels */

    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label,
    div[data-testid="stNumberInput"] label p,
    div[data-testid="stSelectbox"] label p {
        color: #20394F !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }

    /* Number input fields */

    div[data-testid="stNumberInput"]
    div[data-baseweb="input"] {
        background: #FFFFFF !important;
        border: 1px solid #CBD7E3 !important;
        border-radius: 10px !important;
    }

    div[data-testid="stNumberInput"] input {
        background: #FFFFFF !important;
        color: #172D45 !important;
        -webkit-text-fill-color: #172D45 !important;
    }

    div[data-testid="stNumberInput"] button {
        background: #E9F0F6 !important;
        color: #172D45 !important;
    }

    /* Select boxes */

    div[data-testid="stSelectbox"]
    div[data-baseweb="select"] > div {
        background: #FFFFFF !important;
        color: #172D45 !important;
        border: 1px solid #CBD7E3 !important;
        border-radius: 10px !important;
    }

    div[data-testid="stSelectbox"]
    div[data-baseweb="select"] span {
        color: #172D45 !important;
    }

    /* Primary button */

    div.stFormSubmitButton > button[kind="primary"] {
        background: #087F7C !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        min-height: 49px;
        font-weight: 800;
        font-size: 15px;
    }

    div.stFormSubmitButton > button[kind="primary"]:hover {
        background: #056C68 !important;
        color: white !important;
    }

    /* Clear button */

    div.stButton > button {
        border-radius: 11px !important;
        font-weight: 600;
    }

    /* Highlighted loan ratio */

    .ratio-card {
        background: #ECF7F5;
        border: 1px solid #B9DDD7;
        border-radius: 12px;
        padding: 17px 20px;
        margin: 12px 0 10px 0;
    }

    .ratio-label {
        font-size: 12px;
        font-weight: 700;
        color: #426E6E;
    }

    .ratio-value {
        font-size: 24px;
        font-weight: 800;
        color: #087F7C;
        margin-top: 5px;
    }

    /* Result cards */

    .result-card {
        background: #FFFFFF;
        border: 1px solid #DCE6EF;
        border-radius: 18px;
        padding: 29px 20px;
        text-align: center;
        margin-bottom: 18px;
    }

    .result-eyebrow {
        color: #64758B;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.6px;
    }

    .result-yes {
        color: #09857C;
        font-size: 65px;
        font-weight: 800;
        margin: 12px 0 4px;
    }

    .result-no {
        color: #D05254;
        font-size: 65px;
        font-weight: 800;
        margin: 12px 0 4px;
    }

    .result-caption {
        font-size: 14px;
        color: #607389;
        line-height: 1.6;
    }

    .info-card {
        background: #FFFFFF;
        border: 1px solid #DFE7EF;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 12px;
    }

    .info-title {
        font-size: 12px;
        font-weight: 800;
        color: #61748B;
        margin-bottom: 8px;
    }

    .info-value {
        font-size: 23px;
        font-weight: 800;
        color: #17364B;
    }

    .footnote {
        color: #607389;
        font-size: 12px;
        line-height: 1.8;
    }

    @media(max-width: 700px) {
        .hero {
            padding: 25px;
        }

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# 4. HEADER
# =====================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-tag">
            AI-POWERED FINANCIAL RISK ANALYSIS
        </div>
        <div class="hero-title">
            Loan Decision System
        </div>
        <div class="hero-text">
            Assess loan applications with machine learning.
            Enter applicant details, analyze predicted
            default risk, and receive a simple YES or NO
            recommendation.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =====================================================
# 5. MAIN PAGE LAYOUT
# =====================================================

left_col, right_col = st.columns(
    [1.55, 1],
    gap="large"
)


# =====================================================
# 6. APPLICANT INPUT FORM
# =====================================================

with left_col:

    st.markdown(
        '<div class="section-heading">Applicant Details</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
            Fill in the information below.
            Fields marked with an asterisk are required.
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form("loan_form"):

        # ---------------------------------------------
        # PERSONAL INFORMATION
        # ---------------------------------------------

        st.markdown(
            """
            <div class="form-heading">
                <span class="step-number">01</span>
                Personal Information
            </div>
            """,
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2)

        with c1:

            person_age = st.number_input(
                "Applicant Age *",
                min_value=18,
                max_value=100,
                value=30,
                step=1,
                key="field_age",
                help="The applicant's age in years."
            )

            person_income = st.number_input(
                "Annual Income *",
                min_value=1.0,
                value=60000.0,
                step=1000.0,
                key="field_income",
                help=(
                    "Total yearly income. Use the same "
                    "currency units as the training dataset."
                )
            )

        with c2:

            home_ownership = st.selectbox(
                "Home Ownership *",
                ["RENT", "OWN", "MORTGAGE", "OTHER"],
                key="field_home",
                help="Choose the applicant's current housing status."
            )

            emp_length = st.number_input(
                "Employment Experience (Years) *",
                min_value=0.0,
                max_value=50.0,
                value=5.0,
                step=1.0,
                key="field_employment",
                help="Number of years the applicant has worked."
            )

        st.divider()

        # ---------------------------------------------
        # LOAN INFORMATION
        # ---------------------------------------------

        st.markdown(
            """
            <div class="form-heading">
                <span class="step-number">02</span>
                Loan Information
            </div>
            """,
            unsafe_allow_html=True
        )

        c3, c4 = st.columns(2)

        with c3:

            loan_intent = st.selectbox(
                "Loan Purpose *",
                [
                    "PERSONAL",
                    "EDUCATION",
                    "MEDICAL",
                    "VENTURE",
                    "HOMEIMPROVEMENT",
                    "DEBTCONSOLIDATION"
                ],
                format_func=lambda x: {
                    "PERSONAL": "Personal Expenses",
                    "EDUCATION": "Education",
                    "MEDICAL": "Medical Expenses",
                    "VENTURE": "Business / Venture",
                    "HOMEIMPROVEMENT": "Home Improvement",
                    "DEBTCONSOLIDATION": "Debt Consolidation"
                }[x],
                key="field_purpose"
            )

            loan_amount = st.number_input(
                "Requested Loan Amount *",
                min_value=1.0,
                value=10000.0,
                step=500.0,
                key="field_loan_amount"
            )

        with c4:

            loan_grade = st.selectbox(
                "Loan Grade *",
                ["A", "B", "C", "D", "E", "F", "G"],
                key="field_grade",
                help=(
                    "Credit risk grade assigned by the lender. "
                    "A generally indicates lower risk; "
                    "G generally indicates higher risk. "
                    "Exact meanings depend on the lender."
                )
            )

            loan_rate = st.number_input(
                "Annual Interest Rate (%) *",
                min_value=0.0,
                max_value=100.0,
                value=11.5,
                step=0.1,
                key="field_interest"
            )

        # Automatic calculation
        loan_income_ratio = loan_amount / person_income

        st.markdown(
            f"""
            <div class="ratio-card">
                <div class="ratio-label">
                    AUTOMATICALLY CALCULATED
                </div>
                <div class="ratio-value">
                    Loan-to-Income: {loan_income_ratio * 100:.2f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "This compares the requested loan amount "
            "with the applicant's annual income."
        )

        if loan_income_ratio > 1:
            st.warning(
                "The requested loan amount is greater "
                "than the applicant's annual income. "
                "Please verify the values and units."
            )

        st.divider()

        # ---------------------------------------------
        # CREDIT INFORMATION
        # ---------------------------------------------

        st.markdown(
            """
            <div class="form-heading">
                <span class="step-number">03</span>
                Credit Information
            </div>
            """,
            unsafe_allow_html=True
        )

        c5, c6 = st.columns(2)

        with c5:

            previous_default = st.selectbox(
                "Previous Loan Default *",
                ["N", "Y"],
                format_func=lambda x: (
                    "No" if x == "N" else "Yes"
                ),
                key="field_default",
                help=(
                    "Has the applicant previously "
                    "defaulted on a credit obligation?"
                )
            )

        with c6:

            credit_history = st.number_input(
                "Credit History (Years) *",
                min_value=0.0,
                max_value=100.0,
                value=5.0,
                step=1.0,
                key="field_credit_history",
                help=(
                    "Number of years of recorded "
                    "credit history."
                )
            )

        st.write("")

        submit = st.form_submit_button(
            "Check Loan Eligibility",
            type="primary",
            use_container_width=True
        )

    st.button(
        "Clear Form",
        on_click=clear_application,
        use_container_width=True
    )


# =====================================================
# 7. REQUEST PREDICTION FROM FASTAPI
# =====================================================

if submit:

    # Prevent previous result appearing after a failed request
    st.session_state.prediction_result = None
    st.session_state.application_summary = None

    input_data = {
        "person_age": int(person_age),
        "person_income": float(person_income),
        "person_home_ownership": home_ownership,
        "person_emp_length": float(emp_length),
        "loan_intent": loan_intent,
        "loan_grade": loan_grade,
        "loan_amnt": float(loan_amount),
        "loan_int_rate": float(loan_rate),
        "loan_percent_income": float(loan_income_ratio),
        "cb_person_default_on_file": previous_default,
        "cb_person_cred_hist_length": float(credit_history)
    }

    try:

        with st.spinner("Analyzing applicant information..."):

            response = requests.post(
                f"{API_URL}/predict",
                json=input_data,
                timeout=30
            )

        response.raise_for_status()

        result = response.json()

        approved = result["loan_approved"]
        probability = float(result["default_probability"])

        if approved not in ("YES", "NO"):
            raise ValueError("Invalid recommendation from backend.")

        if not 0 <= probability <= 1:
            raise ValueError("Invalid default probability.")

        st.session_state.prediction_result = {
            "approved": approved,
            "probability": probability
        }

        st.session_state.application_summary = {
            "loan_amount": loan_amount,
            "annual_income": person_income,
            "purpose": loan_intent
        }

    except requests.exceptions.ConnectionError:

        st.error(
            "FastAPI is not running or cannot be reached. "
            "Start your backend on port 8000."
        )

    except requests.exceptions.Timeout:

        st.error(
            "Prediction timed out. Please try again."
        )

    except requests.exceptions.HTTPError as error:

        st.error(
            f"FastAPI returned an error: {error}"
        )

    except (ValueError, KeyError, TypeError) as error:

        st.error(
            f"Invalid prediction response: {error}"
        )

    except requests.exceptions.RequestException as error:

        st.error(
            f"Network request failed: {error}"
        )


# =====================================================
# 8. ASSESSMENT RESULT PANEL
# =====================================================

with right_col:

    st.markdown(
        '<div class="section-heading">Assessment Result</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
            View the machine learning recommendation
            and predicted default risk.
        </div>
        """,
        unsafe_allow_html=True
    )

    result = st.session_state.prediction_result

    if result is not None:

        approved = result["approved"]
        probability = result["probability"]

        if approved == "YES":

            result_style = "result-yes"
            result_message = "Lower Predicted Default Risk"

        else:

            result_style = "result-no"
            result_message = "Higher Predicted Default Risk"

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-eyebrow">
                    LOAN RECOMMENDATION
                </div>
                <div class="{result_style}">
                    {approved}
                </div>
                <div class="result-caption">
                    {result_message}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Default probability
        st.markdown("#### Default Risk")

        risk_percentage = probability * 100

        st.metric(
            label="Predicted Default Probability",
            value=f"{risk_percentage:.2f}%"
        )

        st.progress(probability)

        st.caption(
            "This percentage represents the model's "
            "estimated chance of loan default."
        )

        st.divider()

        # Application summary
        st.markdown("#### Application Summary")

        summary = st.session_state.application_summary

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-title">
                    REQUESTED LOAN AMOUNT
                </div>
                <div class="info-value">
                    {summary["loan_amount"]:,.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            "**Annual Income:** "
            f'{summary["annual_income"]:,.2f}'
        )

        st.write(
            "**Loan Purpose:** "
            f'{summary["purpose"].replace("_", " ").title()}'
        )

        st.divider()

        st.markdown("#### Prediction Model")

        st.write("**Algorithm:** Random Forest")
        st.write("**Training Balancing Method:** SMOTE")

    else:

        st.markdown(
            """
            <div class="result-card">
                <div class="result-eyebrow">
                    YOUR LOAN RECOMMENDATION
                </div>
                <div style="
                    font-size: 48px;
                    color: #A4B1C0;
                    margin: 20px 0;
                    font-weight: 800;
                ">
                    -- 
                </div>
                <div class="result-caption">
                    Your prediction will appear after
                    submitting the applicant details.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("#### How It Works")

        st.write("**1. Enter your information**")
        st.caption(
            "Provide personal, loan and credit details."
        )

        st.write("**2. Check Loan Eligibility**")
        st.caption(
            "FastAPI processes your application "
            "using the Random Forest model."
        )

        st.write("**3. View your result**")
        st.caption(
            "Receive a YES/NO recommendation "
            "and default-risk probability."
        )

    st.divider()

    st.info(
        "This is an educational risk-assessment tool. "
        "The YES/NO output is based on predicted loan "
        "default, not an official lending decision."
    )


# =====================================================
# 9. FOOTER
# =====================================================

st.divider()

st.markdown(
    """
    <div class="footnote" style="text-align:center;">
        Loan Decision System
        <br>
        Built with Streamlit, FastAPI and Random Forest
    </div>
    """,
    unsafe_allow_html=True
)
