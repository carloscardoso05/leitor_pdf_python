class Answer:
    def __init__(self, text: str = "", correct: bool = False) -> None:
        self.text = text
        self.correct = correct
    def __str__(self) -> str:
        return f'{self.text} --- {self.correct}'