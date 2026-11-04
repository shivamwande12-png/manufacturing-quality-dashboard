import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Manufacturing Quality Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================================
# 2. CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #0e1117;
}

/* Main Container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Headings */
h1, h2, h3, h4 {
    color: #ffffff !important;
}

/* General Text */
p, label {
    color: #e2e8f0;
}

/* KPI Cards */
[data-testid="stMetric"] {
    background-color: #ffffff !important;
    padding: 20px !important;
    border-radius: 12px !important;
    border: 1px solid #d1d5db !important;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.2);
}

/* KPI Labels */
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #475569 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

/* KPI Values */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div,
[data-testid="stMetricValue"] p {
    color: #0f172a !important;
    font-size: 28px !important;
    font-weight: 800 !important;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border-radius: 10px;
}

/* Download Buttons */
.stDownloadButton button {
    background-color: #2563eb !important;
    color: white !important;
    border-radius: 8px;
    border: none;
    font-weight: bold;
    padding: 10px 20px;
}

.stDownloadButton button:hover {
    background-color: #1d4ed8 !important;
}

/* Divider */
hr {
    border-color: #334155;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# 3. DASHBOARD HEADER
# ==========================================================

st.title("🏭 Manufacturing Quality Dashboard")

st.markdown(
    "### Product Inspection & Machine Performance Analysis"
)

st.caption("Real-time Manufacturing Quality Monitoring System")

st.markdown("---")


# ==========================================================
# 4. MANUFACTURING PRODUCT DATA
# ==========================================================

data = {

    "Product_ID": [
        "P101", "P102", "P103", "P104", "P105",
        "P106", "P107", "P108", "P109", "P110",
        "P111", "P112", "P113", "P114", "P115"
    ],

    "Machine": [
        "M1", "M1", "M2", "M2", "M3",
        "M1", "M2", "M3", "M1", "M2",
        "M3", "M1", "M2", "M3", "M1"
    ],

    "Length": [
        52.0, 48.5, 52.0, 50.2, 49.8,
        52.2, 50.0, 48.0, 50.1, 50.8,
        52.1, 49.9, 50.3, 48.5, 50.0
    ],

    "Width": [
        20.1, 20.2, 20.0, 20.0, 20.2,
        20.1, 19.8, 20.0, 20.5, 20.2,
        19.9, 20.1, 20.0, 21.8, 19.9
    ]

}

df = pd.DataFrame(data)


# ==========================================================
# 5. ACCEPTABLE MEASUREMENT LIMITS
# ==========================================================

min_length = 49.0
max_length = 51.0

min_width = 19.0
max_width = 21.0


# ==========================================================
# 6. DATA CALCULATIONS
# ==========================================================

df["Area"] = np.round(
    df["Length"] * df["Width"], 2
)

df["Length_Error"] = np.round(
    df["Length"] - 50.0, 2
)

df["Width_Error"] = np.round(
    df["Width"] - 20.0, 2
)


# ==========================================================
# 7. PRODUCT QUALITY INSPECTION
# ==========================================================

status_list = []
reason_list = []

for i in range(len(df)):

    L = df.loc[i, "Length"]
    W = df.loc[i, "Width"]

    length_ok = min_length <= L <= max_length
    width_ok = min_width <= W <= max_width

    if length_ok and width_ok:

        status_list.append("Pass")
        reason_list.append("No Defect")

    elif not length_ok and width_ok:

        status_list.append("Fail")
        reason_list.append("Length Defect")

    elif length_ok and not width_ok:

        status_list.append("Fail")
        reason_list.append("Width Defect")

    else:

        status_list.append("Fail")
        reason_list.append("Both Defect")


df["Status"] = status_list
df["Defect_Reason"] = reason_list


# ==========================================================
# 8. OVERALL PRODUCTION SUMMARY
# ==========================================================

total = len(df)

passed = (df["Status"] == "Pass").sum()

failed = (df["Status"] == "Fail").sum()

pass_rate = (passed / total) * 100

defect_rate = (failed / total) * 100

avg_length = np.mean(df["Length"])

avg_width = np.mean(df["Width"])


# ==========================================================
# 9. MACHINE-WISE DEFECT REPORT
# ==========================================================

machine_report = pd.crosstab(
    df["Machine"],
    df["Status"]
)

# Ensure both columns exist

for col in ["Pass", "Fail"]:
    if col not in machine_report.columns:
        machine_report[col] = 0

machine_report["Total"] = (
    machine_report["Pass"] +
    machine_report["Fail"]
)

machine_report["Defect_Rate_%"] = np.round(
    (machine_report["Fail"] /
     machine_report["Total"]) * 100,
    1
)


# ==========================================================
# 10. OVERALL PRODUCTION KPI CARDS
# ==========================================================

st.subheader("📊 Overall Production Summary")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Total Products",
    total
)

