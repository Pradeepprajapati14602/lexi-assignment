"""
Exa.ai integration for web-based template discovery.
Searches the web for similar legal documents when no local match exists.
BONUS FEATURE - Created by UOIONHHC
"""

from exa_py import Exa
from typing import List, Dict, Any, Optional
from app.core.config import settings
import httpx


class ExaService:
    """Service for web template discovery using exa.ai"""
    
    def __init__(self):
        self.client = None
        if settings.EXA_API_KEY:
            self.client = Exa(api_key=settings.EXA_API_KEY)
    
    async def search_legal_templates(
        self,
        query: str,
        num_results: int = 5,
        include_domains: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for legal document templates on the web.
        
        Args:
            query: Search query (e.g., "insurance notice template India")
            num_results: Number of results to return
            include_domains: Optional list of domains to search within
            
        Returns:
            List of search results with content
        """
        if not self.client:
            return []
        
        try:
            # Enhance query for legal documents
            enhanced_query = f"{query} legal document template sample format"
            
            # Search with content retrieval
            search_response = self.client.search_and_contents(
                enhanced_query,
                type="auto",
                num_results=num_results,
                text={
                    "max_characters": settings.EXA_TEXT_LENGTH,
                    "include_html_tags": False
                },
                include_domains=include_domains,
                use_autoprompt=True
            )
            
            # Process results
            results = []
            for result in search_response.results:
                results.append({
                    "title": result.title,
                    "url": result.url,
                    "text": result.text,
                    "score": result.score if hasattr(result, 'score') else None,
                    "published_date": result.published_date if hasattr(result, 'published_date') else None
                })
            
            return results
        
        except Exception as e:
            print(f"Error searching with Exa: {e}")
            return []
    
    async def find_similar_template(
        self,
        user_query: str,
        doc_type: Optional[str] = None,
        jurisdiction: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Find a similar legal template from the web based on user query.
        
        Args:
            user_query: User's drafting request
            doc_type: Type of document (notice, agreement, petition, etc.)
            jurisdiction: Legal jurisdiction (IN, US, UK, etc.)
            
        Returns:
            Best matching web document or None
        """
        # Build search query
        query_parts = [user_query]
        
        if doc_type:
            query_parts.append(doc_type)
        
        if jurisdiction:
            jurisdiction_map = {
                "IN": "India",
                "US": "United States",
                "UK": "United Kingdom",
                "AU": "Australia",
                "CA": "Canada"
            }
            jurisdiction_name = jurisdiction_map.get(jurisdiction, jurisdiction)
            query_parts.append(jurisdiction_name)
        
        query = " ".join(query_parts)
        
        # Search
        results = await self.search_legal_templates(query, num_results=3)
        
        if not results:
            return None
        
        # Return best result
        return results[0]
    
    async def fetch_document_content(self, url: str) -> Optional[str]:
        """
        Fetch raw document content from URL.
        
        Args:
            url: Document URL
            
        Returns:
            Document text content
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                # Basic text extraction (could be enhanced with BeautifulSoup)
                return response.text
        
        except Exception as e:
            print(f"Error fetching document from {url}: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if Exa service is available"""
        return self.client is not None


# Global instance
exa_service = ExaService()
