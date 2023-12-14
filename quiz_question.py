from answer import Answer

class QuizQuestion:
    def __init__(self, question: str = '', difficulty: int = 0, answers: list[Answer] = []) -> None:
        self.question = question
        self.difficulty = difficulty
        self.answers = answers
    
    def __str__(self) -> str:
        letters = ['A','B','C','D']
        answers = ''
        for letter, answer in zip(letters, self.answers):
            answers += f'{letter} - {answer}\n'
        return f'''
{self.question}
{self.difficulty}
{answers}
'''