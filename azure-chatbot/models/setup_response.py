from pydantic import BaseModel

class SetupResponse(BaseModel):
    status: str
    message: str