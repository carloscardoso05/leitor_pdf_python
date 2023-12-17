import pandas as pd
from extract_data import *
import itertools as it
import os


def convert_quiz_pdf_to_xlsx(file_name: str) -> str:
    file_path, extension = os.path.splitext(file_name)
    text = pdf_to_text(file_name)
    clean_text = clear_text(text, unwanted_matches)
    answers = get_correct_answers(clean_text)
    questions = get_questions(clean_text)
    questions = check_answers(questions, answers)

    questions_table = [
        [
            question.question,
            *[answer.text for answer in question.answers],
            find_correct_letter(question),
            question.difficulty
        ] for question in questions
    ]

    question_columns = ['question_text', 'a',
                        'b', 'c', 'd', 'correct', 'difficulty']

    df = pd.DataFrame(data=questions_table, columns=question_columns)
    excel_path = file_path+".xlsx"
    try:
        df.to_excel(excel_path, sheet_name='quiz', index_label='question_id')
    except PermissionError as error:
        error.add_note(
            f'Erro: arquivo {excel_path} aberto em outro processo')
        raise error
