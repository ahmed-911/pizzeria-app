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
import matplotlib.pyplot as plt
import io
from pptx import Presentation
from pptx.util import Inches

# ---------------- دالة إنشاء PowerPoint ----------------
def create_ppt(title, df, fig):
    prs = Presentation()
    slide_layout = prs.slide_layouts[5]  # Blank slide

    # شريحة الرسم البياني
    slide_chart = prs.slides.add_slide(slide_layout)
    left, top, width, height = Inches(0.5), Inches(0.5), Inches(9), Inches(1)
    txBox = slide_chart.shapes.add_textbox(left, top, width, height)
    txBox.text_frame.text = title

    img_stream = io.BytesIO()
    fig.savefig(img_stream, format='png', bbox_inches="tight")
    img_stream.seek(0)
    slide_chart.shapes.add_picture(img_stream, Inches(1), Inches(1.5), Inches(7), Inches(4))

    # شريحة الجدول
    slide_table = prs.slides.add_slide(slide_layout)
    txBox2 = slide_table.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
    txBox2.text_frame.text = "Table"

    fig_table, ax_table = plt.subplots(figsize=(10, 6))
    ax_table.axis('off')
    tbl = ax_table.table(cellText=df.values, colLabels=df.columns, loc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    plt.tight_layout()

    img_table = io.BytesIO()
    fig_table.savefig(img_table, format='png', bbox_inches='tight')
    plt.close(fig_table)
    img_table.seek(0)
    slide_table.shapes.add_picture(img_table, Inches(0.5), Inches(1.5), width=Inches(9))

    pptx_output = io.BytesIO()
    prs.save(pptx_output)
    pptx_output.seek(0)
    return pptx_output

# ---------------- دالة التحليل ----------------
def analyze_columns(df, selected_cols, chart_option):
    counts = df.groupby(selected_cols).size()

    # اسم عمود العد
    count_col_name = "Count"
    while count_col_name in df.columns:
        count_col_name += "_1"

    counts = counts.reset_index(name=count_col_name)

    # إضافة النسبة
    if chart_option == "Percentages":
        counts["Percentage"] = counts[count_col_name] / counts[count_col_name].sum() * 100

    st.subheader("Results")
    st.dataframe(counts, use_container_width=True)

    # الرسم البياني
    fig, ax = plt.subplots(figsize=(8, 4))
    labels = counts[selected_cols].astype(str).agg(' | '.join, axis=1)

    if chart_option == "Numbers":
        ax.bar(labels, counts[count_col_name])
        ax.set_ylabel("Count")
    else:
        ax.bar(labels, counts["Percentage"])
        ax.set_ylabel("Percentage")

    plt.xticks(rotation=45, ha="right")
    plt.title("Distribution")
    plt.tight_layout()
    st.pyplot(fig)

    # تصدير Excel
    excel_output = io.BytesIO()
    with pd.ExcelWriter(excel_output, engine="openpyxl") as writer:
        counts.to_excel(writer, sheet_name='Analysis', index=False)
    excel_output.seek(0)

    st.download_button(
        "Download Excel",
        data=excel_output,
        file_name="analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # تصدير PowerPoint
    ppt_output = create_ppt("Analysis Results", counts, fig)
    st.download_button(
        "Download PowerPoint",
        data=ppt_output,
        file_name="analysis.pptx",
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )

# ---------------- واجهة التطبيق ----------------
st.title("📊 Excel Column Analysis Tool")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    sheet_name = st.selectbox("Select a sheet", xls.sheet_names)
    df = pd.read_excel(uploaded_file, sheet_name=sheet_name)

    analysis_type = st.radio(
        "Select analysis type",
        ["One column", "Two columns", "Three columns", "Four columns", "Five columns"]
    )

    chart_option = st.radio("Chart Display", ["Numbers", "Percentages"])

    num_cols_map = {
        "One column": 1,
        "Two columns": 2,
        "Three columns": 3,
        "Four columns": 4,
        "Five columns": 5
    }

    num_cols = num_cols_map[analysis_type]

    selected_cols = []
    available_columns = list(df.columns)

    for i in range(num_cols):
        col = st.selectbox(f"Select column {i+1}", available_columns, key=f"col_{i}")
        selected_cols.append(col)
        available_columns = [c for c in available_columns if c != col]

    if len(selected_cols) == num_cols:
        analyze_columns(df, selected_cols, chart_option)