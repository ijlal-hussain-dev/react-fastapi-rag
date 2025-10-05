from pydantic import BaseModel, HttpUrl
from typing import Optional

class SearchResult(BaseModel):
    fileName: str
    blobPath: HttpUrl
    contentSnippet: Optional[str] = None
    customer: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None