from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
import os
from typing import Tuple, List
from dotenv import load_dotenv

load_dotenv()


class RAGEngine:
    """
    Core RAG (Retrieval-Augmented Generation) engine using llama_index.
    This class handles document ingestion, indexing, and query processing.
    """
    
    def __init__(self):
        """
        Initialize the RAG engine by setting up the document index.
        """
        # Load OpenAI API key from environment variable
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        model = os.getenv("OPENAI_MODEL", "gpt-4o")
        temperature = float(os.getenv("OPENAI_TEMPERATURE", 0.7))

        # Initialize the LLM
        self.llm = OpenAI(temperature=temperature, model=model)
        
        # # Create service context
        # self.service_context = ServiceContext.from_defaults(llm=self.llm)
        
        # # Create initial index
        # self.refresh_index()
    
    def refresh_index(self):
        """
        (Re)build the document index by processing all documents in the data directory.
        """
        # Load documents from the data directory
        documents = SimpleDirectoryReader('../data').load_data()
        
        # Create vector store index
        self.index = VectorStoreIndex.from_documents(
            documents,
            service_context=self.service_context
        )
    
    def process_query(self, msg_list: List[Tuple[str, bool]]) -> Tuple[str, List[str]]:
        """
        Process a user query using RAG with the provided chat history.
        """
        messages = [
            ChatMessage(role="system", content="You are a helpful AI assistant"),
        ]
        for msg in msg_list:
            role = "user" if msg[1] else "assistant"
            messages.append(ChatMessage(role=role, content=msg[0]))
        resp = OpenAI().chat(messages)        
        return resp.message.content.strip(), []

        # Create query engine
        query_engine = self.index.as_query_engine()
        
        # Get response
        response = query_engine.query(query)
        
        # Extract source documents
        sources = [
            node.node.get_content()[:100] + "..."  # First 100 chars of each source
            for node in response.source_nodes
        ]
        
        return str(response), sources 