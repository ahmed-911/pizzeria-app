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
# pages/3_nps.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from pptx import Presentation
from pptx.util import Inches, Pt
import xlsxwriter

# دالة لإنشاء ملف PowerPoint مع نتائج NPS
def create_pptx_with_nps_results(
    nps_score,
    promoter_percent,
    passive_percent,
    detractor_percent,
    total_responses,
    nps_column
):
    prs = Presentation()

    # شريحة العنوان
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    try:
        slide.shapes.title.text = f"NPS للعمود: {nps_column}"
    except Exception:
        tx = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
        tx.text_frame.text = f"NPS للعمود: {nps_column}"

    # شريحة النتائج
    blank_slide_layout = prs.slide_layouts[5]
    slide = prs.slides.add_slide(blank_slide_layout)

    tx = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(1))
    tx.text_frame.text = "نتائج NPS"

    tf = slide.shapes.add_textbox(Inches(1), Inches(1.2), Inches(8), Inches(4)).text_frame

    p = tf.paragraphs[0]
    p.text = f"صافي نقاط الترويج (NPS): {nps_score:.2f}"
    p.font.bold = True
    p.font.size = Pt(18)

    tf.add_paragraph().text = f"النسبة المئوية للمروجين: {promoter_percent:.2f}%"
    tf.add_paragraph().text = f"النسبة المئوية للمحايدين: {passive_percent:.2f}%"
    tf.add_paragraph().text = f"النسبة المئوية للمنتقدين: {detractor_percent:.2f}%"
    tf.add_paragraph().text = f"حجم العينة: {total_responses}"

    # شريحة الرسم البياني
    slide = prs.slides.add_slide(blank_slide_layout)
    slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(1)).text_frame.text = "توزيع فئات NPS"

    chart_data = pd.DataFrame({
        "الفئة": ["المروجون", "المحايدون", "المنتقدون"],
        "النسبة المئوية": [promoter_percent, passive_percent, detractor_percent]
    })

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(chart_data["الفئة"], chart_data["النسبة المئوية"], color=["green", "orange", "red"])
    ax.set_title("توزيع فئات NPS")
    ax.set_ylabel("النسبة المئوية")
    plt.tight_layout()

    chart_image = io.BytesIO()
    fig.savefig(chart_image, format="png", bbox_inches="tight")
    chart_image.seek(0)
    slide.shapes.add_picture(chart_image, Inches(1), Inches(1.5), width=Inches(8))
    plt.close(fig)

    output = io.BytesIO()
    prs.save(output)
    output.seek(0)
    return output


st.title("📊 NPS")
uploaded_file = st.file_uploader("⬆️ ارفع ملف Excel", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        # قراءة الملف
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, encoding="utf-8")
        else:
            df = pd.read_excel(uploaded_file)

        df.columns = df.columns.str.strip()
        nps_column = st.selectbox("اختر العمود المراد تحليله:", df.columns.tolist())

        if nps_column:
            st.subheader(f"تحليل العمود: {nps_column}")

            nps_data = pd.to_numeric(df[nps_column], errors="coerce").dropna()
            total_responses = len(nps_data)

            if total_responses > 0:
                promoters = nps_data[nps_data >= 9].count()
                passives = nps_data[(nps_data >= 7) & (nps_data <= 8)].count()
                detractors = nps_data[nps_data <= 6].count()

                promoter_percent = (promoters / total_responses) * 100
                passive_percent = (passives / total_responses) * 100
                detractor_percent = (detractors / total_responses) * 100

                nps_score = promoter_percent - detractor_percent

                st.markdown(f"**حجم العينة:** {total_responses}")

                results_df = pd.DataFrame({
                    "الفئة": ["المروجون", "المحايدون", "المنتقدون"],
                    "العدد": [promoters, passives, detractors],
                    "النسبة المئوية": [
                        f"{promoter_percent:.2f}%",
                        f"{passive_percent:.2f}%",
                        f"{detractor_percent:.2f}%"
                    ]
                })

                st.dataframe(results_df, use_container_width=True)

                chart_counts_df = pd.DataFrame({
                    "الفئة": ["المروجون", "المحايدون", "المنتقدون"],
                    "العدد": [promoters, passives, detractors]
                })
                st.bar_chart(chart_counts_df.set_index("الفئة")["العدد"])

                st.metric(label="صافي نقاط الترويج (NPS)", value=f"{nps_score:.2f}")

                if nps_score >= 50:
                    st.success("النتيجة ممتازة! لديك قاعدة عملاء مخلصين جدًا.")
                elif nps_score >= 0:
                    st.info("النتيجة جيدة. لديك عدد من العملاء الراضين.")
                else:
                    st.warning("النتيجة تحتاج إلى تحسين.")

                st.subheader("تصدير النتائج")

                excel_output = io.BytesIO()
                with pd.ExcelWriter(excel_output, engine="xlsxwriter") as writer:
                    results_df.to_excel(writer, sheet_name="NPS_Analysis", index=False)

                st.download_button(
                    label="تصدير إلى Excel",
                    data=excel_output.getvalue(),
                    file_name="NPS_Analysis.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

                pptx_output = create_pptx_with_nps_results(
                    nps_score,
                    promoter_percent,
                    passive_percent,
                    detractor_percent,
                    total_responses,
                    nps_column
                )

                st.download_button(
                    label="تصدير إلى PowerPoint",
                    data=pptx_output.getvalue(),
                    file_name="NPS_Presentation.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )

            else:
                st.warning("لا توجد بيانات رقمية كافية في العمود المحدد.")

    except Exception as e:
        st.error(f"حدث خطأ أثناء معالجة الملف: {e}")