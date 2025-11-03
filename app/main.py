from fastapi import FastAPI
from .api.v1.sessions import router as sessions_router

app = FastAPI(
    title='Session Management API',
)

app.include_router(sessions_router)
