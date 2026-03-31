"""
LLM models module supporting multiple providers:
- OpenAI (GPT-4, GPT-3.5-turbo, etc.)
- Groq (Llama, Mixtral, etc.)
- Google Gemini
"""

import os
import sys
import logging
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from config.config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    GROQ_API_KEY,
    GROQ_MODEL,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    DEFAULT_LLM_PROVIDER,
    TEMPERATURE,
    MAX_TOKENS,
)

logger = logging.getLogger(__name__)


class LLMFactory:
    """Factory class to create LLM instances"""
    
    @staticmethod
    def create_llm(provider: str = None, model: str = None, temperature: float = None, max_tokens: int = None):
        """
        Create an LLM instance based on provider
        
        Args:
            provider: LLM provider (openai, groq, gemini)
            model: Specific model name
            temperature: Temperature for generation (0.0-1.0)
            max_tokens: Maximum tokens for response
            
        Returns:
            LLM instance
        """
        provider = (provider or DEFAULT_LLM_PROVIDER).lower()
        temperature = temperature if temperature is not None else TEMPERATURE
        max_tokens = max_tokens or MAX_TOKENS
        
        try:
            if provider == "openai":
                return LLMFactory._create_openai(model, temperature, max_tokens)
            elif provider == "groq":
                return LLMFactory._create_groq(model, temperature, max_tokens)
            elif provider == "gemini":
                return LLMFactory._create_gemini(model, temperature, max_tokens)
            else:
                logger.warning(f"Unknown provider: {provider}. Defaulting to Groq.")
                return LLMFactory._create_groq(model, temperature, max_tokens)
        
        except Exception as e:
            logger.error(f"Failed to create LLM instance: {str(e)}")
            raise
    
    @staticmethod
    def _create_openai(model: str = None, temperature: float = None, max_tokens: int = None):
        """Create OpenAI LLM instance"""
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured")
        
        model = model or OPENAI_MODEL
        logger.info(f"Initializing OpenAI model: {model}")
        
        return ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    
    @staticmethod
    def _create_groq(model: str = None, temperature: float = None, max_tokens: int = None):
        """Create Groq LLM instance"""
        if not GROQ_API_KEY:
            raise ValueError("Groq API key not configured")
        
        model = model or GROQ_MODEL
        logger.info(f"Initializing Groq model: {model}")
        
        return ChatGroq(
            api_key=GROQ_API_KEY,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    
    @staticmethod
    def _create_gemini(model: str = None, temperature: float = None, max_tokens: int = None):
        """Create Google Gemini LLM instance"""
        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key not configured")
        
        model = model or GEMINI_MODEL
        logger.info(f"Initializing Gemini model: {model}")
        
        return ChatGoogleGenerativeAI(
            api_key=GEMINI_API_KEY,
            model=model,
            temperature=temperature,
            convert_system_message_to_human=True,
        )


def get_llm(provider: str = None, model: str = None, temperature: float = None, max_tokens: int = None):
    """
    Get an LLM instance
    
    Args:
        provider: LLM provider
        model: Model name
        temperature: Generation temperature
        max_tokens: Max tokens
        
    Returns:
        LLM instance
    """
    return LLMFactory.create_llm(provider, model, temperature, max_tokens)


def get_chatgroq_model():
    """Initialize and return the Groq chat model (backward compatibility)"""
    return LLMFactory._create_groq()