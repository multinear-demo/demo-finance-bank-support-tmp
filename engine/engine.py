# pyright: reportMissingImports=false
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
import os
from typing import Tuple, List
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


class RAGEngine:
    """
    Core RAG (Retrieval-Augmented Generation) engine using llama_index.
    This class handles document ingestion, indexing, and query processing.
    """

    temperature = 0.2
    model = "gpt-4o"

    def __init__(self):
        """
        Initialize the RAG engine by setting up the document index.
        """
        # Load OpenAI API key from environment variable
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", 0.2))

        # Initialize the LLM
        # self.llm = OpenAI(temperature=temperature, model=model)
        from llama_index.core import Settings
        Settings.llm = OpenAI(temperature=self.temperature, model=self.model)
        # print(Settings.llm._get_client())
        # logfire.instrument_openai(Settings.llm._client)

        if os.getenv("TRACE_LOGFIRE", False):
            import logfire
            logfire.configure()
            logfire.instrument_openai(Settings.llm._get_client())

        # # Create service context
        # self.service_context = ServiceContext.from_defaults(llm=self.llm)

        # # Create initial index
        # self.refresh_index()

    def refresh_index(self):
        """
        (Re)build the document index by processing all documents in the data directory.
        """
        # Load documents from the data directory
        # documents = SimpleDirectoryReader('../data').load_data()

        # # Create vector store index
        # self.index = VectorStoreIndex.from_documents(
        #     documents,
        #     service_context=self.service_context
        # )

        # https://docs.llamaindex.ai/en/stable/examples/usecases/10k_sub_question/
        # lyft_docs = SimpleDirectoryReader(input_files=["./data/10k/lyft_2021.pdf"]).load_data()
        # uber_docs = SimpleDirectoryReader(input_files=["./data/10k/uber_2021.pdf"]).load_data()
        # self.lyft_index = VectorStoreIndex.from_documents(lyft_docs)
        # self.uber_index = VectorStoreIndex.from_documents(uber_docs)

        # bank_docs = SimpleDirectoryReader(input_files=["./data/bank_kiwi_faq.txt"]).load_data()

        # Get the path relative to the current file
        bank_docs = SimpleDirectoryReader(
            input_files=[str(Path(__file__).parent.parent / "data" / "acme_bank_faq.txt")]
        ).load_data()

        self.bank_index = VectorStoreIndex.from_documents(bank_docs)

        # Create vector store index
        # self.index = VectorStoreIndex.from_documents(
        #     lyft_docs + uber_docs,
        #     service_context=self.service_context
        # )

    async def process_query(self, msg_list: List[Tuple[str, bool]]) -> Tuple[str, List[str]]:
        """
        Process a user query using RAG with the provided chat history.
        """
        try:
            # lyft_engine = self.lyft_index.as_query_engine(similarity_top_k=3)
            # uber_engine = self.uber_index.as_query_engine(similarity_top_k=3)
            # query_engine_tools = [
            #     QueryEngineTool(
            #         query_engine=lyft_engine,
            #         metadata=ToolMetadata(
            #             name="lyft_10k",
            #             description=(
            #                 "Provides information about Lyft financials for year 2021"
            #             ),
            #         ),
            #     ),
            #     QueryEngineTool(
            #         query_engine=uber_engine,
            #         metadata=ToolMetadata(
            #             name="uber_10k",
            #             description=(
            #                 "Provides information about Uber financials for year 2021"
            #             ),
            #         ),
            #     ),
            # ]

            bank_engine = self.bank_index.as_query_engine(similarity_top_k=3)
            query_engine_tools = [
                QueryEngineTool(
                    query_engine=bank_engine,
                    metadata=ToolMetadata(
                        name="bank_faq",
                        description=(
                            "Provides information about Bank FAQ"
                        ),
                    ),
                ),
            ]

            s_engine = SubQuestionQueryEngine.from_defaults(
                query_engine_tools=query_engine_tools
            )
            response = await s_engine.aquery(msg_list[-1][0])  # last user message
            return str(response), []
        except Exception as e:
            print(e)
            return "Error processing request. Try again.", []

        # ------------------------------------------------------------------------
        messages = [
            ChatMessage(role="system", content="You are a helpful AI assistant"),
        ]
        for msg in msg_list:
            role = "user" if msg[1] else "assistant"
            messages.append(ChatMessage(role=role, content=msg[0]))
        resp = self.llm.chat(messages)        
        return resp.message.content.strip(), []

        # ------------------------------------------------------------------------
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
