import os
import io
import google.generativeai as genai
from PIL import Image

# Configure Gemini once at module load
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
_gemini_model = genai.GenerativeModel("gemini-1.5-flash")

CAPTION_PROMPT = (
    "Describe this image vividly and in detail, "
    "including the main objects, colors, mood, and any relevant context. "
    "Keep the description under 150 words."
)

def describe_image(uploaded_file: Image.Image) -> str:
    """Generate a descriptive caption for an image using Google Gemini."""
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

    response = _gemini_model.generate_content([CAPTION_PROMPT, image_part])
    caption = response.text.strip()

    print("caption:", caption)
    return caption