
from fastapi import APIRouter
from app.utils.file_conversion import FORMAT_MAP

router = APIRouter()

@router.get("/supported-formats")
async def supported_formats():
    """
    Returns a list of supported image formats that can be converted.
    """
    return {"formats": list(FORMAT_MAP.keys())}
