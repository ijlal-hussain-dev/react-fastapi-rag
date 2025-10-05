from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AZURE_SEARCH_ENDPOINT: str
    AZURE_SEARCH_KEY: str
    AZURE_SEARCH_INDEX_NAME: str = "invertia-demo-index"
    AZURE_STORAGE_CONNECTION_STRING: str
    AZURE_CONTAINER_NAME: str
    UVICORN_PORT: int = 9900

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
