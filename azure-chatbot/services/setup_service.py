import logging
import asyncio # Required for asynchronous waiting
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes.aio import SearchIndexerClient, SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndexer,
    SearchIndexerDataSourceConnection,
    FieldMapping
)


from env.config import settings
from models.search_schema import get_index_schema 

logger = logging.getLogger(__name__)


class SearchSetupService:
    """Async service to setup Azure Search: index, datasource, indexer."""

    def __init__(self):
        self.indexClient = SearchIndexClient(
            endpoint=settings.AZURE_SEARCH_ENDPOINT,
            credential=AzureKeyCredential(settings.AZURE_SEARCH_KEY)
        )
        self.indexerClient = SearchIndexerClient(
            endpoint=settings.AZURE_SEARCH_ENDPOINT,
            credential=AzureKeyCredential(settings.AZURE_SEARCH_KEY)
        )

        self.index_name = settings.AZURE_SEARCH_INDEX_NAME
        self.indexer_name = "invertia-demo-indexer" 
        self.datasource_name = "invertia-demo-ds" # Defined for clarity

    async def create_index(self):
        """Creates or recreates the search index based on the schema."""
        index = get_index_schema(self.index_name)
        try:
            await self.indexClient.delete_index(self.index_name)
            logger.info("Existing Index deleted: %s", self.index_name)
        except Exception:
            pass
            
        await self.indexClient.create_index(index)
        logger.info("Index created: %s", self.index_name)
        return {"status": "created", "message": f"Index {self.index_name} created"}

    async def create_blob_data_source(self):
        """Create Azure Blob datasource with contentAndMetadata setting."""
        ds = SearchIndexerDataSourceConnection(
            name=self.datasource_name,
            type="azureblob",
            connection_string=settings.AZURE_STORAGE_CONNECTION_STRING,
            container={"name": settings.AZURE_CONTAINER_NAME},
            # CRITICAL: Must be set to read custom/system metadata
            data_to_extract="contentAndMetadata" 
        )
        try:
            await self.indexerClient.delete_data_source_connection(ds.name)
        except Exception:
            pass
            
        await self.indexerClient.create_data_source_connection(ds)
        logger.info("Datasource created: %s", ds.name)

    async def create_indexer(self):
        """Create indexer with corrected field mappings and explicit configuration."""
        # try:
        #     await self.indexerClient.delete_indexer(self.indexer_name)
        # except Exception:
        #     pass
            
        indexer = SearchIndexer(
            name=self.indexer_name, 
            data_source_name=self.datasource_name,
            target_index_name=self.index_name,
            parameters={
                "configuration": {
                    "parsingMode": "default", 
                    "dataToExtract": "contentAndMetadata" 
                }
            },

            field_mappings=[],
            output_field_mappings=[
                FieldMapping(source_field_name="/document/content", target_field_name="content"),
                FieldMapping(source_field_name="/document/metadata_storage_name", target_field_name="blobName"),
                FieldMapping(source_field_name="/document/metadata_storage_path", target_field_name="blobPath"),
                FieldMapping(source_field_name="/document/description", target_field_name="description")
            ]
        )

        await self.indexerClient.create_indexer(indexer)
        logger.info("Indexer created: %s", self.indexer_name)

    async def run_indexer(self):
        """Polls status, resets, and runs the indexer, fixing concurrency issues."""
        indexer_name = self.indexer_name
        
        # FIX: Wait for the indexer to finish any prior run
        while True:
            try:
                indexer_status = await self.indexerClient.get_indexer_status(indexer_name)
                
                if indexer_status.status in ['running']:
                    logger.info("Indexer status: RUNNING. Waiting 10 seconds...")
                    await asyncio.sleep(10)
                elif (
                    indexer_status.last_result and 
                    indexer_status.last_result.status in ['inProgress', 'transientFailure']
                ):
                    logger.info("Last indexer result status: IN PROGRESS/FAILURE. Waiting 10 seconds...")
                    await asyncio.sleep(10)
                else:
                    logger.info("Indexer status: IDLE or complete. Proceeding with reset/run.")
                    break
            except Exception as e:
                logger.warning("Could not check indexer status: %s. Proceeding.", str(e))
                break

        try:
            await self.indexerClient.reset_indexer(indexer_name)
            logger.info("Indexer reset successfully: %s", indexer_name)
        except Exception as e:
            logger.warning("Failed to reset indexer: %s. Error: %s", indexer_name, str(e))

        await self.indexerClient.run_indexer(indexer_name)
        logger.info("Indexer run initiated: %s", indexer_name)

    async def full_setup(self):
        """Perform full setup: index + datasource + indexer + run."""
        try:
            await self.create_index()
            await self.create_blob_data_source()
            await self.create_indexer()          
            return {"status": "success", "message": "Full setup completed and indexer started"}
        except Exception as e:
            logger.exception("Full setup failed")
            raise RuntimeError(f"Full setup failed: {str(e)}")