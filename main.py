import fitz
import re
from answer import Answer

from quiz_question import QuizQuestion


def extract_text(path: str) -> str:
    pdf = fitz.open(path)
    text = ''
    for page in pdf:
        text += page.get_text()
    return text


def extract_lines(path: str) -> list[str]:
    return extract_text(path).split('\n')


def pdf_to_txt(path: str) -> str:
    pdf = fitz.open(path)
    path = path.removesuffix('.pdf') + '.txt'
    with open(path, "wb") as file:
        for page in pdf:
            text = page.get_text().encode("utf8")
            file.write(text)
    return path

def get_question_block(lines: list[str]) -> list[str]:
    start_index: int = None
    end_index: int = None
    for i in range(len(lines)):
        line = lines[i]
        new_question = re.match(r'\d+\.', line)
        if new_question and start_index == None:
            start_index = i+1
            continue
        if new_question and start_index != None:
            end_index = i
            break
    return (start_index, end_index)


def extract_question(question_block: list[str], sanitize_text: str, silent:bool=False):
    if sanitize_text in question_block:
        sanitize_text_index = question_block.index(sanitize_text)
        question_block = question_block[:sanitize_text_index]
    letters = ['A', 'B', 'C', 'D']

    # texto da pergunta
    question_text_end = question_block.index('A')
    question_text = ' '.join(question_block[:question_text_end])

    # respostas
    answers = []
    for i in range(4):
        try:
            start = question_block.index(letters[i]) + 1
            end = question_block.index(letters[i+1]) if i < 3 else len(block)
            answer_text = ' '.join(question_block[start:end])
            answers.append(Answer(answer_text))
        except ValueError as e:
            if not silent: raise ValueError("Formato incorreto")
    return QuizQuestion(question_text, 0, answers)

if __name__ == '__main__':
    lines = extract_lines('teste.pdf')
    sanitize_text = lines[0]
    n = 1
    while True:
        input()
        start, end = get_question_block(lines)
        block = lines[start: end]
        lines = lines[end:]
        print('\n'+'-'*30+'\n')
        print(n)
        print(extract_question(block, sanitize_text, silent=True))
        print('\n'+'-'*30+'\n')
        n += 1


'''

O meio de transmissão a ser fortemente considerado, quando a interferência e
a distância se constituir num problema crítico de um projeto de rede, é?    
A
cabo par trançado CAT6.
B
cabo de fibra óptica.
C
cabo STP.
D
cabo coaxial.

'''
