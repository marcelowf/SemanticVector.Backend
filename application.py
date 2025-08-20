import os
from fastapi import APIRouter, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from core.logging import setup_logging
from routers import routes_encode, routes_decode, routes_health, routes_scraper
from contextlib import asynccontextmanager
from sentence_transformers import SentenceTransformer
from core.config import settings
from services.encoder_service import EncoderService

logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando o servidor...")
    try:
        model = SentenceTransformer(settings.embedding_model_name)
        EncoderService.set_model(model)
        logger.info("Modelo de embedding carregado.")
    except Exception as e:
        logger.error(f"Falha ao carregar modelo de embedding: {e}")

    yield
    logger.info("Desligando o servidor...")

app = FastAPI(title="RAG Embedding API", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

router = APIRouter()

@router.get("/")
async def home():
    return FileResponse(os.path.join("static", "index.html"))
    
app.include_router(router)
app.include_router(routes_encode.router, prefix="/encode", tags=["Encode"])
app.include_router(routes_decode.router, prefix="/decode", tags=["Decode"])
app.include_router(routes_health.router, prefix="/health", tags=["Health"])
app.include_router(routes_scraper.router, prefix="/scraper", tags=["Scraper"])
