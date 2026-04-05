from theme import apply_theme, render_sidebar
from auth import init_auth, require_login
import streamlit as st

COMPANY_NAME = "Pizzeria Insights"

apply_theme()
init_auth()

if not require_login():
    st.warning("Please log in first.")
    st.stop()

render_sidebar(COMPANY_NAME)
import streamlit as st
import pandas as pd
from io import BytesIO

st.title("📊 CES ")

# رفع الملف
uploaded_file = st.file_uploader("⬆️ ارفع ملف Excel", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("🧾 الأعمدة:")
    st.write(df.columns.tolist())

    selected_columns = st.multiselect("🔍 اختر الأعمدة للتحليل", df.columns)

    if selected_columns:
        df_clean = df[selected_columns].apply(pd.to_numeric, errors='coerce')

        results = {}
        for col in selected_columns:
            col_data = df_clean[col].dropna()

            total = col_data.shape[0]
            satisfied = col_data[col_data >= 5].shape[0]  # 5-6-7
            percent = (satisfied / total) * 100 if total > 0 else 0

            results[col] = {
                "عدد المشاركين": total,
                "عدد الراضين (5-7)": satisfied,
                "نسبة الرضا (%)": round(percent, 1)
            }

        results_df = pd.DataFrame(results).T.reset_index().rename(columns={"index": "البند"})

        # عرض النتائج
        st.subheader("📈 النتائج")
        st.dataframe(results_df, use_container_width=True)
        st.bar_chart(results_df.set_index("البند")["نسبة الرضا (%)"])

        # الرضا العام
        total_all = df_clean[selected_columns].count().sum()
        satisfied_all = df_clean[selected_columns].apply(lambda x: (x >= 5).sum()).sum()
        overall = (satisfied_all / total_all) * 100 if total_all > 0 else 0

        st.markdown(f"### 🔹 معدل الرضا العام: **{overall:.1f}%**")

        # تحميل النتائج
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            results_df.to_excel(writer, index=False)

        st.download_button(
            "💾 تحميل النتائج Excel",
            data=output.getvalue(),
            file_name="ces_results.xlsx"
        )