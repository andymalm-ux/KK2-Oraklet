from transformers import pipeline
from pydantic import BaseModel, PrivateAttr
from app.chain.runnable import Runnable
from fastapi import APIRouter, Request
import pandas as pd

router = APIRouter()

class PromptInput(BaseModel):
  question: str

class PromptBuilder(Runnable[PromptInput, str]):
  def invoke(self, data: PromptInput) -> str:
    return data.question
  
class QuestionInput(BaseModel):
  question: str

class DataFramePromptBuilder(Runnable[DataFrameContext, str]):
  def invoke(self, data: DataFrameContext) -> str:

      df = pd.DataFrame(data.csv_data)

      return f"""
Du är en assistent som analyserar CSV-data.

Regler:
- Använd endast information från tabellen.
- Hitta inte på information.
- Om svaret inte finns i tabellen ska du säga det.
- Om användaren ber om innehållet i tabellen ska du visa raderna.

Tabell:

{df.head(10).to_string()}

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
        output = self._pipe(messages, max_new_tokens=150)

        return output[0]["generated_text"][-1]["content"]
  
class Answer(BaseModel):
  answer: str

class Parser(Runnable[str, Answer]):
  def invoke(self, data: str) -> Answer:
    answer = data.split("Svar: ")[-1].strip()
    return Answer(answer=answer)
  
chain = (DataFramePromptBuilder() | SmolLM() | Parser())

# @router.post("/AI/ask", response_model=Answer)
# def ask(question: DataFrameContext):
#   result = chain.invoke(question)

#   return result

@router.post("/AI/ask")
def ask(
    question: QuestionInput,
    request: Request
):
    csv_data = request.app.state.csv_data

    context = DataFrameContext(
        question=question.question,
        csv_data=csv_data
    )

    return chain.invoke(context)