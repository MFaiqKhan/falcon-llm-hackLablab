from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct
import os

client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY'))

def init_qdrant():
    # This is now handled in the data_ingestion.py script
    pass

def insert_knowledge(text, embedding):
    point = PointStruct(
        id=len(text),
        vector=embedding,
        payload={"text": text}
    )
    client.upload_points(
        collection_name="Medical_LLM",
        points=[point]
    )

def search_knowledge(query_vector, top_k=1):
    search_result = client.search(
        collection_name="Medical_LLM",
        query_vector=query_vector,
        limit=top_k
    )
    return [hit.payload['text'] for hit in search_result]