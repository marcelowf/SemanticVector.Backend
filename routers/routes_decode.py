from fastapi import APIRouter
from schemas.schema import DecodePayload
from services.decoder_service import DecoderService

router = APIRouter()

@router.post("/")
async def embedding_decode(payload: DecodePayload):
    result = await DecoderService.decode_embedding(payload.message)
    return {"message": result}
