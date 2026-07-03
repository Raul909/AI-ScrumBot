import os
from typing import Optional
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

class ChromaManager:
    """
    ChromaManager singleton wrapping langchain_chroma.
    """
    _instance: Optional['ChromaManager'] = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ChromaManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self, persist_directory: str = "./chroma_db"):
        if self._initialized:
            return
            
        self.persist_directory = persist_directory
        # Defaulting to OpenAI embeddings, could be configurable
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        self._initialized = True
        
    def get_vectorstore(self) -> Chroma:
        """Returns the Chroma vectorstore instance."""
        return self.vectorstore
