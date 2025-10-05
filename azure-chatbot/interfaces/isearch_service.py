from abc import ABC, abstractmethod
from typing import List


class ISearchService(ABC):
    @abstractmethod
    async def search_files(self, query: str, top: int = 5) -> List[str]:
        pass

    @abstractmethod
    async def suggest(self, query: str, suggester: str, top: int = 5) -> List[str]:
        pass

    @abstractmethod
    async def semantic_search(self, query: str, top: int = 5) -> List[str]:
        pass

    @abstractmethod
    async def vector_search(self, vector: list[float], top: int = 5) -> List[str]:
        pass
