import pymupdf
import fitz
import pandas as pd


doc = pymupdf.open("EarningsReports/spot.pdf") # open a document

for page in doc:
    text = page.get_text("text")
    print(text)
