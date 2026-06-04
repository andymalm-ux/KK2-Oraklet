from fastapi import FastAPI
from pydantic import BaseModel
from app.chain.runnable import TicketInput, ticket_pipeline

app = FastAPI()

class LLMRequest(BaseModel):
    id: int
    message: str

@app.post("/llm")
def llm_route(body: LLMRequest):
    incoming_ticket = TicketInput(
        customer_id=body.id,
        message=body.message
    )
    return ticket_pipeline.invoke(incoming_ticket)

from .data import router as data_router
from .chain.steps import router as steps_router

app.include_router(data_router)
app.include_router(steps_router)