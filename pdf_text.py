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
    file_path = path + ".txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(get_pdf_text(pdf_path))
    return file_path


def extract_questions(file_name):
    questions = []
    lines = []
    question_text = ""
    in_question = False
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            lines.append(line.removesuffix('\n'))

    for line in lines:
        question_start: re.Match = re.match(r'\d+\.\s', line)
        if question_start:
            in_question = True
            if question_text:
                questions.append(question_text)
            question_text = ""
            start_size = question_start.span()[1] - question_start.span()[0]
            question_text += line[start_size:]
            continue
        if in_question:
            question_text += line

    return questions

if __name__ == "__main__":
    file_pdf = "teste.pdf"
    file_txt = convert_pdf_to_txt(file_pdf)
    questions = extract_questions(file_txt)
    with open("questoes.txt", "w", encoding="utf-8") as file:
        for index, value in enumerate(questions):
            file.write(f"Questão {index+1}:\n")
            file.write(value)
            file.write("\n"*2)
