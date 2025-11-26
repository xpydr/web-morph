
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import List
import io, zipfile

from app.utils.file_conversion import convert_file, FORMAT_MAP

router = APIRouter()

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...), convert_to: str = Query(...)):
    print(convert_to)
    convert_to_lower = convert_to.lower()
    if convert_to_lower not in FORMAT_MAP:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid format: {convert_to}. Choose from: {', '.join(FORMAT_MAP.keys())}"
        )

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            if not file.filename:
                continue  # skip empty

            contents = await file.read()
            converted = convert_file(contents, convert_to_lower)

            if converted is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"Cannot convert {file.filename} (invalid or unsupported image)"
                )

            name_no_ext = file.filename.rsplit(".", 1)[0]
            new_filename = f"{name_no_ext}.{convert_to_lower}"
            zipf.writestr(new_filename, converted)

    zip_buffer.seek(0)

    return StreamingResponse(
        iter(lambda: zip_buffer.read(8192), b""),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=converted_files.zip"}
    )
    