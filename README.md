## Enterprise-Rag-Assistant

Enterprise Assistant is a Retrieval-Augmented Generation (RAG) system built for retail and enterprise use cases. It can answer queries about product catalogs (CSV) and business documents (PDF) by combining structured logic with semantic search powered by FAISS and SentenceTransformers.

This assistant supports:

- Product lookups by  name, or description
- Price-based queries
- Semantic search in multi-page PDFs (catalogs, handbooks, flyers)

## Configuration

Set your Groq API key in environment variables:
- export GROQ_API_KEY="your_api_key"
- MODEL=openai/gpt-oss-120b

## Usage
Run  : python app/ingest.py

Run the Streamlit app:
- streamlit run app.py

  
Open the app in your browser at http://localhost:8501.


## Sample Questions And Answers

PDF Handbook Queries:

Q: What does the Rewards Handbook say about point expiry?

A: Points expire after 24 months if unused.

Q: Summarize Gold tier benefits.

A: Gold members earn 1.5x points, get free shipping, and early access to sales.

Q: what is return process for electronics?

A: Electronics can be returned **within 15 days** of purchase.
Process:
Bring the item and a valid receipt/invoice (proof of purchase is mandatory).
Unopened electronics – eligible for a full refund.
Opened electronics – eligible only for an exchange (no refund).
If the return is due to a warranty issue, the claim must be processed through an authorized service‑center.
All returns must follow these steps and meet the 15‑day window.

CVS based Queries:

Q: what is the price of smartphone X200?

A: The Smartphone X200 is priced at **15,999**.

Q: what are products available in apparel?

A:**Apparel products:**
SKU: 2006 | Formal Blue Shirt | Price: 1299


## 📂 Project Structure

```bash
Enterprise-Rag-Assistant
│── app/                 
│   │── ingest.py          #Load data ,split, embed ,store in Faiss      
│   │── rag_chain.py       # Main Rag pipline      
│   │── retriever.py       #Retrieve the top k relevant document chunks from the vector store
│   
│── .env                  # Environment variables
│── requirements.txt      # Python dependencies
│── README.md             # Project documentation
│── .venv/                # Virtual environment
│── app.py               # Sreamlit Entry point (outside app folder)

SKU: 2015 | Winter Jacket | Price: 3499
SKU: 2001 | Classic White T‑Shirt | Price: 499
