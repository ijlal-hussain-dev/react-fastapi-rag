from fastapi import APIRouter, Depends, Query
from services.blob_service import BlobService, generate_pdf_bytes

router = APIRouter(prefix="/blobs", tags=["BlobService"])

def get_blob_service() -> BlobService:
    return BlobService()

@router.post("/create-container")
async def create_container(service: BlobService = Depends(get_blob_service)):
    """Ensure the blob container exists."""
    result = await service.create_container()
    return {"message": result}


@router.post("/upload-blob")
async def upload_file(filetype: str = Query("pdf", description="File type"), 
                      file_name: str = Query(..., description="File name"), 
                      service: BlobService = Depends(get_blob_service)):
    """
    Upload a single file to the blob container.
    Expects file data to be generated via PDF generator or uploaded manually.
    """
    # For demo, generate a PDF in memory
    pdf_bytes = await generate_pdf_bytes(file_name,40)
    result = await service.upload_file(file_name, pdf_bytes)
    return {"message": result}


@router.post("/generate-upload")
async def generate_and_upload(
    prefix: str = Query("Invoice", description="Invoice ID prefix for generated PDFs"),
    filetype: str = Query("pdf", description="File type, only pdf supported"),
    count: int = Query(20, description="Number of files to generate"),
    service: BlobService = Depends(get_blob_service)
):
    """
    Generate `count` PDF invoices with realistic multi-country fields and upload to blob container.
    """
    if filetype.lower() != "pdf":
        return {"error": "Only PDF file type is supported"}

    uploaded_files = []
    await service.create_container()  # ensure container exists

    for i in range(1, count + 1):
        invoice_id = f"{prefix}{i:03d}"
        pdf_bytes = await generate_pdf_bytes(invoice_id, i)
        file_name = f"{invoice_id}.pdf"
        await service.upload_file(file_name, pdf_bytes)
        uploaded_files.append(file_name)

    return {"message": f"{count} {filetype.upper()} files uploaded", "files": uploaded_files}



@router.get("/get-props")
async def get_props(
    prefix: str = Query("invoice001.pdf", description="blobName"),
    service: BlobService = Depends(get_blob_service)
):
    """
    Generate `count` PDF invoices with realistic multi-country fields and upload to blob container.
    """
    ret = await service.inspect_blob_metadata(prefix)  # ensure container exists
    return ret