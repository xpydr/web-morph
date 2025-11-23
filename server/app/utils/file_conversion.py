
from PIL import Image, UnidentifiedImageError
from io import BytesIO

# Full Pillow saveable format mapping
FORMAT_MAP = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "bmp": "BMP",
    "tiff": "TIFF",
    "tif": "TIFF",
    "gif": "GIF",
    "webp": "WEBP",
    "ppm": "PPM",
    "pgm": "PPM",
    "pbm": "PPM",
    "ico": "ICO",
    "icns": "ICNS",
    "tga": "TGA",
    "eps": "EPS",
    "pdf": "PDF",
    "sgi": "SGI",
    "rgb": "RGB",
    "pcx": "PCX",
    "spider": "SPIDER",
}

def convert_file(file_bytes: bytes, convert_to: str) -> BytesIO | None:
    try:
        img = Image.open(BytesIO(file_bytes)).convert("RGB")
    except UnidentifiedImageError:
        return None  # Not a valid image

    pil_format = FORMAT_MAP.get(convert_to.lower())
    if not pil_format:
        return None  # Unsupported format

    output = BytesIO()
    img.save(output, format=pil_format)
    output.seek(0)
    return output
