import logging
from typing import List, Optional, Any, Dict
from azure.search.documents.aio import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from env.config import settings
from models.search_result import SearchResult 
from azure.search.documents.models import QueryType

logger = logging.getLogger(__name__)

class SearchService:
    """Search service for PDF blobs in Azure Cognitive Search."""

    def __init__(self):
        # NOTE: The client is initialized here but is an instance of SearchClient, 
        # which is an async context manager and handles connections internally.
        self.client = SearchClient(
            endpoint=settings.AZURE_SEARCH_ENDPOINT,
            index_name=settings.AZURE_SEARCH_INDEX_NAME,
            credential=AzureKeyCredential(settings.AZURE_SEARCH_KEY),
            connection_timeout=45  # 45 seconds timeou
        )
        self.index_name = settings.AZURE_SEARCH_INDEX_NAME

    async def search_keyword(self, query: str, top: int = 10) -> List[SearchResult]:
        """Perform full-text keyword search using the helper."""
        # This function is now just a clean wrapper for the helper.
        return await self._execute_search(query=query, top=top)

    async def search_semantic(self, query: str, top: int = 10):
        results = []
        async with self.client:
            response = await self.client.search(
                search_text=query,
                top=top,
                query_type= QueryType.SEMANTIC,
                semantic_configuration_name="default"  # must match your index config
            )
            async for r in response:
                results.append(
                    SearchResult(
                        fileName=r.get("fileName"),
                        blobPath=r.get("blobPath"),
                        contentSnippet=(r.get("content") or "")[:500],
                        description=r.get("description")
                    )
                )
        return results
    

    async def suggest(self, query: str, top: int = 5) -> List[str]:
        try:
            results = await self.client.suggest(
                search_text=query,
                suggester_name="sg",
                top=top
            )

            suggestions = []
            for item in results:
                # Each item is a dict with "text" field
                text = item.get("text")
                if text:
                    suggestions.append(text)

            return suggestions

        except AzureError as e:
            logger.error("Suggest query failed: %s", e)
            return []
        except Exception as e:
            logger.error("Unexpected error in suggest: %s", e)
            return []


    async def search_with_filter(
        self,
        query: str,
        top: int = 10,
        id: Optional[str] = None,
        blob_name: Optional[str] = None,
    ) -> List[SearchResult]:
        """Perform full-text keyword search with optional filters on id or blobName."""

        filters = []

        # Only filter on fields that are filterable
        if id:
            filters.append(f"id eq '{id}'")
        if blob_name:
            filters.append(f"blobName eq '{blob_name}'")

        filter_string = " and ".join(filters) if filters else None

        return await self._execute_search(
            query=query,
            filter=filter_string,
            top=top
        )

    async def _execute_search(self, query: str, top: int = 10, **kwargs: Any) -> List[SearchResult]:
        """Helper to execute search with error handling and correct async logic."""
        results: List[SearchResult] = []
        
        select_fields = ["blobName", "blobPath", "content", "description"]

        try:
            # Use async with for robust connection management
            async with self.client:
                results_iter = await self.client.search(
                    search_text=query, 
                    top=top, 
                    select=select_fields, # Use the select fields list
                    **kwargs
                )
                
                # Now use async for on the awaited iterator
                async for r in results_iter:
                    # NOTE: Ensure the fields (customer, location, phone) exist in your index.
                    # Use .get() with a default value to prevent TypeErrors if they are missing.
                    results.append(
                        SearchResult(
                            fileName=r.get("blobName"),
                            blobPath=r.get("blobPath"),
                            contentSnippet=(r.get("content") or "")[:500], 
                            # TODO: customer=r.get("customer"),
                            # location=r.get("location"),
                            # phone=r.get("phone"),
                            description=r.get("description"),
                        )
                    )
        except AzureError as e:
            logger.error("Search query failed with AzureError: %s", e)
            # Raise the exception so the FastAPI endpoint can catch and return HTTP 500
            raise RuntimeError(f"Azure Search query failed: {e}") 
        except Exception as e:
            logger.error("Search query failed with unexpected error: %s", e)
            raise RuntimeError(f"Search query failed: {e}") 
            
        return results