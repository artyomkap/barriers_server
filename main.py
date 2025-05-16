from asyncio import tasks

import uvicorn
from fastapi import FastAPI

from api import deals, clients, task, report
from api.routers import router as api_router
from database.connect import engine
from database.models import Base
import asyncio
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import HTTPException as FastAPIHTTPException

load_dotenv()

app = FastAPI(title="FastAPI with Aiogram and SQLAlchemy")


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(api_router, prefix="/api")
app.include_router(clients.router, prefix="/api")
app.include_router(deals.router, prefix="/api")
app.include_router(task.router, prefix="/api")
app.include_router(report.router, prefix="/api")

origins = [
    "https://barriers-services.ru"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI(
    title="FastAPI with Aiogram and SQLAlchemy",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)




# Aiogram startup
@app.on_event("startup")
async def startup_event():
    await init_models()


@app.exception_handler(FastAPIHTTPException)
async def custom_http_exception_handler(request: Request, exc: FastAPIHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
