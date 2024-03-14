import re
from typing import List
from openpyxl import Workbook
from models import Questao, Resposta
import os

class Reader:
    def __init__(self, input_lines: List[str]):
        self.input_lines = input_lines
        self.in_questions_section = True
        self.position = 0
        self.read_position = 0
        self.line = ''
        self.read_line()

    def read_line(self):
        if self.read_position >= len(self.input_lines):
            self.line = ''
        else:
            self.line = self.input_lines[self.read_position].strip()
            self.position = self.read_position
            self.read_position += 1
            while self.read_position < len(self.input_lines) and len(self.line.strip()) == 0:
                self.line = self.input_lines[self.read_position].strip()
                self.position = self.read_position
                self.read_position += 1

    def has_ended(self):
        return self.read_position >= len(self.input_lines)

    def get_next_question(self, questions: List[Questao]):
        q = Questao()
        id = self.get_question_id(self.line)
        self.read_line()
        q.id = id

        while not self.is_choice(self.line):
            q.texto += self.line
            self.read_line()

        for _ in range(4):
            q.respostas.append(self.get_next_answer())

        questions.append(q)

        if self.is_answers_section(self.line):
            self.in_questions_section = False
            self.read_line()

    def get_next_correct_answer(self, questions: List[Questao]):
        id = self.get_question_id(self.line)
        self.read_line()
        letra = self.line[0]
        self.line = self.line[2:]
        for i, q in enumerate(questions):
            if q.id == id:
                for j, rs in enumerate(q.respostas):
                    if rs.letra == letra:
                        questions[i].respostas[j].correta = True
                break
        while not self.is_question_number(self.line) and not self.has_ended():
            self.read_line()

    def get_next_answer(self) -> Resposta:
        res = Resposta()
        res.letra = self.line[0]
        self.read_line()
        while not (self.is_choice(self.line) or self.is_answers_section(self.line) or self.is_question_number(self.line)):
            res.texto += self.line
            self.read_line()
        return res

    @staticmethod
    def get_question_id(line: str) -> int:
        number_string = ''.join(filter(str.isdigit, line))
        return int(number_string)


    @staticmethod
    def is_answers_section(line: str) -> bool:
        return re.search(r'[Cc]haves? de [Rr]espostas?', line) is not None

    @staticmethod
    def is_question_number(line: str) -> bool:
        return re.match(r'^\d+\.$', line) is not None

    @staticmethod
    def is_choice(line: str) -> bool:
        return re.search(r'[abcd]\)', line) is not None

def convert_txt_to_xlxs(path: str):
    base, extension = os.path.splitext(path)
    with open(path, "r") as file:
        content = file.readlines()

    questions = []
    r = Reader(content)

    while not r.has_ended():
        if r.in_questions_section:
            r.get_next_question(questions)
        else:
            r.get_next_correct_answer(questions)

    wb = Workbook()
    sheet = wb.active
    sheet.title = "questões"

    header = ["question_id", "question_text", "a", "b", "c", "d", "correct", "difficulty"]
    sheet.append(header)

    for q in questions:
        letra = next((res.letra for res in q.respostas if res.correta), 'a')
        row = [q.id - 1, q.texto] + [res.texto for res in q.respostas] + [letra, 0]
        sheet.append(row)

    wb.save(base + '.xlsx')

if __name__ == "__main__":
    convert_txt_to_xlxs()
