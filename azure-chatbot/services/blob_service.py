import logging
from azure.storage.blob.aio import BlobServiceClient
from interfaces.iblob_service import IBlobService
from .pdf_helper import generate_pdf_bytes
from env.config import settings

logger = logging.getLogger(__name__)

class BlobService(IBlobService):
    def __init__(self):
        self.container_name = settings.AZURE_CONTAINER_NAME
        self.client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)

    async def create_container(self) -> str:
        container_client = self.client.get_container_client(self.container_name)
        try:
            await container_client.create_container()
            logger.info(f"Container {self.container_name} created")
            return f"Container {self.container_name} created"
        except Exception:
            logger.info(f"Container {self.container_name} already exists")
            return f"Container {self.container_name} already exists"

    async def upload_file(self, file_name: str, file_data: bytes) -> str:
        container_client = self.client.get_container_client(self.container_name)
        blob_client = container_client.get_blob_client(file_name)
        description = f"Invoice for {file_name}"

        metadata = {
            "description": description # KEEP custom description metadata
        }

        await blob_client.upload_blob(file_data, overwrite=True, metadata=metadata)
        logger.info(f"Uploaded {file_name} with metadata: {metadata}")
        return f"Uploaded {file_name}"

    async def generate_files(self, prefix: str, count: int) -> str:
        uploaded_files = []
        await self.create_container()
        for i in range(1, count + 1):
            invoice_id = f"{prefix}{i:03d}"
            pdf_bytes = await generate_pdf_bytes(invoice_id,i)
            file_name = f"{invoice_id}.pdf"
            await self.upload_file(file_name, pdf_bytes)
            uploaded_files.append(file_name)
        logger.info(f"Generated and uploaded {count} files")
        return f"Generated and uploaded {count} files: {uploaded_files}"
    
    async def inspect_blob_metadata(self, blob_name: str):
        """
        Fetches and prints blob properties and custom metadata, logging output 
        to the console (where your application is running).
        Returns a dictionary for successful API response.
        """
        output_data = {}
        try:
            container_client = self.client.get_container_client(self.container_name)
            blob_client = container_client.get_blob_client(blob_name)

            logger.info(f"--- Attempting to Inspect Blob: {blob_name} ---")

            # Fetch Properties and Metadata
            blob_properties = await blob_client.get_blob_properties()
            
            # 1. System Properties (Crucial for fileName, blobPath)
            output_data['SystemProperties'] = {
                'File Name (metadata_storage_name)': blob_properties.name,
                'Full URI (metadata_storage_uri)': blob_client.url,
                'Path (metadata_storage_path)': blob_properties.name,
            }
            logger.info("\n System Properties (Potential Field Mapping Sources):\n%s", 
                        output_data['SystemProperties'])

            # 2. Custom Metadata (Crucial for description)
            output_data['CustomMetadata'] = {}
            if blob_properties.metadata:
                for key, value in blob_properties.metadata.items():
                    # The key used here is the *exact* casing needed after metadata_storage_
                    print(key, value)
                    output_key = f"/document/metadata_storage_{key}"
                    output_data['CustomMetadata'][output_key] = value
                    
                logger.info("\nCustom User Metadata (Check Casing!):\n%s", 
                            output_data['CustomMetadata'])
            else:
                logger.warning("No custom user metadata found on this blob.")
                output_data['CustomMetadata'] = "None found."
            
            return {"status": "success", "data": output_data}

        finally:
            return output_data