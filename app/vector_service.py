import os
import io
import time
import random
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from PIL import Image

# Configure Gemini once at module load
# Using gemini-2.0-flash-lite: higher free-tier quota (30 RPM vs 15 RPM)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
_gemini_model = genai.GenerativeModel("gemini-2.0-flash-lite")

CAPTION_PROMPT = (
    "Describe this image vividly and in detail, "
    "including the main objects, colors, mood, and any relevant context. "
    "Keep the description under 150 words."
)

_MAX_RETRIES = 4
_BASE_DELAY  = 5  # seconds


def describe_image(uploaded_file: Image.Image) -> str:
    """Generate a descriptive caption for an image using Google Gemini.

    Retries automatically on 429 quota errors using exponential backoff
    with jitter (up to _MAX_RETRIES attempts).
    """
    print("describe_image called")
    print("image:", uploaded_file)

    # Convert PIL image to JPEG bytes for the Gemini API
    buffer = io.BytesIO()
    uploaded_file.convert("RGB").save(buffer, format="JPEG")
    image_bytes = buffer.getvalue()

    image_part = {
        "mime_type": "image/jpeg",
        "data": image_bytes,
    }

    last_exc = None
    for attempt in range(_MAX_RETRIES):
        try:
            response = _gemini_model.generate_content([CAPTION_PROMPT, image_part])
            caption = response.text.strip()
            print("caption:", caption)
            return caption
        except ResourceExhausted as exc:
            last_exc = exc
            delay = _BASE_DELAY * (2 ** attempt) + random.uniform(0, 2)
            print(
                f"[describe_image] Quota exceeded (attempt {attempt + 1}/{_MAX_RETRIES}). "
                f"Retrying in {delay:.1f}s…"
            )
            time.sleep(delay)

    raise RuntimeError(
        f"Gemini API quota exhausted after {_MAX_RETRIES} retries. "
        "Please wait a minute or check your billing at https://ai.dev/rate-limit."
    ) from last_exc