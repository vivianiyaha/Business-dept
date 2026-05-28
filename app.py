import streamlit as st
import pandas as pd

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Business Department Appraisal System",
    layout="wide"
)

# ======================================================
# CUSTOM STYLE
# ======================================================
st.markdown("""
<style>
.stApp {
    background-color: white;
}

h1, h2, h3 {
    color: #1f2937;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# TITLE
# ======================================================
st.title("📊 Monthly Business Development Appraisal")
st.markdown("Fill in the employee monthly KPI performance below.")

# ======================================================
# CSV UPLOAD
# ======================================================
st.subheader("Upload Employee KPI CSV")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

employee_data = None
selected_employee = None

if uploaded_file is not None:
    employee_data = pd.read_csv(uploaded_file)

    # Clean column names
    employee_data.columns = employee_data.columns.str.strip()

    st.success("CSV uploaded successfully!")

    # ======================================================
    # NAME DROPDOWN
    # ======================================================
    if "Name" in employee_data.columns:

        selected_employee = st.selectbox(
            "Select Employee Name",
            employee_data["Name"].unique()
        )

        selected_row = employee_data[
            employee_data["Name"] == selected_employee
        ].iloc[0]

# ======================================================
# EMPLOYEE DETAILS
# ======================================================
col1, col2, col3 = st.columns(3)

with col1:
    employee_name = st.text_input(
        "Employee Name",
        value=selected_employee if selected_employee else ""
    )

with col2:
    employee_id = st.text_input("Employee ID")

with col3:
    month = st.selectbox(
        "Appraisal Month",
        [
            "January", "February", "March",
            "April", "May", "June",
            "July", "August", "September",
            "October", "November", "December"
        ]
    )

# ======================================================
# KPI DATA
# ======================================================
kpi_data = {
    "KPI Area": [
        "Lead Generation",
        "Client Acquisition",
        "Revenue Growth",
        "Client Conversion",
        "Pipeline Management",
        "Proposal Success",
        "Client Retention",
        "Customer Relationship",
        "Business Expansion",
        "Reporting & Compliance",
        "Team Collaboration",
        "Professional Conduct"
    ],

    "KPI Measure": [
        "Number of qualified leads generated",
        "New customers acquired",
        "Sales revenue achieved (₦)",
        "Client conversion rate",
        "Value of active pipeline (₦)",
        "Proposal to deal conversion rate",
        "Existing customer retention rate",
        "Number of repeat customers",
        "New markets/accounts opened",
        "Timely submission of reports",
        "Feedback from departments",
        "Attendance, discipline & professionalism"
    ],

    "Target": [
        100,
        10,
        5000000,
        30,
        10000000,
        40,
        90,
        5,
        2,
        100,
        100,
        100
    ],

    "Weight (%)": [
        10,10,15,10,10,10,10,5,5,5,5,5
    ]
}

df = pd.DataFrame(kpi_data)

# ======================================================
# INPUT TABLE
# ======================================================
st.subheader("KPI Appraisal Scorecard")

for i in range(len(df)):

    kpi_name = df.loc[i, "KPI Area"]

    st.markdown(f"### {kpi_name}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        target = st.number_input(
            f"Target - {i}",
            value=float(df.loc[i, "Target"]),
            key=f"target_{i}"
        )

    # Get value from CSV automatically
    default_actual = 0.0

    if uploaded_file is not None:
        if kpi_name in employee_data.columns:
            default_actual = float(selected_row[kpi_name])

    with col2:
        actual = st.number_input(
            f"Actual Performance - {i}",
            min_value=0.0,
            value=default_actual,
            key=f"actual_{i}"
        )

    with col3:
        weight = df.loc[i, "Weight (%)"]
        st.info(f"Weight: {weight}%")

    with col4:

        if target > 0:
            achievement = (actual / target) * 100
        else:
            achievement = 0

        achievement = min(achievement, 100)

        weighted_score = (
            achievement * weight
        ) / 100

        st.success(f"Score: {weighted_score:.2f}")

    df.loc[i, "Actual Performance"] = actual
    df.loc[i, "Score"] = weighted_score

# ======================================================
# FINAL SCORE
# ======================================================
total_score = df["Score"].sum()

st.markdown("---")
st.subheader("Final Appraisal Score")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Score",
        f"{total_score:.2f}%"
    )

with col2:

    if total_score >= 90:
        rating = "Excellent"
    elif total_score >= 75:
        rating = "Very Good"
    elif total_score >= 60:
        rating = "Good"
    elif total_score >= 50:
        rating = "Average"
    else:
        rating = "Poor"

    st.metric(
        "Performance Rating",
        rating
    )

# ======================================================
# SUMMARY TABLE
# ======================================================
st.subheader("Appraisal Summary")

summary_df = df[
    [
        "KPI Area",
        "KPI Measure",
        "Target",
        "Weight (%)",
        "Actual Performance",
        "Score"
    ]
]

st.dataframe(
    summary_df,
    use_container_width=True
)

# ======================================================
# DOWNLOAD REPORT
# ======================================================
csv = summary_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Appraisal Report",
    data=csv,
    file_name=f"{employee_name}_{month}_appraisal.csv",
    mime="text/csv"
    )
