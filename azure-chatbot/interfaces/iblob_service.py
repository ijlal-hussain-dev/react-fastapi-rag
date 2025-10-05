from abc import ABC, abstractmethod

class IBlobService(ABC):
    @abstractmethod
    async def create_container(self) -> str:
        pass

    @abstractmethod
    async def upload_file(self, file_path: str, blob_name: str) -> str:
        pass

    @abstractmethod
    async def generate_files(self, prefix: str, count: int) -> str:
        """
        Generate multiple PDF files with realistic content and upload them.
        `prefix` will be used for file names (e.g., 'INV').
        `count` is the number of files to generate.
        """
        pass