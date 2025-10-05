import logging
import pytest
from unittest.mock import AsyncMock, patch
from azure.core.exceptions import AzureError
from services.search_service import SearchService
from models.search_result import SearchResult

@pytest.mark.asyncio
class TestSearchServiceErrors:

    async def test_search_keyword_azure_error(self, caplog):
        caplog.set_level(logging.ERROR)
        async def raise_azure_error(*args, **kwargs):
            raise AzureError("Azure failure")

        with patch("services.search_service.SearchClient", autospec=True) as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.search = AsyncMock(side_effect=raise_azure_error)

            service = SearchService()
            with pytest.raises(RuntimeError, match="Azure Search query failed: Azure failure"):
                await service.search_keyword("fail query")

            # Check that the error was logged
            assert any("Search query failed with AzureError: Azure failure" in r.message for r in caplog.records)


    async def test_search_keyword_unexpected_error(self, caplog):
        caplog.set_level(logging.ERROR)
        async def raise_generic_error(*args, **kwargs):
            raise ValueError("Unexpected failure")

        with patch("services.search_service.SearchClient", autospec=True) as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.search = AsyncMock(side_effect=raise_generic_error)

            service = SearchService()
            with pytest.raises(RuntimeError, match="Search query failed: Unexpected failure"):
                await service.search_keyword("fail query")

            # Check that the error was logged
            assert any("Search query failed with unexpected error" in r.message for r in caplog.records)

    async def test_suggest_azure_error(self, caplog):
        caplog.set_level(logging.ERROR)
        async def raise_azure_error(*args, **kwargs):
            raise AzureError("Suggest failure")

        with patch("services.search_service.SearchClient", autospec=True) as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.suggest = AsyncMock(side_effect=raise_azure_error)

            service = SearchService()
            results = await service.suggest("fail sugg")
            assert results == []
            assert any("Suggest query failed" in r.message for r in caplog.records)

    async def test_suggest_generic_error(self, caplog):
        caplog.set_level(logging.ERROR)
        async def raise_generic_error(*args, **kwargs):
            raise ValueError("Unexpected failure")

        with patch("services.search_service.SearchClient", autospec=True) as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.suggest = AsyncMock(side_effect=raise_generic_error)

            service = SearchService()
            results = await service.suggest("fail sugg")
            assert results == []
            assert any("Unexpected error in suggest" in r.message for r in caplog.records)
