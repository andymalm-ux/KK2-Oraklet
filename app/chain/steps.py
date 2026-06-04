from transformers import pipeline
from pydantic import PrivateAttr
from app.chain.runnable import Runnable
from app.schemas import DataFrameContext, Answer, QuestionInput
from fastapi import APIRouter, HTTPException, Request
import pandas as pd

router = APIRouter()

class DataFramePromptBuilder(
    Runnable[DataFrameContext, str]
):
    def invoke(self, data: DataFrameContext) -> str:

        df = pd.DataFrame(data.csv_data)

        preview = df.head(10).to_string()

        return f"""
Du är en assistent som analyserar CSV-data.

Regler:
- Använd endast information från tabellen.
- Hitta inte på information.
- Om information saknas ska du säga det.
- Svara kortfattat.

Tabell:

{preview}

Fråga:
{data.question}

Svar:
"""  
class SmolLM(Runnable[str, str]):
    model_name: str = "HuggingFaceTB/SmolLM2-360M-Instruct"

    _pipe = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)

        print(f"Loading {self.model_name}...")
        self._pipe = pipeline(
            "text-generation",
            model=self.model_name
        )
        print("Model loaded successfully!")

    def invoke(self, data: str):
        messages = [{"role": "user", "content": data}]
        output = self._pipe(messages, max_new_tokens=200)

        return output[0]["generated_text"][-1]["content"]

class AnswerParser(Runnable[str, Answer]):
    def invoke(self, data: str) -> Answer:

        return Answer(answer=data.strip()) 

@router.post("/AI/ask")
def ask(
    question: QuestionInput,
    request: Request
):

    csv_data = request.app.state.csv_data

    if not csv_data:
        raise HTTPException(
            status_code=404,
            detail="No CSV file uploaded."
        )

    context = DataFrameContext(
        question=question.question,
        csv_data=csv_data
    )

    chain = request.app.state.csv_chain

    return chain.invoke(context)