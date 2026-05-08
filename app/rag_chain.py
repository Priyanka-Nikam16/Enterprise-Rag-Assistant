##This code will combine retrieval (context) and generation(response)

import os
from dotenv import load_dotenv
from groq import Groq
from app.retriever import retriever

load_dotenv()
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
    )
MODEL_NAME=os.getenv("MODEL_NAME","openai/gpt-oss-120b")

def generate_answer(query:str):
     """
    MAIN RAG Pipeline:
    1. Retrieve context from the retriever
    2. Build the prompt
    3. Generate response using the Groq client
    """
     
     #Step 1: Retrieve context
     context=retriever(query)

     #step 2: Build prompt
     prompt=f""" 
Context={context}
Question={query}


"""
     system_prompt=""""
     You are Retail Assistant, an AI system that answers customer queries about products, promotions, policies, and inventory. 
Always use the retrieved context from the knowledge base (product catalog, return policy, promotions flyer, inventory snapshot). 
If the answer is not found in the retrieved context, respond with: "I don’t know based on the available information."

Guidelines:
1. Be concise, clear, and customer-friendly.
2. Use exact product names, SKUs, and prices from the catalog.
3. For promotions, mention the discount type and product details.
4. For policies, quote the relevant rule from the document.
5. Never invent product details, offers, or policies.
6. If multiple matches exist, list them clearly.
7. If no relevant information is retrieved, say: "I don’t know."

     """
     #step 3: Generate response
     response=client.chat.completions.create(
          model=MODEL_NAME,
          messages=[
               {"role":"system","content":system_prompt},
               {"role":"user","content":prompt}
          ]
     )
     return response.choices[0].message.content