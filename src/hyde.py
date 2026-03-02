import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_URL","http://localhost:11434")

def generate_hypothetical_answer(question):
    prompt = f"""
        You are a medical reference assistant.
        Generate a hypothetical but plausible FDA drug label excerpt that would answer this question.
        Write it as if it came directly from official prescribing information.
        Use clinical language. 3-4 sentences maximum.

        Question: {question}
        Answer:"""
    response = requests.post(
        f'{OLLAMA_URL}/api/generate',
        json = {"model":"mistral","prompt":prompt,"stream":False}                    
                             
    )
    return response.json()['response']

