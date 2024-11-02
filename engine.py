from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms.openai import OpenAI
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
            
        # Initialize the LLM
        # self.llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")
        
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
    
    def process_query(self, query: str) -> Tuple[str, List[str]]:
        """
        Process a user query using RAG.
        
        Args:
            query (str): User's question or message
            
        Returns:
            Tuple[str, List[str]]: Tuple containing (response text, list of source documents)
        """
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