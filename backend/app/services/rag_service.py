from sentence_transformers import SentenceTransformer
from .milvus_service import search_knowledge
from .falcon_service import generate_response

model = SentenceTransformer('all-MiniLM-L6-v2')

def process_query(query: str):
    query_embedding = model.encode(query).tolist()
    contexts = search_knowledge(query_embedding)
    #context = " ".join(contexts)
    context = "Hi, I am an AI Agent"
    print("------query------", query)
    #print("-----------context----------", context)
    response = generate_response(query, context)
    return response