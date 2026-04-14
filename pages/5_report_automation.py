from theme import apply_theme, render_sidebar
from auth import init_auth, require_login
import streamlit as st
import pandas as pd
from pptx import Presentation
from io import BytesIO

COMPANY_NAME = "Pizzeria Insights"

apply_theme()
init_auth()

if not require_login():
    st.warning("Please log in first.")
    st.stop()

render_sidebar(COMPANY_NAME)

st.title("📊 Report Automation (Excel ➜ PowerPoint)")

# ---------------- Upload Files ----------------
excel_file = st.file_uploader("Upload Excel File", type=["xlsx"])
ppt_file = st.file_uploader("Upload PowerPoint Template", type=["pptx"])

if excel_file and ppt_file:
    df = pd.read_excel(excel_file)

    st.subheader("Select Columns")

    csat_col = st.selectbox("CSAT Column (1-5)", df.columns)
    ces_col = st.selectbox("CES Column (1-7)", df.columns)
    nps_col = st.selectbox("NPS Column (1-10)", df.columns)

    st.subheader("Report Info")

    title = st.text_input("Report Title", "Customer Experience Report")
    date = st.text_input("Report Date", "April 2026")

    if st.button("Generate Report 🚀"):

        # ---------------- Calculations ----------------
        csat_data = pd.to_numeric(df[csat_col], errors='coerce').dropna()
        ces_data = pd.to_numeric(df[ces_col], errors='coerce').dropna()
        nps_data = pd.to_numeric(df[nps_col], errors='coerce').dropna()

        csat_score = (csat_data[csat_data >= 4].count() / len(csat_data)) * 100
        ces_score = (ces_data[ces_data >= 5].count() / len(ces_data)) * 100

        promoters = nps_data[nps_data >= 9].count()
        detractors = nps_data[nps_data <= 6].count()
        nps_score = ((promoters / len(nps_data)) * 100) - ((detractors / len(nps_data)) * 100)

        # ---------------- Placeholder Map ----------------
        placeholder_map = {
            "[[TITLE_01]]": title,
            "[[DATE_01]]": date,
            "[[CSAT_01]]": f"{csat_score:.1f}%",
            "[[CES_01]]": f"{ces_score:.1f}%",
            "[[NPS_01]]": f"{nps_score:.1f}"
        }

        # ---------------- Replace Text in PPT ----------------
        prs = Presentation(ppt_file)

        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text = shape.text
                    for key, value in placeholder_map.items():
                        if key in text:
                            shape.text = text.replace(key, value)

        # ---------------- Save Output ----------------
        output = BytesIO()
        prs.save(output)
        output.seek(0)

        st.success("Report Generated Successfully 🎉")

        st.download_button(
            label="Download PowerPoint",
            data=output.getvalue(),
            file_name="Automated_Report.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )