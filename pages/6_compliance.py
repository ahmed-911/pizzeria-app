
from theme import apply_theme, render_sidebar
from auth import init_auth, login_form, require_login
import streamlit as st
import pandas as pd
from io import BytesIO

COMPANY_NAME = "Pizzeria Insights"

# =========================
# Theme & Authentication
# =========================
apply_theme()
init_auth()

if not require_login():
    login_form(COMPANY_NAME)
    st.stop()

render_sidebar(COMPANY_NAME)

# =========================
# Page
# =========================
st.title("✅ Compliance Analysis")

st.markdown("""
Analyze compliance based on **Yes / No** values.

- ✅ **Yes** = Compliant
- ❌ **No** = Not Compliant

Compliance Rate = (Number of **Yes** ÷ Total Responses) × 100
""")

uploaded_file = st.file_uploader(
    "📂 Upload Excel File",
    type=["xlsx", "xls"]
)

# =========================
# Read Excel
# =========================
if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.subheader("📋 Available Columns")
    st.write(df.columns.tolist())

    selected_columns = st.multiselect(
        "Select Compliance Columns",
        df.columns
    )

    if selected_columns:

        results = []

        for col in selected_columns:

            # تحويل البيانات إلى نص
            data = (
                df[col]
                .dropna()
                .astype(str)
                .str.strip()
                .str.lower()
            )

            total = len(data)

            compliant = data.isin([
                "yes",
                "نعم"
            ]).sum()

            not_compliant = data.isin([
                "no",
                "لا"
            ]).sum()

            compliance_rate = (
                compliant / total * 100
                if total > 0 else 0
            )

            results.append({
                "Item": col,
                "Total Responses": total,
                "Compliant": compliant,
                "Not Compliant": not_compliant,
                "Compliance Rate (%)": round(compliance_rate, 1)
            })

        results_df = pd.DataFrame(results)

        st.subheader("📊 Compliance Results")

        st.dataframe(
            results_df,
            use_container_width=True
        )

        st.bar_chart(
            results_df.set_index("Item")["Compliance Rate (%)"]
        )

        # =========================
        # Overall Compliance
        # =========================

        overall_total = results_df["Total Responses"].sum()

        overall_compliant = results_df["Compliant"].sum()

        overall_rate = (
            overall_compliant / overall_total * 100
            if overall_total > 0 else 0
        )

        st.metric(
            "Overall Compliance Rate",
            f"{overall_rate:.1f}%"
        )

        # =========================
        # Export Excel
        # =========================

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            results_df.to_excel(
                writer,
                index=False,
                sheet_name="Compliance Results"
            )

        st.download_button(
            label="📥 Download Excel Report",
            data=output.getvalue(),
            file_name="compliance_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
