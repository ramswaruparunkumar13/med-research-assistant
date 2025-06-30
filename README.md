Medical Research Assistant
A simple implementation of an AI-powered tool to fetch, summarize, and semantically organize medical research papers from PubMed. Designed to help clinicians, researchers, and students quickly access concise, relevant insights from the ever-growing body of clinical literature.

~~Features
Keyword-based paper search from PubMed using E-utilities API  
AI-powered summarization using BART, prompted for clinical relevance  
Semantic similarity search using SentenceTransformers and FAISS  
Local persistence of embeddings and metadata  
Avoids re-processing already stored papers  
Smart fallback shows related papers from your database when no new papers are found

~~Requirements
All dependencies are listed in requirements.txt. Key packages include:
transformers, torch: for BART-based summarization
requests: for API interaction
sentence-transformers, faiss-cpu: for vector embeddings and similarity search

~~Setup Instructions(for Linux/macOS)
~~Extract the project

unzip med_research_assistant.zip
cd med_research_assistant

~~Run setup script

source setup.sh

~~Run the agent

python main.py

~~Setup for cmd(windows) // (dont recommend it!!)
cd "path of med_research_assistant"
pip install -r requirements.txt
python main.py

~~Usage(example)

    $ python main.py
    Enter a healthcare keyword to search papers or 'exit': cancer

    Summarizing paper: Cancer Immunotherapy: Recent Advances (2021)

    Summary:
    This study investigates immune checkpoint inhibitors in metastatic melanoma..

    Related papers based on summary similarity:
    - Novel PD-1 therapies in oncology (2020)

~Architecture
User Keyword - PubMed API (E-Search + E-Fetch)
            - Select Valid Abstract
            - Summarize using BART (with clinical prompt)
            - Generate Embedding via SentenceTransformer
            - Store Embedding + Metadata in FAISS + JSON
            - Search for similar papers by semantic similarity


Summarization
Model: facebook/bart-large-cnn
Framework: Hugging Face Transformers
Generates structured summaries of up to ~130 tokens

Storage and Similarity
Embeddings generated using sentence-transformers (all-MiniLM-L6-v2)
Stored in a faiss.IndexFlatL2 index on disk 
Metadata (PaperID and summary) stored in cve_metadata.json
Similarity search uses nearest neighbor search on summary embeddings

Testing(for feedback during dev)
Consists of simple integration tests desinged mainly for development and validation purposes. These tests verify key functionalities such as semantic search using FAISS and text summarization with Hugging Face BART model.

Scalability
A production-ready version could scale in several directions:
Backend Service: Wrap core logic in a REST API to support integration into clinical dashboards or research tools.
Database Upgrade: Swap local JSON/FAISS storage for scalable alternatives like PostgreSQL + a managed vector DB (e.g., Pinecone, Weaviate).
Model Enhancements: Replace off-the-shelf models with domain-specific ones (e.g., BioBERT, ClinicalBERT) for higher relevance in specialized contexts.
Multi-user Support: Add authentication and user-specific storage for team or institutional use.
Deployment: Containerize the app with Docker and deploy to the cloud (e.g., AWS/GCP) for broader access and reliability.








