import logging
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field
from summarizer import summarize, summarize_image, STYLES, LANGUAGES
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger(__name__)

INDEX_HTML = Path(__file__).parent / "static" / "index.html"
MAX_TEXT_CHARS = 200_000
MAX_IMAGE_BYTES = 10 * 1024 * 1024

app = FastAPI(title="Text Summarizer API")
app.mount("/static", StaticFiles(directory=INDEX_HTML.parent), name="static")


class TextRequest(BaseModel):
    text: str = Field(max_length=MAX_TEXT_CHARS)
    style: str = "Short paragraph"
    language: str = "English"


def check_options(style: str, language: str):
    if style not in STYLES:
        raise HTTPException(400, f"style must be one of {list(STYLES)}")
    if language not in LANGUAGES:
        raise HTTPException(400, f"language must be one of {LANGUAGES}")


@app.get("/")
def root():
    return FileResponse(INDEX_HTML)


@app.get("/options")
def options():
    return {"styles": list(STYLES), "languages": LANGUAGES}


@app.post("/summarize")
def summarize_text(req: TextRequest):
    check_options(req.style, req.language)
    try:
        return {"summary": summarize(req.text, req.style, req.language)}
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception:
        logger.exception("summarize failed")
        raise HTTPException(500, "Summarization failed. Please try again.")


@app.post("/summarize-image")
async def summarize_img(
    file: UploadFile = File(...),
    style: str = Form("Short paragraph"),
    language: str = Form("English"),
):
    check_options(style, language)
    if not (file.content_type or "").startswith("image/"):
        raise HTTPException(400, "File must be an image")
    data = await file.read(MAX_IMAGE_BYTES + 1)
    if len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(413, "Image must be 10 MB or smaller")
    try:
        return {"summary": summarize_image(data, file.content_type, style, language)}
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception:
        logger.exception("summarize-image failed")
        raise HTTPException(500, "Summarization failed. Please try again.")
