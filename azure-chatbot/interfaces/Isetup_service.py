from abc import ABC, abstractmethod
from typing import Dict

class ISetupService(ABC):
    @abstractmethod
    async def create_index(self) -> Dict:
        pass

    @abstractmethod
    async def create_indexer(self) -> Dict:
        pass

    @abstractmethod
    async def setup_all(self) -> Dict:
        pass
