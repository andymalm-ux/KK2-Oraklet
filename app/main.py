from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.chain.pipeline import create_csv_chain
from app.chain.steps import SmolLM

@asynccontextmanager
async def lifespan(app: FastAPI):

    llm = SmolLM()

    app.state.llm = llm
    app.state.csv_chain = create_csv_chain(llm)

    app.state.csv_data = []

    yield


app = FastAPI(lifespan=lifespan)

from .data import router as data_router
from .chain.steps import router as steps_router

app.include_router(data_router)
app.include_router(steps_router)