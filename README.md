# Pinch

Summarize text, PDFs, or images with Google Gemini (via Vertex AI). Pick a summary style and an output language.

Two interfaces share the same backend:

- **Streamlit app**: upload a PDF, TXT, or image, or paste text.
- **FastAPI web page**: paste text or upload an image, plus a JSON API.

## Features

- Styles: short paragraph, bullet points, one sentence, simple English
- Languages: English, Khmer, Thai, Vietnamese, Chinese, Japanese, French, Spanish
- Image summaries that read the text inside the image
- Light and dark mode on the web page

## Requirements

- Python 3.10+
- A Google Cloud project with the Vertex AI API enabled
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)

## Setup

```
pip install -r requirements.txt
gcloud auth application-default login
```

Create a `.env` file in the project root:

```
GCP_PROJECT_ID=your-project-id
GCP_LOCATION=us-central1
```

`GCP_LOCATION` is optional and defaults to `us-central1`.

## Run

Streamlit app (http://localhost:8501):

```
streamlit run app.py
```

FastAPI web page (http://localhost:8000, API docs at `/docs`):

```
uvicorn api:app --reload
```

Run both commands from the project folder.

## API

| Method | Path               | Body                                              | Description              |
| ------ | ------------------ | ------------------------------------------------- | ------------------------ |
| GET    | `/options`         |                                                   | Available styles/languages |
| POST   | `/summarize`       | JSON: `text`, `style`, `language`                 | Summarize text           |
| POST   | `/summarize-image` | Form: `file`, `style`, `language`                 | Summarize an image       |

Both POST endpoints return `{"summary": "..."}`. Text is limited to 200,000 characters and images to 10 MB.

```
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here", "style": "Bullet points", "language": "English"}'
```

## Project structure

```
app.py          Streamlit UI
api.py          FastAPI server
summarizer.py   Gemini calls, styles, languages
utils.py        PDF text extraction
config.py       Environment settings
static/         Web page (Tailwind via CDN) and mascot images
```

## Notes

The API has no authentication. Don't expose it publicly, or anyone could run up your Vertex AI usage.
