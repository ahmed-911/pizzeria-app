from io import BytesIO

import pandas as pd
import streamlit as st
from auth import init_auth, login_form, require_login
from theme import apply_theme, render_sidebar
import streamlit as st

COMPANY_NAME = "Pizzeria Insights"

apply_theme()
init_auth()

if not require_login():
    login_form(COMPANY_NAME)
    st.stop()

render_sidebar(COMPANY_NAME)

st.title("📊 CSAT Analysis")

uploaded_file = st.file_uploader("⬆️ Upload Excel", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("🧾 الأعمدة الموجودة")
    st.write(df.columns.tolist())

    selected_columns = st.multiselect("🔍 اختر الأعمدة للتحليل", df.columns)

    if selected_columns:
        df_numeric = df[selected_columns].apply(pd.to_numeric, errors="coerce")

        results = {}

        for col in selected_columns:
            col_data = df_numeric[col].dropna()

            total = col_data.shape[0]
            satisfied = col_data[col_data >= 4].shape[0]
            percent = (satisfied / total) * 100 if total > 0 else 0

            results[col] = {
                "عدد المشاركين": total,
                "عدد الراضين (4-5)": satisfied,
                "نسبة الرضا (%)": round(percent, 1)
            }

        results_df = (
            pd.DataFrame(results)
            .T
            .reset_index()
            .rename(columns={"index": "البند"})
        )

        st.subheader("📈 النتائج")
        st.dataframe(results_df, use_container_width=True)

        st.bar_chart(
            results_df.set_index("البند")["نسبة الرضا (%)"]
        )

        total_all = df_numeric[selected_columns].count().sum()
        satisfied_all = df_numeric[selected_columns].apply(lambda x: (x >= 4).sum()).sum()
        overall = (satisfied_all / total_all) * 100 if total_all > 0 else 0

        st.markdown(f"### 🔹 معدل الرضا العام: **{overall:.1f}%**")

        output = BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            results_df.to_excel(writer, index=False, sheet_name="CSAT Results")

        st.download_button(
            label="💾 تحميل النتائج Excel",
            data=output.getvalue(),
            file_name="csat_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
