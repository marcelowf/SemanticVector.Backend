from fastapi import APIRouter
from schemas.schema import EmbeddingPayload
from services.decoder_service import DecoderService

router = APIRouter()

@router.post("/")
async def embedding_decode(payload: EmbeddingPayload):
    return {"text": DecoderService.decode_embedding(payload.embedding)}

