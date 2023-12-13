import re
import os
from PyPDF2 import PdfReader

# getting a specific page from the pdf file


def get_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)
    pages_text = ""
    for i in range(num_pages):
        page = reader.pages[i]
        text = page.extract_text()
        pages_text += text
    return pages_text


def convert_pdf_to_txt(pdf_path):
    path, extension = os.path.splitext(pdf_path)
    with open(path + ".txt", "w", encoding="utf-8") as file:
        file.write(get_pdf_text(pdf_path))


def extract_questions(file_name):
    questions = []
    lines = []
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            lines.append(line.removesuffix('\n'))

    for line in lines:
        print(re.match(r'\d+\.\s', line))
    return questions

extract_questions("teste.txt")