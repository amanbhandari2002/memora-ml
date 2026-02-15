---
title: Snapmemo ML
emoji: 📸
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
---

# Snapmemo ML

FastAPI app for image captioning (BLIP) and semantic search (sentence-transformers + Qdrant).

## Upload to Hugging Face Spaces

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and click **Create new Space**.
2. Pick a **name** and **license**; choose **Docker** as the SDK.
3. Push this repo to the Space:
   - **Option A:** When creating the Space, choose **Import from a Git repository** and paste your GitHub repo URL (e.g. `https://github.com/YOUR_USERNAME/memora-ml`). HF will clone it and use this Dockerfile.
   - **Option B:** Clone the new Space repo, copy your code in, then push:
     ```bash
     git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
     cd YOUR_SPACE_NAME
     cp -r /path/to/memora-ml/* .
     git add . && git commit -m "Add Snapmemo ML" && git push
     ```
4. In the Space → **Settings** → **Repository secrets**, add `QDRANT_URL` and `QDRANT_API_KEY`.
5. The Space will build and run. Your app will be at `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space`.

## API

- **POST /generate-caption** – Send image URL; returns caption and stores embedding in Qdrant.
- **POST /search-image-vector** – Semantic search by text query and `user_id`.
- **GET /health** – Health check.

## Secrets (required on Hugging Face)

In your Space → **Settings** → **Repository secrets**, add:

| Secret name       | Description                    |
|-------------------|--------------------------------|
| `QDRANT_URL`      | Your Qdrant cluster URL        |
| `QDRANT_API_KEY`  | Your Qdrant API key            |

Without these, the app will fail when calling Qdrant.

## Local run

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Set `QDRANT_URL` and `QDRANT_API_KEY` in your environment (or `.env`) if you use env-based config.
