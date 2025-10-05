import logging
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes.models import (
    SearchIndexer, SearchIndexerDataSourceConnection,
    SearchIndexerDataContainer
)
from azure.search.documents.indexes.aio import SearchIndexerClient
from env.config import settings
from services.search_service import SearchService

logger = logging.getLogger(__name__)

class IndexerService:
    """
    Service to manage Azure Search data source and indexer for Blob Storage.
    """

    def __init__(self):
        self.client = SearchIndexerClient(
            endpoint=settings.AZURE_SEARCH_ENDPOINT,
            credential=AzureKeyCredential(settings.AZURE_SEARCH_KEY)
        )

    async def create_blob_data_source_and_indexer(self):
        """
        Create a data source connection to Azure Blob Storage
        and an indexer to populate the search index automatically.
        """
        # 1. Create data source
        data_source = SearchIndexerDataSourceConnection(
            name="blob-datasource",
            type="azureblob",
            connection_string=settings.AZURE_STORAGE_CONNECTION_STRING,
            container=SearchIndexerDataContainer(
                name=settings.AZURE_CONTAINER_NAME
            )
        )
        try:
            await self.client.create_data_source_connection(data_source)
            logger.info("Data source created successfully.")
        except Exception as e:
            logger.warning(f"Data source creation skipped or failed: {e}")

        # 2. Create indexer
        indexer = SearchIndexer(
            name="blob-indexer",
            data_source_name="blob-datasource",
            target_index_name=settings.AZURE_SEARCH_INDEX_NAME
        )
        try:
            await self.client.create_indexer(indexer)
            logger.info("Indexer created successfully.")
        except Exception as e:
            logger.warning(f"Indexer creation skipped or failed: {e}")


def get_indexer_service() -> IndexerService:
    search_service = SearchService(
        endpoint=settings.AZURE_SEARCH_ENDPOINT,
        index_name=settings.AZURE_SEARCH_INDEX_NAME,
        key=settings.AZURE_SEARCH_KEY
    )
    return IndexerService(search_service=search_service)