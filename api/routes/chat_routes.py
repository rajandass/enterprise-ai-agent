
from unittest import result
import uuid
from fastapi import(
    APIRouter,
    Depends
      )
from api.dependencies.auth import (
    verify_api_key
)

from fastapi import Request
from fastapi.responses import StreamingResponse
from api.schemas.chat_schema import QueryRequest
import logging

logger = logging.getLogger(__name__)

from services.conversation_service import (
    save_message,
    get_conversation,
    list_conversations,
    create_chat_session,
    generate_title
)

from pipelines.query import (
    ask_question,
    stream_answer
)
from api.dependencies.rate_limiter import (
    limiter
)


router = APIRouter()

from services.response.api_response_service import (
    success_response
)

@router.post("/ask"
          )
@limiter.limit("5/minute")
def ask(
    request: Request,
    req: QueryRequest,
    api_key: str = Depends(
        verify_api_key
    )
):
    logger.info("chat_request_received")
    request_id = str(uuid.uuid4())
    result = ask_question(req.query)
    session_id = req.session_id
    logger.info( f"chat_request session_id={req.session_id}")
    
    create_chat_session(
    session_id=session_id,
    title=generate_title(req.query)
    )

    save_message(
        session_id=session_id,
        role="user",
        content=req.query
    )

    save_message(
        session_id=session_id,
        role="assistant",
        content=result["answer"],
        citations=result.get("citations", [])
    )
    
    return success_response(result)

@router.post("/ask-stream"
          )
@limiter.limit("5/minute")
def ask_stream(
    request: Request,
    req: QueryRequest,
    api_key: str = Depends(verify_api_key)
):

    return StreamingResponse(
        stream_answer(req.query),
        media_type="text/plain"
    )

@router.get("/conversations/{session_id}")
def get_conversation_history(
    session_id: str,
     api_key: str = Depends(verify_api_key)
):
    messages = get_conversation(session_id)

    return success_response({
        "session_id": session_id,
        "messages": messages
    })

@router.get("/conversations")
def get_conversations(
    api_key: str = Depends(verify_api_key)
):
    conversations = list_conversations()

    return success_response({
        "conversations": conversations
    })