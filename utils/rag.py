"""
RAG (Retrieval-Augmented Generation) utilities for document processing,
embedding, and semantic search.
"""

import os
import sys
import logging
from typing import List, Tuple, Dict
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
except ImportError:
    RecursiveCharacterTextSplitter = None
    FAISS = None

from config.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    VECTOR_DB_PATH,
    DOCUMENTS_PATH,
    TOP_K_DOCUMENTS,
    SIMILARITY_THRESHOLD,
)
from models.embeddings import get_embedding_model

logger = logging.getLogger(__name__)

class RAGSystem:
    """Handles document ingestion, embedding, and retrieval for RAG"""
    
    def __init__(self):
        """Initialize the RAG system"""
        self.embedding_model = get_embedding_model()
        self.vector_store = None
        self.documents = []
        self._load_vector_store()
    
    def _load_vector_store(self):
        """Load existing vector store or create new one"""
        try:
            if os.path.exists(VECTOR_DB_PATH):
                self.vector_store = FAISS.load_local(
                    VECTOR_DB_PATH,
                    embeddings=self.embedding_model.model,
                    allow_dangerous_deserialization=True
                )
                logger.info(f"Loaded existing vector store from {VECTOR_DB_PATH}")
            else:
                logger.info("No existing vector store found. Will create one on first document ingestion.")
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            self.vector_store = None
    
    def ingest_documents(self, file_paths: List[str]) -> Dict:
        """
        Ingest documents from file paths
        
        Args:
            file_paths: List of file paths to ingest
            
        Returns:
            Dictionary with ingestion results
        """
        results = {
            "total_files": len(file_paths),
            "successful": 0,
            "failed": 0,
            "errors": []
        }
        
        try:
            all_chunks = []
            
            for file_path in file_paths:
                try:
                    chunks = self._load_and_split_document(file_path)
                    if chunks:
                        all_chunks.extend(chunks)
                        results["successful"] += 1
                        logger.info(f"Successfully ingested {file_path}")
                except Exception as e:
                    results["failed"] += 1
                    error_msg = f"Error ingesting {file_path}: {str(e)}"
                    results["errors"].append(error_msg)
                    logger.error(error_msg)
            
            # Create or update vector store
            if all_chunks:
                if self.vector_store is None:
                    self.vector_store = FAISS.from_documents(
                        all_chunks,
                        embedding=self.embedding_model.model
                    )
                else:
                    # Add new documents to existing store
                    self.vector_store.add_documents(all_chunks)
                
                # Save vector store
                os.makedirs(VECTOR_DB_PATH, exist_ok=True)
                self.vector_store.save_local(VECTOR_DB_PATH)
                logger.info(f"Vector store saved to {VECTOR_DB_PATH}")
        
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            results["errors"].append(f"Vector store creation error: {str(e)}")
        
        return results
    
    def _load_and_split_document(self, file_path: str) -> List:
        """
        Load and split a document into chunks
        
        Args:
            file_path: Path to the document
            
        Returns:
            List of document chunks
        """
        try:
            from langchain_core.documents import Document
            
            # Read file content
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif file_extension == '.pdf':
                try:
                    from PyPDF2 import PdfReader
                    with open(file_path, 'rb') as f:
                        pdf_reader = PdfReader(f)
                        content = ""
                        for page_num in range(len(pdf_reader.pages)):
                            page = pdf_reader.pages[page_num]
                            content += page.extract_text()
                except ImportError:
                    logger.warning("PyPDF2 not installed. Skipping PDF processing.")
                    return []
            else:
                logger.warning(f"Unsupported file format: {file_extension}")
                return []
            
            # Split text into chunks
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP,
            )
            
            chunks_text = splitter.split_text(content)
            
            # Create Document objects with metadata
            documents = [
                Document(
                    page_content=chunk,
                    metadata={
                        "source": file_path,
                        "chunk_index": i
                    }
                )
                for i, chunk in enumerate(chunks_text)
            ]
            
            logger.info(f"Split {file_path} into {len(documents)} chunks")
            return documents
        
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {str(e)}")
            raise
    
    def retrieve_relevant_chunks(self, query: str, k: int = None) -> List[Tuple[str, float]]:
        """
        Retrieve relevant document chunks based on query
        
        Args:
            query: Query string
            k: Number of results to retrieve (uses TOP_K_DOCUMENTS from config if not specified)
            
        Returns:
            List of tuples (chunk_text, similarity_score)
        """
        try:
            if self.vector_store is None:
                logger.warning("Vector store not initialized. No documents available for retrieval.")
                return []
            
            k = k or TOP_K_DOCUMENTS
            
            # Perform similarity search with scores
            results = self.vector_store.similarity_search_with_score(query, k=k)
            
            # Filter by similarity threshold
            filtered_results = [
                (doc.page_content, 1 - score)  # Convert distance to similarity
                for doc, score in results
                if (1 - score) >= SIMILARITY_THRESHOLD
            ]
            
            logger.info(f"Retrieved {len(filtered_results)} relevant chunks for query")
            return filtered_results
        
        except Exception as e:
            logger.error(f"Error retrieving relevant chunks: {str(e)}")
            return []
    
    def format_context(self, chunks: List[Tuple[str, float]]) -> str:
        """
        Format retrieved chunks into a context string for the LLM
        
        Args:
            chunks: List of (chunk_text, similarity_score) tuples
            
        Returns:
            Formatted context string
        """
        if not chunks:
            return "No relevant documents found."
        
        context = "**Relevant Information from Documents:**\n\n"
        for i, (chunk, score) in enumerate(chunks, 1):
            context += f"**Source {i}** (Relevance: {score:.2%})\n{chunk}\n\n"
        
        return context
    
    def clear_vector_store(self):
        """Clear the vector store"""
        try:
            if os.path.exists(VECTOR_DB_PATH):
                import shutil
                shutil.rmtree(VECTOR_DB_PATH)
            self.vector_store = None
            logger.info("Vector store cleared")
        except Exception as e:
            logger.error(f"Error clearing vector store: {str(e)}")


def get_rag_system() -> RAGSystem:
    """Factory function to get RAG system instance"""
    return RAGSystem()
