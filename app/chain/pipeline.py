from app.chain.steps import SmolLM
from app.chain.steps import DataFramePromptBuilder
from app.chain.steps import AnswerParser


def create_csv_chain(llm: SmolLM):
    return (DataFramePromptBuilder() | llm | AnswerParser())