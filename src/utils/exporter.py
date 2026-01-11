from markdown import markdown
from datetime import datetime
from fpdf import FPDF

def exportToPDF(text: str):
    cleaned_text = text.replace('–', '-')

    time = datetime.now().strftime('%Y-%m-%d')
    html = markdown(cleaned_text)

    print(f'\n CLEANED TEXT: \n{cleaned_text}\n\n')
    print(f'\n HTML: \n{html}\n\n')

    pdf = FPDF()
    pdf.add_page()
    pdf.write_html(html)

    output_filename = f'./data/exports/{time}-newsletter.pdf'

    pdf.output(output_filename)