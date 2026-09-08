import os
import chromadb
from sentence_transformers import SentenceTransformer

class RAGRetriever:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="chroma_db")
        self.collection = self.client.get_or_create_collection(
            name="course_materials"
        )
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")

    def add_documents(self, chunks, source):
        ids = [f"{source}-{i}" for i in range(len(chunks))]
        embeddings = self.encoder.encode(chunks).tolist()

        self.collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=[{"source": source} for _ in chunks]
        )

    def search(self, query, top_k=4):
        if self.collection.count() == 0:
            return []

        embedding = self.encoder.encode([query]).tolist()
        result = self.collection.query(
            query_embeddings=embedding,
            n_results=min(top_k, self.collection.count())
        )
        return result.get("documents", [[]])[0]
