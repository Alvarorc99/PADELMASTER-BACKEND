"""Main file that defines the endpoint to connect the backend with the frontend"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.config.config import *
from src.prompt import *
from src.qa import *

app = FastAPI()

class UserQuery(BaseModel):
    user_query: str
    conversation: list[dict] = Field(default=[])

@app.post("/query")
async def ask_chatbot(request: UserQuery):
    try:
        logger.info("Full request received: %s", request)
        logger.info(f"Query received: {request.user_query}")
        logger.info("Conversation: %s", request.conversation)
        response = get_qa(request.user_query, request.conversation)
        if response.get("answer"):
            return response
        else:
            raise HTTPException(status_code=404, detail="No se encontraron resultados")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la consulta: {e}")