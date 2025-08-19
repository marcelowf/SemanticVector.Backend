from fastapi import APIRouter
from schemas.schema import EmbeddingPayload
from services.encoder_service import EncoderService

router = APIRouter()

@router.post("/")
async def embedding_encode(payload: EmbeddingPayload):
    return {"embedding": EncoderService.encode_embedding(payload.embedding)}
