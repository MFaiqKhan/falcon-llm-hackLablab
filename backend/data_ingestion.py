import os
from PyPDF2 import PdfReader
import xml.etree.ElementTree as ET
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from dotenv import load_dotenv

load_dotenv()

def process_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    text = ' '.join(root.itertext())
    return text

def process_pdf(file_path):
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text() + ' '
    return text

def init_qdrant():
    client = QdrantClient(
        url=os.getenv('QDRANT_URL'),
        api_key=os.getenv('QDRANT_API_KEY')
    )
    
    collections = client.get_collections()
    if "Medical_LLM" not in [c.name for c in collections.collections]:
        client.create_collection(
            collection_name="Medical_LLM",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)  # 384 is the dimension for 'all-MiniLM-L6-v2'
        )
    return client

def insert_knowledge(client, text, embedding, metadata):
    point = PointStruct(
        id=len(client.scroll(collection_name="Medical_LLM", limit=1)[0]) + 1,  # Simple incremental ID
        vector=embedding,
        payload={"text": text, "metadata": metadata}
    )
    client.upload_records(
        collection_name="Medical_LLM",
        records=[point]
    )

def ingest_data(directory):
    client = init_qdrant()
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    for filename in os.listdir(directory):
        print(directory)
        file_path = os.path.join(directory, filename)
        if filename.endswith('.xml'):
            print(filename)
            text = process_xml(file_path)
            file_type = 'xml'
        elif filename.endswith('.pdf'):
            text = process_pdf(file_path)
            file_type = 'pdf'
        else:
            continue
        
        embedding = model.encode(text).tolist()
        metadata = {"filename": filename, "file_type": file_type}
        insert_knowledge(client, text, embedding, metadata)
    
    print("Data ingestion completed.")

if __name__ == "__main__":
    ingest_data('E:\Github\\falcon-llm-hack\\backend\\assets')