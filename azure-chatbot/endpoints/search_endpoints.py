from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from services.search_service import SearchService
from models.search_result import SearchResult

router = APIRouter(prefix="/search", tags=["Search"])


def get_search_service() -> SearchService:
    return SearchService()


from fastapi import APIRouter, Query, Depends, HTTPException
from typing import List
import logging
router = APIRouter(prefix="/search", tags=["search"])
logger = logging.getLogger(__name__)


@router.get(
    "/keyword",
    summary="Keyword Search",
    description="Perform a full-text keyword search across indexed PDF blob data.",
    # NOTE: Ensure SearchResult, SearchService, and get_search_service are imported
    response_model=List[SearchResult], 
    response_description="A list of search results containing file details and snippets.",
    responses={
        200: {
            "description": "Successful search",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "fileName": "invoice001.pdf",
                            "blobPath": "https://.../invoice001.pdf",
                            "contentSnippet": "Invoice ID: invoice001 Customer: Oliver Taylor...",
                            "customer": "Oliver Taylor",
                            "location": "Birmingham, UK",
                            "phone": "+44-121-496-0033",
                            "description": "Payment for office supplies and equipment."
                        }
                    ]
                }
            },
        },
        400: {"description": "Invalid query parameters"},
        500: {"description": "Internal server error"},
    },
)
async def keyword_search(
    query: str = Query(..., description="Keyword to search"),
    top: int = Query(10, ge=1, le=50, description="Number of results to return"),
    # NOTE: Assuming SearchService and get_search_service are available globally or imported
    service: SearchService = Depends(get_search_service), 
):
    """
    Executes the keyword search via the SearchService and handles errors.
    """
    try:
        # This calls the fixed search_keyword method
        return await service.search_keyword(query=query, top=top)
    
    except RuntimeError as e:
        logger.error(f"Search endpoint failed for query '{query}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to execute Azure Search query: {e}"
        )
    except Exception as e:
        # Catch any other unexpected error
        logger.exception(f"An unexpected error occurred in keyword_search for query '{query}'.")
        raise HTTPException(
            status_code=500,
            detail="An unexpected internal server error occurred."
        )


@router.get(
    "/semantic",
    summary="Semantic Search",
    description="Perform a semantic search with improved ranking and extractive captions.",
    response_model=List[SearchResult],
    responses={
        200: {"description": "Search results with semantic ranking"},
        400: {"description": "Invalid request"},
        500: {"description": "Internal server error"},
    },
)
async def semantic_search(
    query: str,
    top: int = 10,
    service: SearchService = Depends(get_search_service),
):
    return await service.search_semantic(query=query, top=top)


@router.get(
    "/filter",
    summary="Filtered Search",
    description="Perform a keyword search with optional filters for id or blobName.",
    response_model=List[SearchResult],
    responses={
        200: {"description": "Filtered search results"},
        400: {"description": "Invalid filter parameters"},
        500: {"description": "Internal server error"},
    },
)
async def filtered_search(
    query: Optional[str] = Query("", description="Keyword to search; leave empty to filter only"),
    id: Optional[str] = Query(None, description="Filter by exact document ID"),
    blob_name: Optional[str] = Query(None, description="Filter by exact blobName"),
    top: int = Query(10, ge=1, le=50, description="Number of results to return"),
    service: SearchService = Depends(get_search_service),
):
    """
    Perform a full-text search with optional exact-match filters on id or blobName.
    If query is empty, the search will only apply filters.
    """
    return await service.search_with_filter(query=query, id=id, blob_name=blob_name, top=top)


@router.get(
    "/suggest",
    summary="Autocomplete / Typeahead Suggestions",
    description=(
        "Retrieve typeahead suggestions from the search index based on a partial query. "
        "Suggestions are drawn from `blobName` and `description` fields of the indexed documents. "
        "Empty or None suggestions are automatically filtered out."
    ),
    response_model=List[str],
    response_description="List of suggested document names or descriptions",
    responses={
        200: {
            "description": "Successfully retrieved suggestions",
            "content": {
                "application/json": {
                    "example": ["invoice001.pdf", "invoice002.pdf", "Payment details"]
                }
            },
        },
        400: {"description": "Invalid query parameter"},
        500: {"description": "Internal server error while fetching suggestions"},
    },
)
async def suggest(
    query: str = Query(
        ..., 
        min_length=1, 
        description="Partial search term for typeahead suggestions"
    ),
    top: int = Query(
        5, 
        ge=1, 
        le=20, 
        description="Maximum number of suggestions to return"
    ),
    service: SearchService = Depends(get_search_service),
) -> List[str]:
    """
    Perform a typeahead suggestion query against the search index.
    
    Args:
        query (str): Partial search term to match indexed documents.
        top (int, optional): Limit on the number of suggestions returned. Defaults to 5.
        service (SearchService): Search service dependency.
    
    Returns:
        List[str]: A list of suggested terms (document names or descriptions).
    """
    return await service.suggest(query=query, top=top)