from pydantic import BaseModel

class QuestionInput(BaseModel):
    question: str


class DataFrameContext(BaseModel):
    question: str
    csv_data: list[dict]


class Answer(BaseModel):
    answer: str