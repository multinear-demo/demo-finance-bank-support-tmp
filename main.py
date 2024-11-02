from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

from engine import RAGEngine


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

# Schemas
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    sources: List[str]

@app.post("/api/chat", response_model=ChatResponse, tags=["chat"])
async def chat(body: ChatMessage):
    """
    Process a chat message using RAG and return the response with sources.
    """
    try:
        import asyncio; await asyncio.sleep(1) # wait 1 second
        response = "This is a mock response from the real AI."
        sources = ["source1", "source2"]

        # if random 50%, return error
        # import random
        # if random.random() < 0.5:
        #     raise Exception("Random error")
        # response, sources = rag_engine.process_query(message.message)
        return ChatResponse(response=response, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/refresh-index", tags=["chat"])
async def refresh_index():
    """
    Refresh the document index by reprocessing all documents in the data directory.
    """
    try:
        rag_engine.refresh_index()
        return {"status": "success", "message": "Index refreshed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files (frontend)
app.mount("/", StaticFiles(directory="./static", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
