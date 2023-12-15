import pandas as pd
from extract_data import *
import itertools as it
import os


def convert_quiz_pdf_to_xlsx(file_name: str) -> str:
    file_path, extension = os.path.splitext(file_name)
    txt_file = pdf_to_txt(file_name)
    clear_txt_file(txt_file, unwanted_matches)
    answers = get_correct_answers(txt_file)
    questions = get_questions(txt_file)
    questions = check_answers(questions, answers)

    questions_table = [
        [question.question,
         *[answer.text for answer in question.answers],
         find_correct_letter(question),
         question.difficulty] for question in questions
    ]

    question_columns = ['question_text', 'a','b','c','d','correct','difficulty']
    
    df = pd.DataFrame(data=questions_table, columns=question_columns)
    try:
        df.to_excel(file_path+".xlsx", sheet_name='quiz')
    except PermissionError as error:
        error.add_note(f'Erro: arquivo {file_path+".xlsx"} aberto em outro processo')
        raise error
