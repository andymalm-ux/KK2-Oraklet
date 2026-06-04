from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
# from app.chain.runnable import TicketInput
from app.chain.steps import SmolLM

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.llm = SmolLM()

    yield

    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

from .data import router as data_router
from .chain.steps import router as steps_router

app.include_router(data_router)
app.include_router(steps_router)