# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```
pip install -r requirements.txt
streamlit run app.py          # Streamlit UI (PDF, TXT, image) at :8501
uvicorn api:app --reload      # FastAPI + static page (text, image) at :8000, docs at /docs
```

Run both from the project root: `api.py` serves `static/index.html` relative to its own file, but `.env` is loaded from the working directory. There are no tests or linter configured.

## Setup

- Gemini is called through **Vertex AI** (`genai.Client(vertexai=True, ...)`), not an API key. It needs `gcloud auth application-default login` and the Vertex AI API enabled on the project.
- `.env` must define `GCP_PROJECT_ID` (optional `GCP_LOCATION`, default `us-central1`). `config.py` raises at import if the project ID is missing. `.env` is gitignored; never edit or commit it.

## Architecture

Two independent front ends share one backend module:

- `summarizer.py` is the core. It builds the prompts, calls Gemini once (module-level `client`), and holds the `STYLES` dict and `LANGUAGES` list. `summarize()` is for text and `summarize_image()` is for images. Both raise `ValueError` for bad input or an empty or blocked model response.
- `app.py` (Streamlit) and `api.py` (FastAPI) both import from `summarizer.py`. Adding a style or language means editing `STYLES` or `LANGUAGES` only. `api.py` exposes them via `/options`, and `static/index.html` builds its style buttons and language picker from that endpoint.
- `utils.py` holds `read_pdf`, which only the Streamlit app uses. The FastAPI page has no PDF or TXT upload.
- Error contract in `api.py`: `ValueError` becomes HTTP 400. Any other exception becomes a generic HTTP 500 with the real error logged. The front end reads `detail` from the JSON error body.
- `static/index.html` is a single page (the site is called Pinch) styled with the Tailwind CDN and Google Fonts. `api.py` mounts `static/` at `/static`, which serves the favicon and mascot images. Its script uses the element ids as globals (`language`, `text`, `image`, `result`, `langBtn`, `langList`, and others), so renaming an id breaks it. The selected style lives in the `currentStyle` variable. The language picker is a custom listbox over a hidden `<select id="language">`, which holds the value that gets sent. On desktop (`lg:`) the layout is locked to the viewport height with no page scroll.
