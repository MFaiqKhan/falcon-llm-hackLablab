from ai71 import AI71
from flask import current_app

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

def generate_response(prompt: str, context):
    ai71_client = AI71(current_app.config['AI71_API_KEY'])
    print("------cccccccccccccccccc", context)
    
    messages = [
        {"role": "system", "content": "You are a helpful medical assistant."},
        {"role": "user", "content": f"Context: {context}\n\nUser: {prompt}"}
    ]
    try:
        response = ai71_client.chat.completions.create(
            model="tiiuae/falcon-180B-chat",
            messages=messages,
            max_tokens=10000,
            temperature=0.7
        )
        print(response)
        
        result = response.choices[0].message.content.strip()
        
        return result

    except Exception as e:
        return {"error": f"Failed to generate result: {str(e)}"}