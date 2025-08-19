from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def web_scraping():
    return {"Screped"}
