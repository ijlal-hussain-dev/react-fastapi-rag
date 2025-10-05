from pydantic import BaseSettings

class BaseConfig(BaseSettings):
    AZURE_SEARCH_ENDPOINT: str
    AZURE_SEARCH_KEY: str
    AZURE_SEARCH_INDEX_NAME: str

    class Config:
        env_file = ".env"
