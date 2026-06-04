from transformers import pipeline
from pydantic import BaseModel, PrivateAttr
from app.chain.runnable import Runnable
from fastapi import APIRouter

router = APIRouter()

class PromptInput(BaseModel):
  question: str

class PromptBuilder(Runnable[PromptInput, str]):
  def invoke(self, data: PromptInput) -> str:
    return data.question
  
class SmolLM(Runnable[str, str]):
    model_name: str = "HuggingFaceTB/SmolLM-135M-Instruct"

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
  
chain = (PromptBuilder() | SmolLM() | Parser())

@router.post("/AI/ask", response_model=Answer)
def ask(question: PromptInput):
  result = chain.invoke(question)

  return result