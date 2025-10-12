from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
from app.vector_db import saveEmbeddingToDb ,searchCaptionMatch
from app.vector_service import describe_image
from pydantic import BaseModel
import requests
from PIL import Image
from io import BytesIO

app = FastAPI()





app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

class SearchRequest(BaseModel):
    query: str
    user_id: str

class ImageUrl(BaseModel):
    filePath: str
    fileName: str
    user_uid:str



@app.post("/generate-caption")
async def generate_caption(data: ImageUrl):
    print('here-----',data.filePath)
    print('2here-----',data.fileName)
    response = requests.get(data.filePath)
    image = Image.open(BytesIO(response.content))


    caption = describe_image(image)
    print(caption)
    saveEmbeddingToDb(caption,data.fileName,data.user_uid)

    print('saved-----')
    return {"caption": caption}


@app.post("/search-image-vector")
async def search_image_vector(request:SearchRequest):
    print('serching-----')

    caption = request.query
    print(caption)
    results= searchCaptionMatch(request.query,request.user_id)

    print('searched-----')
    print(results)
    return {"results": results}
