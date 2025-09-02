from PIL import Image
import torch
from models.blip import processor,model

def describe_image(uploaded_file):
    print('got here')
    print('up------',uploaded_file)

    # Generate caption using BLIP
    inputs = processor(images=uploaded_file,return_tensors="pt")
    out = model.generate(**inputs,num_beams=5,
    max_length=50,early_stopping=True)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption