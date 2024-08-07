import os
import logging
from dotenv import load_dotenv
from ai71 import AI71
from flask import current_app
from sentence_transformers import SentenceTransformer
from .milvus_service import search_knowledge

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

model = SentenceTransformer('all-MiniLM-L6-v2')

def summarize_context(context, max_sentences=2):
    sentences = context.split('.')
    summary = '. '.join(sentences[:max_sentences]) + '.'
    return summary.strip()

def process_query(query: str):
    logger.info(f"Processing query: {query}")
    query_embedding = model.encode(query).tolist()
    contexts = search_knowledge(query_embedding)
    
    # Summarize the context
    full_context = " ".join(contexts)
    summarized_context = summarize_context(full_context)
    
    logger.info(f"Summarized Context: {summarized_context}")
    response = generate_response(query, summarized_context)
    return response

def generate_response(prompt: str, context):
    ai71_client = AI71(current_app.config['AI71_API_KEY'])
    logger.info(f"Generating response for prompt: {prompt}")
    
    messages = [
        {"role": "system", "content": "You are a helpful medical assistant. Provide concise answers."},
        {"role": "user", "content": f"Context: {context}\n\nUser: {prompt}"}
    ]
    
    try:
        response = ai71_client.chat.completions.create(
            model="tiiuae/falcon-180B-chat",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        result = response.choices[0].message.content.strip()
        logger.info(f"Generated response: {result[:100]}...")  # Log first 100 characters
        
        return result

    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return {"error": f"Failed to generate response: {str(e)}"}

# This function can be used for testing purposes
def test_generate_response(prompt: str, context: str):
    AI71_API_KEY = os.getenv("AI71_API_KEY")
    if not AI71_API_KEY:
        logger.error("AI71_API_KEY not found in environment variables")
        return {"error": "AI71_API_KEY not configured"}
    
    ai71_client = AI71(AI71_API_KEY)
    
    return generate_response(prompt, context)

if __name__ == "__main__":
    # For testing purposes
    test_prompt = "What are the symptoms of schizophrenia?"
    test_context = "Schizophrenia is a mental disorder characterized by disruptions in thought processes, perceptions, emotional responsiveness, and social interactions. Symptoms can include hallucinations, delusions, disorganized speech, and social withdrawal."
    #print(test_generate_response(test_prompt, test_context))