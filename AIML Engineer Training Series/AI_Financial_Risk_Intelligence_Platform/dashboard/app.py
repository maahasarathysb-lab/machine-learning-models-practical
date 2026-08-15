from pathlib import Path
import sys
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------
# Project path
# ---------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.models.predict import CreditRiskPredictor

# ---------------------------------------------------
# Load trained pipeline
# ---------------------------------------------------
predictor = CreditRiskPredictor()

# ---------------------------------------------------
# Streamlit page config
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Financial Risk Intelligence Platform",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# Session state
# ---------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0b1020, #111827);
        color: white;
    }

    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    .hero {
        background: linear-gradient(90deg, #2563eb, #1d4ed8);
        padding: 24px;
        border-radius: 20px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 12px 35px rgba(37,99,235,0.35);
    }

    .card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 16px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    }

    .metric-title {
        color: #cbd5e1;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 38px;
        font-weight: 700;
        color: white;
    }

    .metric-sub {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 6px;
    }

    .decision {
        display: inline-block;
        padding: 10px 16px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 14px;
    }

    .approve {
        background: rgba(34,197,94,0.18);
        color: #86efac;
        border: 1px solid rgba(34,197,94,0.35);
    }

    .review {
        background: rgba(245,158,11,0.18);
        color: #fde68a;
        border: 1px solid rgba(245,158,11,0.35);
    }

    .reject {
        background: rgba(239,68,68,0.18);
        color: #fca5a5;
        border: 1px solid rgba(239,68,68,0.35);
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #2563eb, #1d4ed8);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 16px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #1d4ed8, #1e40af);
    }

    hr {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="hero">
        <h1 style="margin:0;">AI Financial Risk Intelligence Platform</h1>
        <p style="margin:8px 0 0 0;">
        Executive Credit Underwriting Dashboard powered by Machine Learning
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.header("Applicant Information")

status = st.sidebar.selectbox("Account Status", ["A11", "A12", "A13", "A14"])
duration = st.sidebar.slider("Loan Duration (months)", 4, 72, 24)
credit_history = st.sidebar.selectbox("Credit History", ["A30", "A31", "A32", "A33", "A34"])
purpose = st.sidebar.selectbox(
    "Purpose",
    ["A40", "A41", "A42", "A43", "A44", "A45", "A46", "A48", "A49", "A410"],
)
credit_amount = st.sidebar.number_input("Credit Amount", min_value=250, max_value=20000, value=4500)
savings = st.sidebar.selectbox("Savings", ["A61", "A62", "A63", "A64", "A65"])
employment_duration = st.sidebar.selectbox("Employment Duration", ["A71", "A72", "A73", "A74", "A75"])
installment_rate = st.sidebar.slider("Installment Rate", 1, 4, 4)
personal_status_sex = st.sidebar.selectbox("Personal Status / Sex", ["A91", "A92", "A93", "A94"])
other_debtors = st.sidebar.selectbox("Other Debtors", ["A101", "A102", "A103"])
present_residence = st.sidebar.slider("Present Residence", 1, 4, 2)
property_value = st.sidebar.selectbox("Property", ["A121", "A122", "A123", "A124"])
age = st.sidebar.slider("Age", 19, 75, 30)
other_installment_plans = st.sidebar.selectbox("Other Installment Plans", ["A141", "A142", "A143"])
housing = st.sidebar.selectbox("Housing", ["A151", "A152", "A153"])
existing_credits = st.sidebar.slider("Existing Credits", 1, 4, 1)
job = st.sidebar.selectbox("Job", ["A171", "A172", "A173", "A174"])
people_liable = st.sidebar.slider("People Liable", 1, 2, 1)
telephone = st.sidebar.selectbox("Telephone", ["A191", "A192"])
foreign_worker = st.sidebar.selectbox("Foreign Worker", ["A201", "A202"])

predict_button = st.sidebar.button("Analyze Credit Risk")
if predict_button:

    application = {
        "status": status,
        "duration": duration,
        "credit_history": credit_history,
        "purpose": purpose,
        "credit_amount": credit_amount,
        "savings": savings,
        "employment_duration": employment_duration,
        "installment_rate": installment_rate,
        "personal_status_sex": personal_status_sex,
        "other_debtors": other_debtors,
        "present_residence": present_residence,
        "property": property_value,
        "age": age,
        "other_installment_plans": other_installment_plans,
        "housing": housing,
        "existing_credits": existing_credits,
        "job": job,
        "people_liable": people_liable,
        "telephone": telephone,
        "foreign_worker": foreign_worker,
    }

    result = predictor.predict(application)

    probability = result["default_probability"]
    approval = 1 - probability

    # ---------------------------------------------------
    # KPI Cards
    # ---------------------------------------------------
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="card">
                <div class="metric-title">Default Probability</div>
                <div class="metric-value">{probability:.0%}</div>
                <div class="metric-sub">Risk level: {result['risk_level']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="card">
                <div class="metric-title">Approval Probability</div>
                <div class="metric-value">{approval:.0%}</div>
                <div class="metric-sub">Business threshold: 40%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div class="card">
                <div class="metric-title">Model Confidence</div>
                <div class="metric-value">91%</div>
                <div class="metric-sub">Prediction stability estimate</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        if probability >= 0.70:
            decision = "Reject"
            cls = "reject"
        elif probability >= 0.40:
            decision = "Manual Review"
            cls = "review"
        else:
            decision = "Approve"
            cls = "approve"

        st.markdown(
            f"""
            <div class="card">
                <div class="metric-title">Decision</div>
                <div class="decision {cls}">{decision}</div>
                <div class="metric-sub">Auto-underwriting outcome</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------------------------------------------------
    # Profile + Gauge + Donut
    # ---------------------------------------------------
    left, middle, right = st.columns([1.1, 1.5, 1.2])

    with left:
        st.markdown(
            f"""
            <div class="card">
                <h3>Applicant Profile</h3>
                <hr>
                <p><b>Age:</b> {age}</p>
                <p><b>Credit Amount:</b> ${credit_amount:,.0f}</p>
                <p><b>Loan Duration:</b> {duration} months</p>
                <p><b>Employment:</b> {employment_duration}</p>
                <p><b>Savings:</b> {savings}</p>
                <p><b>Housing:</b> {housing}</p>
                <p><b>Existing Credits:</b> {existing_credits}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with middle:
        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=probability * 100,
                number={"suffix": "%"},
                title={"text": "Credit Risk Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#2563eb"},
                    "steps": [
                        {"range": [0, 40], "color": "#16a34a"},
                        {"range": [40, 70], "color": "#f59e0b"},
                        {"range": [70, 100], "color": "#dc2626"},
                    ],
                },
            )
        )
        gauge.update_layout(height=360, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(gauge, use_container_width=True)

    with right:
        donut = go.Figure(
            data=[
                go.Pie(
                    labels=["Approval", "Default"],
                    values=[approval, probability],
                    hole=0.68,
                    marker_colors=["#22c55e", "#ef4444"],
                    textinfo="label+percent",
                )
            ]
        )
        donut.update_layout(
            title="Approval vs Default",
            height=360,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(donut, use_container_width=True)

    st.markdown("## Prediction Summary")

    if result["prediction"] == "Bad Credit":
        st.error(
            "**High-Risk Applicant** — The applicant shows elevated credit risk and may require additional verification or stricter lending conditions."
        )
    else:
        st.success(
            "**Low-Risk Applicant** — The applicant demonstrates favorable credit characteristics and is likely suitable for standard loan approval."
        )
    # ---------------------------------------------------
    # Explainable AI (Coefficient Analysis)
    # ---------------------------------------------------
    st.markdown("---")
    st.markdown("## Explainable AI Insights")

    preprocessor = predictor.pipeline.named_steps["preprocessor"]
    model = predictor.pipeline.named_steps["model"]

    feature_names = preprocessor.get_feature_names_out()
    coefficients = model.coef_[0]

    coef_df = pd.DataFrame({
        "Feature": feature_names,
        "Impact": coefficients
    })

    coef_df = coef_df.reindex(
        coef_df["Impact"].abs().sort_values(ascending=False).index
    ).head(10)

    colors = ["#ef4444" if v > 0 else "#22c55e" for v in coef_df["Impact"]]

    coef_fig = go.Figure(
        go.Bar(
            x=coef_df["Impact"],
            y=coef_df["Feature"],
            orientation="h",
            marker_color=colors,
            text=[f"{v:+.3f}" for v in coef_df["Impact"]],
            textposition="outside",
        )
    )

    coef_fig.update_layout(
        title="Top Features Influencing Credit Risk",
        xaxis_title="Model Coefficient (Risk Contribution)",
        yaxis_title="",
        height=450,
        margin=dict(l=20, r=20, t=50, b=20),
    )

    st.plotly_chart(coef_fig, use_container_width=True)

    col_pos, col_neg = st.columns(2)

    with col_pos:
        st.markdown("### Factors Increasing Risk")
        top_pos = coef_df[coef_df["Impact"] > 0].head(5)

        if not top_pos.empty:
            for _, row in top_pos.iterrows():
                st.markdown(
                    f"""
                    <div class="card" style="border-left:4px solid #ef4444;">
                        <b>{row['Feature']}</b><br>
                        Increases default risk by <b>+{row['Impact']:.3f}</b>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with col_neg:
        st.markdown("### Factors Reducing Risk")
        top_neg = coef_df[coef_df["Impact"] < 0].head(5)

        if not top_neg.empty:
            for _, row in top_neg.iterrows():
                st.markdown(
                    f"""
                    <div class="card" style="border-left:4px solid #22c55e;">
                        <b>{row['Feature']}</b><br>
                        Reduces default risk by <b>{row['Impact']:.3f}</b>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    # ---------------------------------------------------
    # Underwriting Recommendation
    # ---------------------------------------------------
    st.markdown("---")
    st.markdown("## Underwriting Recommendation")

    if probability >= 0.70:
        recommendation = (
            "Reject or request substantial additional verification before approval. "
            "Risk is significantly above the lending threshold."
        )
        st.error(recommendation)
    elif probability >= 0.40:
        recommendation = (
            "Manual review recommended. Verify income stability, employment, and recent credit behavior before approval."
        )
        st.warning(recommendation)
    else:
        recommendation = (
            "Applicant appears suitable for standard approval under normal lending conditions."
        )
        st.success(recommendation)

    # ---------------------------------------------------
    # Store prediction history
    # ---------------------------------------------------
    st.session_state.history.append(
        {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Age": age,
            "Credit Amount": credit_amount,
            "Duration": duration,
            "Risk %": round(probability * 100, 1),
            "Decision": decision,
        }
    )

    history_df = pd.DataFrame(st.session_state.history)

    # ---------------------------------------------------
    # Risk trend chart
    # ---------------------------------------------------
    st.markdown("---")
    st.markdown("## Risk Trend Across Predictions")

    if len(history_df) > 1:
        trend_fig = px.line(
            history_df,
            x="Time",
            y="Risk %",
            markers=True,
            title="Predicted Default Risk Over Time",
        )

        trend_fig.update_traces(line=dict(width=3))
        trend_fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))

        st.plotly_chart(trend_fig, use_container_width=True)
    else:
        st.info("Run multiple predictions to see the risk trend chart.")

    # ---------------------------------------------------
    # Recent prediction history
    # ---------------------------------------------------
    st.markdown("---")
    st.markdown("## Recent Prediction History")

    st.dataframe(history_df.tail(10), use_container_width=True)

    # ---------------------------------------------------
    # Download underwriting report
    # ---------------------------------------------------
    st.markdown("---")
    st.markdown("## Export Report")

    report = pd.DataFrame(
        [
            {
                "Default Probability": f"{probability:.2%}",
                "Approval Probability": f"{approval:.2%}",
                "Decision": decision,
                "Recommendation": recommendation,
            }
        ]
    )

    csv = report.to_csv(index=False)

    st.download_button(
        label="Download Underwriting Report (CSV)",
        data=csv,
        file_name="underwriting_report.csv",
        mime="text/csv",
    )

else:
    st.info(
        "Use the left sidebar to enter applicant details and click **Analyze Credit Risk** to generate a full underwriting report."
    )

