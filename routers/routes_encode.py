from fastapi import APIRouter
from schemas.schema import EncodePayload
from services.encoder_service import EncoderService

router = APIRouter()

@router.post("/")
async def embedding_encode(payload: EncodePayload):
    return EncoderService.encode_embedding(payload.embedding)
