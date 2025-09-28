from PIL import Image
import torch
from models.blip import processor,model

def describe_image(uploaded_file):
    print('got here')
    print('up------',uploaded_file)

    # Generate caption using BLIP
    prompt = "Describe this image vividly, including objects, colors, and context."
    inputs = processor(images=uploaded_file, text=prompt ,return_tensors="pt")
    out = model.generate(**inputs,num_beams=7,
    max_length=100,early_stopping=True)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption