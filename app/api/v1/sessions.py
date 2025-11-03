from fastapi import APIRouter, Path, HTTPException
from starlette import status
from pydantic import BaseModel, Field
from datetime import datetime

from ...models.store import SESSION_STORE, SessionData, DataStore
from .messages import router as messages_router

router = APIRouter(
    prefix='/sessions',
)

router.include_router(messages_router, tags=['messages'], prefix='/{session_id}/messages')

class SessionRequest(BaseModel):
    session_user: str = Field(min_length=3)

@router.get("/{session_id}", status_code=status.HTTP_200_OK, response_model=None)
async def read_session(session_id: int = Path(gt=0)) -> SessionData:
    if not SESSION_STORE:
        raise HTTPException(status_code=404, detail='No sessions found.')

    for data in SESSION_STORE:
        if data.session.id == session_id:
            return data.session

    raise HTTPException(status_code=404, detail='Session not found.')


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_session(session_request: SessionRequest):
    session_id = SESSION_STORE[-1].session.id if SESSION_STORE else 0
    session_data = SessionData(
        id=session_id + 1,
        session_user=session_request.session_user,
        created_at=datetime.now().isoformat()
    )
    data_store = DataStore(session=session_data)
    SESSION_STORE.append(data_store)

    return session_data
