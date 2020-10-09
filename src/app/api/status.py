from fastapi import APIRouter

router = APIRouter()


@router.get("/status", status_code=200)
async def status():
    return {"status": True}
