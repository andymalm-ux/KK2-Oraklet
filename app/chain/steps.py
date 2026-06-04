from transformers import pipeline
# from pprint import pprint
from pydantic import BaseModel, PrivateAttr
from app.chain.runnable import Runnable
from fastapi import APIRouter

router = APIRouter()

class PromptInput(BaseModel):
  question: str

class PromptBuilder(Runnable[PromptInput, str]):
  def invoke(self, data: PromptInput) -> str:
    return f"""
Svara kort på följande fråga:

Fråga: {data.question}

Svar:
"""
  
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

# result = chain.invoke(
#   PromptInput(
#     question="Vad är Python?"
#   )
# )
# print(result)

# class PromptTemplate:
#   def __init__(self, template_str: str):
#     self.template_str = template_str
  
#   def format(self, **kwargs):
#     return self.template_str.format(**kwargs)

#   def __or__(self, other):
#     if isinstance(other, SmolLM):
#         return LLMChain(
#         prompt_template=self,
#         llm=other
#         )
#     raise TypeError("It's not an instance of SmolLM")

# class LLMChain:
#   def __init__(
#     self, 
#     prompt_template: PromptTemplate,
#     llm: SmolLM
#   ):
#     self.prompt_template = prompt_template
#     self.llm = llm
  
#   def invoke(self, **kwargs):
#     formatted_prompt = self.prompt_template.format(**kwargs)
#     return self.llm.invoke(formatted_prompt)    
  
# llm = SmolLM()

# recipe_prompt = PromptTemplate(
#   template_str="Give me a quick 2-step recipe for a {dish} using only {ingredient_count} ingredients."
# )

# recipe_chain = recipe_prompt | llm

# result = recipe_chain.invoke(dish="ramen", ingredient_count="two")
# pprint(result)

