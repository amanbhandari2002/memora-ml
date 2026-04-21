# Hugging Face Spaces: port 7860, CPU-only PyTorch (smaller image, works on free tier)
FROM python:3.13-slim

WORKDIR /app

# Install Python deps: CPU-only torch first (saves ~2GB), then the rest
COPY requirements.txt .
RUN pip install --no-cache-dir torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Spaces expect port 7860
EXPOSE 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
