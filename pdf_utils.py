from io import BytesIO
from fpdf import FPDF

def df_to_pdf(dataframe):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    col_width = pdf.w / (len(dataframe.columns) + 1)
    row_height = pdf.font_size * 1.5

    # Header
    for col in dataframe.columns:
        pdf.cell(col_width, row_height, str(col), border=1)
    pdf.ln(row_height)
    # Rows
    for i, row in dataframe.iterrows():
        for item in row:
            pdf.cell(col_width, row_height, str(item), border=1)
        pdf.ln(row_height)
    pdf_output = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    return pdf_output