c2.metric(
    "Passed Products",
    passed
)

c3.metric(
    "Failed Products",
    failed
)

c4.metric(
    "Pass Rate",
    f"{pass_rate:.2f}%"
)

c5.metric(
    "Defect Rate",
    f"{defect_rate:.2f}%"
)


st.markdown("---")


# ==========================================================
# 11. MEASUREMENT ANALYSIS
# ==========================================================

st.subheader("📐 Measurement Analysis")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Average Length",
    f"{avg_length:.2f} mm"
)

m2.metric(
    "Average Width",
    f"{avg_width:.2f} mm"
)

m3.metric(
    "Length Specification",
    "49–51 mm"
)

m4.metric(
    "Width Specification",
    "19–21 mm"
)


st.markdown("---")


# ==========================================================
# 12. PRODUCT INSPECTION TABLE
# ==========================================================

st.subheader("📋 Product Inspection Report")

st.caption(
    "Complete inspection results for all manufactured products."
)


def highlight_status(row):

    if row["Status"] == "Pass":

        return [
            "background-color: #dcfce7; color: #166534"
            for _ in row
        ]

    else:

        return [
            "background-color: #fee2e2; color: #991b1b"
            for _ in row
        ]


styled_df = df.style.apply(
    highlight_status,
    axis=1
).format({
    "Length": "{:.2f}",
    "Width": "{:.2f}",
    "Area": "{:.2f}",
    "Length_Error": "{:.2f}",
    "Width_Error": "{:.2f}"
})


st.dataframe(
    styled_df,
    use_container_width=True,
    hide_index=True,
    height=550
)


st.markdown("---")


# ==========================================================
# 13. MACHINE-WISE DEFECT REPORT
# ==========================================================

st.subheader("⚙️ Machine-wise Defect Report")

st.dataframe(
    machine_report,
    use_container_width=True
)


# ==========================================================
# 14. MACHINE PERFORMANCE SUMMARY
# ==========================================================

st.subheader("🏭 Machine Performance Analysis")

for machine in machine_report.index:

    machine_data = machine_report.loc[machine]

    st.write(
        f"**{machine}** — "
        f"Total: {int(machine_data['Total'])} | "
        f"Passed: {int(machine_data['Pass'])} | "
        f"Failed: {int(machine_data['Fail'])} | "
        f"Defect Rate: {machine_data['Defect_Rate_%']:.1f}%"
    )

    st.progress(
        float(machine_data["Pass"] / machine_data["Total"])
    )


st.markdown("---")


# ==========================================================
# 15. DATA VISUALIZATION
# ==========================================================

st.subheader("📈 Manufacturing Quality Visualization")


# ----------------------------------------------------------
# CHART 1: OVERALL PASS VS FAIL
# ----------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.markdown("#### Overall Product Quality")

    fig1, ax1 = plt.subplots(figsize=(6, 4))

    ax1.pie(
        [passed, failed],
        labels=["Passed", "Failed"],
        autopct="%1.1f%%",
        colors=["lightgreen", "salmon"],
        startangle=90,
        explode=(0.03, 0.03),
        textprops={"fontsize": 11}
    )

    ax1.set_title(
        "Overall Pass vs Fail",
        fontsize=13,
        fontweight="bold"
    )

    st.pyplot(fig1, use_container_width=True)

    plt.close(fig1)


