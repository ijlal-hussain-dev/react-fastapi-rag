from fastapi import APIRouter, Depends, HTTPException
from models.setup_response import SetupResponse
from services.setup_service import SearchSetupService
from env.config import settings

router = APIRouter(prefix="/setup", tags=["Setup"])

@router.post(
    "/create-index",
    summary="Create or Recreate Azure Search Index",
    response_model=SetupResponse,
    response_description="Returns the status of the index creation process"
)
async def setup_index():
    """
    Creates or recreates the Azure Cognitive Search index for PDF blobs.

    - **Fields included**: id, fileName, content, customer, location, phone, description, blobPath
    - **Best Practices**:
        * Returns clear status (`created` or `recreated`)
        * Handles index already exists scenario
    """
    service = SearchSetupService()
    try:
        result = await service.create_index()
        return SetupResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Index creation failed: {str(e)}")


@router.post(
    "/create-all",
    summary="Full Azure Search Setup",
    description=(
        "Performs full setup for Azure Cognitive Search:\n"
        "1. Creates the search index (schema only)\n"
        "2. Connects to the Azure Blob Storage datasource\n"
        "3. TODO: Creates OCR skillset for PDFs\n"
        "4. Creates the indexer to populate the index from blobs"
    ),
    response_model=SetupResponse,
    response_description="Full setup status"
)
async def full_setup():
    """
    Endpoint to perform full Azure Search setup synchronously.

    Best Practices Applied:
    - Clear step-by-step process
    - Returns status for each action
    - Raises 500 if any step fails
    """
    service = SearchSetupService()
    try:
        await service.full_setup()
        return {
            "index": settings.AZURE_SEARCH_INDEX_NAME,
            "message": "Full Azure Search setup completed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Full setup failed: {str(e)}")