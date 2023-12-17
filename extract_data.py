import fitz
import re
from answer import Answer
from quiz_question import QuizQuestion
import os


def extract_text(path: str) -> str:
    pdf = fitz.open(path)
    text = ''
    for page in pdf:
        text += page.get_text()
    return text


def extract_lines(path: str) -> list[str]:
    return extract_text(path).split('\n')


def pdf_to_text(path: str) -> str:
    pdf = fitz.open(path)
    text = ''
    for page in pdf:
        text += page.get_text()
    return text


def try_split(match: str, text: str):
    try:
        match_span = re.search(match, text).span()
    except:
        match_span = (-1, 0)
    first_part, remainder = text[:match_span[0]], text[match_span[1]:]
    return first_part, remainder


def get_questions(text) -> list[QuizQuestion]:
    questions = []
    answers_start = re.search(r'\nChave de respostas\n', text).start()
    only_questions = text[:answers_start]
    questions_blocks = re.split(r'\n\d+\.\n', only_questions)
    questions_blocks[0] = re.sub(r'^\d+\.\n', '', questions_blocks[0])
    for question_text in questions_blocks:
        question, remainder = try_split(r'\nA\n', question_text)
        answer_a, remainder = try_split(r'\nB\n', remainder)
        answer_b, remainder = try_split(r'\nC\n', remainder)
        answer_c, answer_d = try_split(r'\nD\n', remainder)
        answers = [Answer(re.sub('\n', ' ', answer), False)
                   for answer in (answer_a, answer_b, answer_c, answer_d)]
        questions.append(QuizQuestion(re.sub('\n', ' ', question), 0, answers))
    return questions


def get_correct_index(letter: str):
    letter = letter.lower()
    return ['a', 'b', 'c', 'd'].index(letter)


def get_correct_letter(index: str):
    return ['a', 'b', 'c', 'd'][index]


def find_correct_letter(question: QuizQuestion):
    for i, answer in enumerate(question.answers):
        if answer.correct:
            return get_correct_letter(i)


def get_correct_answers(text):
    answers_start = re.search(r'\nChave de respostas\n', text).end()
    only_answers = text[answers_start:]
    answers_blocks = re.split(r'\n\d+\.\s', only_answers)
    answers_blocks[0] = re.sub(r'^\d+\.\s', '', answers_blocks[0])
    answers_blocks[-1] = re.sub(r'\n$', '', answers_blocks[-1])
    return answers_blocks


def clear_text(text: str, unwanted_matches: list[str]) -> str:
    clean_text = ''
    for block in unwanted_matches:
        text = re.sub(block, '', text)
    clean_text = text
    return clean_text


def check_answers(questions: list[QuizQuestion], answers: list[str]):
    questions_copy = questions[:]
    for i, question in enumerate(questions_copy):
        correct_letter = get_correct_index(answers[i])
        question.answers[correct_letter].correct = True
    return questions_copy


unwanted_matches = [
    r'\d{2}\/\d{2}\/\d{4},\s\d{2}:\d{2}\n.+\nhttps:\/\/quizizz\.com\/print\/quiz\/.+\n.+\n',
    r'.+\nhttps:\/\/quizizz\.com\/print\/quiz\/.+\n.+\n\d{2}\/\d{2}\/\d{4},\s\d{2}:\d{2}\n',
    r'\n'.join([
        r'.+',
        r'.+',
        r'NOME.*',
        r'TURMA.*',
        r'DATA.*',
        r'.+\n'
    ])
]