# ----------------------------------------------------------
# CHART 2: MACHINE-WISE PASS AND FAIL
# ----------------------------------------------------------

with col2:

    st.markdown("#### Machine-wise Pass & Fail")

    machines = machine_report.index

    x = np.arange(len(machines))

    fig2, ax2 = plt.subplots(figsize=(6, 4))

    ax2.bar(
        x - 0.15,
        machine_report["Pass"],
        width=0.3,
        label="Pass",
        color="lightgreen",
        edgecolor="black"
    )

    ax2.bar(
        x + 0.15,
        machine_report["Fail"],
        width=0.3,
        label="Fail",
        color="salmon",
        edgecolor="black"
    )

    ax2.set_xticks(x)

    ax2.set_xticklabels(machines)

    ax2.set_xlabel("Machine")

    ax2.set_ylabel("Number of Products")

    ax2.set_title(
        "Machine Performance",
        fontsize=13,
        fontweight="bold"
    )

    ax2.legend()

    ax2.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )

    st.pyplot(fig2, use_container_width=True)

    plt.close(fig2)


# ----------------------------------------------------------
# CHART 3: LENGTH VARIATION
# ----------------------------------------------------------

st.markdown("#### Product Length Variation Analysis")

fig3, ax3 = plt.subplots(figsize=(13, 4))

ax3.plot(
    df["Product_ID"],
    df["Length"],
    marker="o",
    linewidth=2,
    color="royalblue",
    label="Product Length"
)

ax3.axhline(
    max_length,
    color="red",
    linestyle="--",
    label="Maximum Limit (51 mm)"
)

ax3.axhline(
    min_length,
    color="red",
    linestyle="--",
    label="Minimum Limit (49 mm)"
)

ax3.set_xlabel("Product ID")

ax3.set_ylabel("Length (mm)")

ax3.set_title(
    "Length Variation Check",
    fontsize=13,
    fontweight="bold"
)

ax3.legend()

ax3.grid(
    True,
    linestyle="--",
    alpha=0.5
)

plt.xticks(rotation=45)

st.pyplot(fig3, use_container_width=True)

plt.close(fig3)


# ==========================================================
# 16. DEFECT ANALYSIS
# ==========================================================

st.markdown("---")

st.subheader("🔍 Defect Analysis")

defect_counts = df[
    df["Status"] == "Fail"
]["Defect_Reason"].value_counts()

fig4, ax4 = plt.subplots(figsize=(9, 4))

if len(defect_counts) > 0:

    ax4.bar(
        defect_counts.index,
        defect_counts.values,
        color="coral",
        edgecolor="black"
    )

    ax4.set_title(
        "Defect Distribution by Reason",
        fontsize=13,
        fontweight="bold"
    )

    ax4.set_xlabel("Defect Reason")

    ax4.set_ylabel("Number of Products")

    ax4.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )

else:

    ax4.text(
        0.5, 0.5,
        "No Defects Found",
        ha="center",
        va="center"
    )

st.pyplot(fig4, use_container_width=True)

plt.close(fig4)


# ==========================================================
# 17. DOWNLOAD REPORTS
# ==========================================================

st.markdown("---")

st.subheader("📥 Download Manufacturing Reports")

d1, d2 = st.columns(2)

with d1:

    st.download_button(
        label="⬇️ Download Quality Report",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="quality_report.csv",
        mime="text/csv",
        use_container_width=True
    )

with d2:

    st.download_button(
        label="⬇️ Download Machine Report",
        data=machine_report.to_csv().encode("utf-8"),
        file_name="machine_report.csv",
        mime="text/csv",
        use_container_width=True
    )


# ==========================================================
# 18. FOOTER
# ==========================================================

st.markdown("---")

st.markdown("""
<div style="
    text-align:center;
    color:#94a3b8;
    padding:20px;
">

    <h4 style="color:#94a3b8;">
        Manufacturing Quality Analysis Dashboard
    </h4>

    Developed using Python, NumPy, Pandas,
    Matplotlib and Streamlit.

    <br><br>

    Manufacturing Inspection & Quality Control System

</div>
""", unsafe_allow_html=True)
