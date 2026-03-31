"""
Web search utilities for real-time information retrieval.
Supports Google Search API and DuckDuckGo as fallback.
"""

import os
import sys
import logging
from typing import List, Dict, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config.config import GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_ENGINE_ID

logger = logging.getLogger(__name__)

class WebSearcher:
    """Handles web search functionality"""
    
    def __init__(self, use_google: bool = True):
        """
        Initialize web searcher
        
        Args:
            use_google: Whether to use Google Search API (requires API key)
        """
        self.use_google = use_google and GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID
        
        if self.use_google:
            self._init_google_search()
        else:
            self._init_duckduckgo_search()
    
    def _init_google_search(self):
        """Initialize Google Search API"""
        try:
            from googleapiclient.discovery import build
            self.google_service = build(
                "customsearch", "v1",
                developerKey=GOOGLE_SEARCH_API_KEY
            )
            logger.info("Google Search API initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Google Search: {str(e)}. Falling back to DuckDuckGo.")
            self.use_google = False
            self._init_duckduckgo_search()
    
    def _init_duckduckgo_search(self):
        """Initialize DuckDuckGo search as fallback"""
        try:
            import duckduckgo_search
            self.duckduckgo_search = duckduckgo_search
            logger.info("DuckDuckGo search initialized as fallback")
        except ImportError:
            try:
                # Try alternative: requests + beautifulsoup
                import requests
                self.requests = requests
                logger.info("Using requests for search fallback")
            except ImportError:
                logger.error("No search library available. Install duckduckgo-search or requests.")
    
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        Perform web search
        
        Args:
            query: Search query string
            num_results: Number of results to return
            
        Returns:
            List of search results with title and snippet
        """
        try:
            if self.use_google:
                return self._google_search(query, num_results)
            else:
                return self._duckduckgo_search(query, num_results)
        except Exception as e:
            logger.error(f"Web search error: {str(e)}")
            return []
    
    def _google_search(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """
        Perform Google Search
        
        Args:
            query: Search query
            num_results: Number of results
            
        Returns:
            List of search results
        """
        try:
            results = self.google_service.cse().list(
                q=query,
                cx=GOOGLE_SEARCH_ENGINE_ID,
                num=min(num_results, 10),  # Google API max is 10
                gl='us'
            ).execute()
            
            search_results = []
            for item in results.get('items', []):
                search_results.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'source': 'Google'
                })
            
            logger.info(f"Found {len(search_results)} results from Google Search")
            return search_results
        
        except Exception as e:
            logger.error(f"Google Search error: {str(e)}")
            return []
    
    def _duckduckgo_search(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """
        Perform DuckDuckGo search
        
        Args:
            query: Search query
            num_results: Number of results
            
        Returns:
            List of search results
        """
        try:
            if hasattr(self, 'duckduckgo_search'):
                from duckduckgo_search import DDGS
                
                results = []
                with DDGS() as ddgs:
                    for result in ddgs.text(query, max_results=num_results):
                        results.append({
                            'title': result.get('title', ''),
                            'link': result.get('href', ''),
                            'snippet': result.get('body', ''),
                            'source': 'DuckDuckGo'
                        })
                
                logger.info(f"Found {len(results)} results from DuckDuckGo")
                return results
            else:
                return []
        
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {str(e)}")
            return []
    
    def format_search_results(self, results: List[Dict[str, str]]) -> str:
        """
        Format search results into a context string for the LLM
        
        Args:
            results: List of search results
            
        Returns:
            Formatted results string
        """
        if not results:
            return "No relevant web search results found."
        
        context = f"**Recent Web Search Results:**\n\n"
        for i, result in enumerate(results, 1):
            context += f"**Result {i}: {result['title']}**\n"
            context += f"Source: {result.get('source', 'Unknown')}\n"
            context += f"Link: {result.get('link', 'N/A')}\n"
            context += f"Summary: {result.get('snippet', 'N/A')}\n\n"
        
        return context


def get_web_searcher() -> WebSearcher:
    """Factory function to get web searcher instance"""
    return WebSearcher()
