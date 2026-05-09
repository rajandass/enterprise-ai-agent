import uuid
from datetime import datetime

from db.cosmos_client import (
    container,
    session_container
)


def save_message(
    session_id: str,
    role: str,
    content: str,
    citations=None
):
    item = {
        "id": str(uuid.uuid4()),
        "session_id": session_id,
        "role": role,
        "content": content,
        "citations": citations or [],
        "created_at": datetime.utcnow().isoformat()
    }

    container.create_item(body=item)

    return item

def get_conversation(session_id: str):
    query = """
    SELECT * FROM c
    WHERE c.session_id = @session_id
    ORDER BY c.created_at ASC
    """

    parameters = [
        {
            "name": "@session_id",
            "value": session_id
        }
    ]

    items = list(
        container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        )
    )

    return items

def list_conversations():
    query = """
    SELECT *
    FROM c
    ORDER BY c.created_at DESC
    """

    items = list(
        session_container.query_items(
            query=query,
            enable_cross_partition_query=True
        )
    )

    return items

def create_chat_session(
    session_id: str,
    title: str
):
    item = {
        "id": session_id,
        "session_id": session_id,
        "title": title,
        "created_at": datetime.utcnow().isoformat()
    }

    session_container.upsert_item(item)

    return item

def generate_title(query: str):
    words = query.split()

    return " ".join(words[:5])