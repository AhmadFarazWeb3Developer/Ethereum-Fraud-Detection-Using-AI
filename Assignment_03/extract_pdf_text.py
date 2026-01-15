import pdfplumber

with pdfplumber.open("Assignment 3_ Methodology Implementation and Answering Key Questions.pdf") as pdf:
    text = ""
    for page in pdf.pages:
        text += page.extract_text() + "\n"

print(text)