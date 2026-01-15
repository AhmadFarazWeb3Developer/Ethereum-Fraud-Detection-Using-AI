import pdfplumber

with pdfplumber.open("Assignment 4_ Model Deployment, Feedback Collection, and Iterative Improvement.pdf") as pdf:
    text = ""
    for page in pdf.pages:
        text += page.extract_text() + "\n"

print(text)