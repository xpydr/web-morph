
from PIL import Image, UnidentifiedImageError
import io

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

def convert_file(file_bytes: bytes, convert_to: str) -> bytes | None:
    convert_to = convert_to.lower()
    if convert_to not in FORMAT_MAP:
        return None

    pillow_format = FORMAT_MAP[convert_to]

    try:
        img = Image.open(io.BytesIO(file_bytes))

        # Special handling for JPEG (no alpha channel)
        if pillow_format == "JPEG":
            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255)) # white background
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
                img = background
            elif img.mode != "RGB":
                img = img.convert("RGB")

        output = io.BytesIO()
        save_kwargs = {}
        
        # Some formats need extra parameters
        if pillow_format == "JPEG":
            save_kwargs["quality"] = 95
            save_kwargs["optimize"] = True

        img.save(output, format=pillow_format, **save_kwargs)
        return output.getvalue()

    except (UnidentifiedImageError, OSError, ValueError, Exception):
        return None
