from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

from engine import RAGEngine
from session import SessionManager


app = FastAPI(title="RAG Chat Application")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG engine (singleton)
rag_engine = RAGEngine()

# Initialize SessionManager (singleton)
session_manager = SessionManager()

# Schemas
class NewChatMessage(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    response: str
    sources: List[str]

@app.post("/api/chat", response_model=ChatResponse, tags=["chat"])
async def chat(body: NewChatMessage):
    """
    Process a chat message using RAG and return the response with sources.
    """
    # Add user's message
    user_message = (body.message, True)
    session_manager.add_message(body.session_id, user_message)

    # Retrieve session history
    msg_list = session_manager.get_history(body.session_id)

    # Process the query using RAG engine with history
    response, sources = rag_engine.process_query(msg_list)
    
    # Add AI's response
    ai_message = (response, False)
    session_manager.add_message(body.session_id, ai_message)
    
    return ChatResponse(response=response, sources=sources)

@app.post("/api/refresh-index", tags=["chat"])
async def refresh_index():
    """
    Refresh the document index by reprocessing all documents in the data directory.
    """
    rag_engine.refresh_index()
    return {"status": "success", "message": "Index refreshed successfully"}

@app.get("/api/get-history", tags=["chat"])
async def get_history(session_id: str):
    """
    Retrieve the chat history for a given session.
    """
    history = session_manager.get_history(session_id)
    return history

# Mount static files (frontend)
app.mount("/", StaticFiles(directory="./static", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 
