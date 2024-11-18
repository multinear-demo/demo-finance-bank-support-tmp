import sys
from pathlib import Path


# Add parent directory to Python path so we can import engine
sys.path.append(str(Path(__file__).parent.parent))
from engine.engine import RAGEngine

# Singleton instance
_rag_engine = None

def get_rag_engine():
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGEngine()
        _rag_engine.refresh_index()
    return _rag_engine

def run_single(input: str, *args, **kwargs) -> str:
    engine = get_rag_engine()
    import asyncio
    response, _ = asyncio.run(engine.process_query([(input, True)]))
    return response
