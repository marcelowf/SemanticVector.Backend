from pydantic import BaseModel

class EmbeddingPayload(BaseModel):
    embedding: list[str]
