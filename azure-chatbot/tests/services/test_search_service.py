import pytest
from unittest.mock import AsyncMock, patch
from services.search_service import SearchService
from models.search_result import SearchResult
from azure.search.documents.models import QueryType

class AsyncIterator:
    """Helper to mock async iteration for search results"""
    def __init__(self, items):
        self.items = items
        self.index = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.index >= len(self.items):
            raise StopAsyncIteration
        item = self.items[self.index]
        self.index += 1
        return item

@pytest.mark.asyncio
class TestSearchService:

    async def test_search_keyword_returns_results(self):
        mock_results = [
            {
                "blobName": "file1.pdf",
                "blobPath": "https://example.com/file1.pdf",
                "content": "Hello world",
                "description": "Test file"
            },
            {
                "blobName": "file2.pdf",
                "blobPath": "https://example.com/file2.pdf",
                "content": "Another content",
                "description": "Another file"
            },
        ]
        async_iter = AsyncIterator(mock_results)

        with patch("services.search_service.SearchClient", autospec=True) as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.search = AsyncMock(return_value=async_iter)

            service = SearchService()
            results = await service.search_keyword("test query", top=2)

            assert len(results) == 2
            assert all(isinstance(r, SearchResult) for r in results)
            assert results[0].fileName == "file1.pdf"
            assert results[1].contentSnippet.startswith("Another content")

    async def test_suggest_returns_text_list(self):
        mock_suggestions = [{"text": "suggestion1"}, {"text": "suggestion2"}]

        with patch("services.search_service.SearchClient", autospec=True) as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.suggest = AsyncMock(return_value=mock_suggestions)

            service = SearchService()
            suggestions = await service.suggest("sugg")

            assert suggestions == ["suggestion1", "suggestion2"]

    async def test_search_with_filter_builds_filter_string(self):
        mock_results = [
            {
                "blobName": "file1.pdf",
                "blobPath": "https://example.com/file1.pdf",
                "content": "test",
                "description": ""
            }
        ]
        async_iter = AsyncIterator(mock_results)

        with patch("services.search_service.SearchClient", autospec=True) as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.search = AsyncMock(return_value=async_iter)

            service = SearchService()
            results = await service.search_with_filter("test", id="123", blob_name="file1.pdf")

            assert len(results) == 1
            called_args, called_kwargs = mock_client_instance.search.call_args
            assert "filter" in called_kwargs
            assert called_kwargs["filter"] == "id eq '123' and blobName eq 'file1.pdf'"

    async def test_search_semantic_returns_results(self):
        mock_results = [
            {
                "fileName": "file1.pdf",
                "blobPath": "https://example.com/file1.pdf",
                "content": "Semantic content",
                "description": "Desc1"
            },
            {
                "fileName": "file2.pdf",
                "blobPath": "https://example.com/file2.pdf",
                "content": "More semantic content",
                "description": "Desc2"
            },
        ]
        async_iter = AsyncIterator(mock_results)

        with patch("services.search_service.SearchClient", autospec=True) as MockClient:
            mock_client_instance = MockClient.return_value
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.search = AsyncMock(return_value=async_iter)

            service = SearchService()
            results = await service.search_semantic("semantic query", top=2)

            assert len(results) == 2
            assert all(isinstance(r, SearchResult) for r in results)
            assert results[0].fileName == "file1.pdf"
            assert results[1].contentSnippet.startswith("More semantic content")

            called_args, called_kwargs = mock_client_instance.search.call_args
            assert called_kwargs["query_type"] == QueryType.SEMANTIC
            assert called_kwargs["semantic_configuration_name"] == "default"
