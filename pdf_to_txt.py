import pypdfium2 as pdfium
pdf = pdfium.PdfDocument("data/manual.pdf")
version = pdf.get_version()  # get the PDF standard version
n_pages = len(pdf)  # get the number of pages in the document
page = pdf[24].get_textpage()  # load a page
text = page.get_text_range()
import re

text = re.sub(r"<br />", " ", text)
print(text.splitlines())
# import tabula
# dfs = tabula.io.read_pdf("data/manual.pdf", pages=24)
# print(dfs)
# dfs.to_csv('data/parsed.csv')

import tabula
from typing import Text

def convert_text_page(page, file_dir): 
    pdf = pdfium.PdfDocument("data/manual.pdf")
    n_pages = len(pdf)  # get the number of pages in the document
    
    page = pdf[24].get_textpage()  # load a page
    text = page.get_text_range()


# def main(file_path: Text): 
#     pdf = pdfium.PdfDocument(file_path)
#     n_pages = len(pdf)
#     for page_no in range(n_pages): 
