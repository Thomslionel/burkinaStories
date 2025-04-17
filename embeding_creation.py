import streamlit as st
import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
from mistralai import Mistral

# Charger les variables d'environnement
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")



# Initialiser le modèle d'embedding
embed_model = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Initialiser le client Mistral
client = Mistral(api_key=MISTRAL_API_KEY)



def load_documents_from_directory(directory_path):
    print("============= Chargement des documents depuis le répertoire =================")
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            with open(os.path.join(directory_path, filename), "r", encoding="utf-8-sig") as file:
                title = file.readline().strip()               
                story = file.read().strip()
                documents.append({"id": title, "text": story})
    return documents


def split_text(text, chunck_size = 1000, chunck_overlap = 20):
    chuncks = []
    start = 0
    while start < len(text):
        end = start + chunck_size
        chuncks.append(text[start:end])
        start = end - chunck_overlap
    return chuncks


directory_path = "./docs_rag"
documents = load_documents_from_directory(directory_path=directory_path)

# print(f"Loaded {len(documents)} documents")

chunked_documents = []

for doc in documents:
    chunks = split_text(doc["text"])
    print("====Splitting docs into chuncks ====")
    for i, chunck in enumerate(chunks):
        chunked_documents.append({"id" : doc["id"], "text" : chunck})

# print(f"Split documents into {len(chunked_documents)} chunks")


def get_embedding(text):
    try:
        response = embed_model([text])
        embedding = response[0]
        print("==========Generating embeddings...========")
        return embedding
    except Exception as e:
        print("Quota exceeded, waiting 60 seconds...")
        time.sleep(60)  # Attendre 60 secondes si la limite de requêtes est atteinte
        return get_embedding(text)
    except Exception as e:
        print(f"An error occurred: {e}")

for doc in tqdm(chunked_documents):
     print("==========Generating embeddings...========")
     doc["embedding"] = get_embedding(doc["text"])



for doc in chunked_documents:
    print("====Inserting chuncks into db....====")
    collection.upsert(
        ids=[doc["id"]], documents=[doc["text"]], embeddings=[doc["embedding"]]    
    )
