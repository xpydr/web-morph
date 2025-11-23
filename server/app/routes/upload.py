
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.utils.file_conversion import convert_file

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), convert_to: str = "jpg"):
    contents = await file.read()

    converted_bytes = convert_file(contents, convert_to)
    if not converted_bytes:
        raise HTTPException(status_code=400, detail="Invalid file or unsupported format")

    original_name = file.filename.rsplit(".", 1)[0]  # remove original extension
    new_filename = f"{original_name}.{convert_to.lower()}"

    return StreamingResponse(
        converted_bytes,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={new_filename}"}
    )
