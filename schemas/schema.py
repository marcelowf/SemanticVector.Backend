from pydantic import BaseModel

class EncodePayload(BaseModel):
    embedding: list[str]
    
class DecodePayload(BaseModel):
    message: str
