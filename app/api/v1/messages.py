from fastapi import APIRouter, HTTPException, Path, status
from pydantic import BaseModel, Field
from datetime import datetime

from ...models.store import SESSION_STORE, Message

router = APIRouter()

class MessageRequest(BaseModel):
    role: str = Field(pattern="^(user|assistant|system)$")
    content: str = Field(min_length=1)

@router.get("/", status_code=status.HTTP_200_OK, response_model=None)
async def read_session_messages(session_id: int = Path(gt=0)):
    for data in SESSION_STORE:
        if data.session.id == session_id:
            return data.messages

    raise HTTPException(status_code=404, detail='Session not found.')

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def add_message_to_session(session_id: int = Path(gt=0), message: MessageRequest = None):
    for data in SESSION_STORE:
        if data.session.id == session_id:
            new_message: Message = Message(
                role=message.role,
                content=message.content,
                timestamp=datetime.now().isoformat()
            )
            data.messages.append(new_message)
            return new_message

    raise HTTPException(status_code=404, detail='Session not found.')
