from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance,PayloadSchemaType
from qdrant_client.http import models
import uuid


model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")


qdrant_client = QdrantClient(
    url="https://cf8717cd-b5d1-4746-b26d-c491d8af4f3c.us-west-1-0.aws.cloud.qdrant.io", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.pSyn3bMit2Hnvnc6-GuUOebzuy0ynNvFfyOZA6YUsIs",
)


def init_qdrant_collection():
    collection_name = "memories"

    
    # Check if collection exists
    try:
        collections = qdrant_client.get_collections().collections
        existing_names = [col.name for col in collections]

        if collection_name not in existing_names:
            print(f"Creating collection '{collection_name}'...")
            qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE)
            )
        else:
            print(f"Collection '{collection_name}' already exists. Skipping recreation.")

        
        # CHECK IF INDEXING IS DONE FOR PAYLOADS(TO APPLY FILTERS ON THEM)
        payload_schema = qdrant_client.get_collection(collection_name).payload_schema
        if "user_id" not in payload_schema:
            payload_schema = qdrant_client.get_collection(collection_name).payload_schema
            qdrant_client.create_payload_index(
                collection_name=collection_name,
                field_name="user_id",
                field_schema=PayloadSchemaType.KEYWORD
            )
            print(f"Index for 'user_id' created.")

        

    except Exception as err:
        print(f"Error checking/creating collection: {err}")



# THIS WILL INITILISE OUR DATABASE COLLECTION IF NOT CREATED
init_qdrant_collection()    

def saveEmbeddingToDb(caption,imageName, user_uid):
    try:
        print("came to save-----")
        embedding = model.encode(caption).tolist()

        qdrant_client.upsert(
            collection_name="memories",
            points=[
                {
                    "id": str(uuid.uuid4()),
                    "vector": embedding,
                    "payload": {
                        "text": caption,
                        "user_id": user_uid,
                        "image_name":imageName
                    }
                }
            ]
        )

        points, _ = qdrant_client.scroll(
            collection_name="memories",
            limit=5
        )

        print(points)

    except Exception as err:
        print(f"Error saving embedding: {err}")



def searchCaptionMatch(caption, user_id):
    try:
        print('ok-----')
        embedding = model.encode(caption).tolist()
        print('---->',len(embedding))

        results = qdrant_client.search(
            collection_name="memories",
            query_vector=embedding,
            limit=5,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="user_id",
                        match=models.MatchValue(value=user_id)
                    )
                ]
            )
        )

        
        filtered_results = [r for r in results if r.score >= 0.6]
        print('--------',filtered_results)
        return filtered_results

    except Exception as err:
        print(f"Error searching caption match: {err}")
        return []

