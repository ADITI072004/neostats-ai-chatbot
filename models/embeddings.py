"""
Embedding models for RAG (Retrieval-Augmented Generation).
Supports multiple embedding providers: HuggingFace, OpenAI, and Cohere.
"""

import os
import sys
from typing import List
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_openai import OpenAIEmbeddings
except ImportError:
    HuggingFaceEmbeddings = None
    OpenAIEmbeddings = None

from config.config import (
    EMBEDDING_MODEL_PROVIDER,
    EMBEDDING_MODEL_NAME,
    OPENAI_API_KEY,
)

logger = logging.getLogger(__name__)

class EmbeddingModel:
    """Wrapper class for embedding models"""
    
    def __init__(self, provider: str = None, model_name: str = None):
        """
        Initialize embedding model based on provider
        
        Args:
            provider: The embedding provider (huggingface, openai, etc.)
            model_name: The specific model name to use
        """
        self.provider = provider or EMBEDDING_MODEL_PROVIDER
        self.model_name = model_name or EMBEDDING_MODEL_NAME
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the embedding model based on provider"""
        try:
            if self.provider.lower() == "openai":
                if not OPENAI_API_KEY:
                    logger.warning("OpenAI API key not found. Falling back to HuggingFace")
                    self.provider = "huggingface"
                else:
                    self.model = OpenAIEmbeddings(
                        api_key=OPENAI_API_KEY,
                        model=self.model_name
                    )
                    logger.info(f"Initialized OpenAI embeddings with model: {self.model_name}")
            
            if self.model is None:  # Default or fallback to HuggingFace
                if HuggingFaceEmbeddings is None:
                    raise ImportError("HuggingFaceEmbeddings requires langchain-huggingface")
                
                self.model = HuggingFaceEmbeddings(model_name=self.model_name)
                logger.info(f"Initialized HuggingFace embeddings with model: {self.model_name}")
        
        except Exception as e:
            logger.error(f"Failed to initialize embedding model: {str(e)}")
            raise
    
    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """
        Embed multiple documents
        
        Args:
            documents: List of documents to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            return self.model.embed_documents(documents)
        except Exception as e:
            logger.error(f"Error embedding documents: {str(e)}")
            raise
    
    def embed_query(self, query: str) -> List[float]:
        """
        Embed a single query
        
        Args:
            query: Query string to embed
            
        Returns:
            Embedding vector
        """
        try:
            return self.model.embed_query(query)
        except Exception as e:
            logger.error(f"Error embedding query: {str(e)}")
            raise


def get_embedding_model(provider: str = None, model_name: str = None) -> EmbeddingModel:
    """
    Factory function to get an embedding model
    
    Args:
        provider: The embedding provider
        model_name: The specific model name
        
    Returns:
        EmbeddingModel instance
    """
    return EmbeddingModel(provider=provider, model_name=model_name)
