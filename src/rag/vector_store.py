"""
Vector database store interface using ChromaDB.
Handles storing, indexing, and executing similarity searches on text chunk embeddings.
"""
import chromadb
from typing import List, Dict, Any

class VectorStore:
    def __init__(self, db_path: str):
        """
        Initializes the ChromaDB persistent client.
        
        Args:
            db_path (str): File system directory path where vectors will be stored.
        """
        # TODO: Implement persistent Chroma client initialization
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection("lesson_chunks")

    def add_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]) -> None:
        """
        Adds text chunks with their precomputed embeddings to the vector store.
        
        Args:
            chunks (List[Dict[str, Any]]): Text chunk segments.
            embeddings (List[List[float]]): Corresponding high-dimensional vectors.
        """
        # TODO: Map chunks to document insertions
        ids = [c["chunk_id"] for c in chunks]
        documents = [c["text"] for c in chunks]
        metadatas = [{"start_char": c["start_char"], "end_char": c["end_char"]} for c in chunks]
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

    def query_similar(self, query_embedding: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Queries ChromaDB for the closest vector match.
        
        Args:
            query_embedding (List[float]): Vector embedding of the question/topic.
            top_k (int): Number of matches to return.
            
        Returns:
            List[Dict[str, Any]]: Relevant document matching chunks.
        """
        # TODO: Refine query retrieval with distance threshholding
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        formatted_results = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            ids = results["ids"][0]
            metas = results["metadatas"][0] if "metadatas" in results else [{}] * len(docs)
            for doc, id_, meta in zip(docs, ids, metas):
                formatted_results.append({
                    "chunk_id": id_,
                    "text": doc,
                    "metadata": meta
                })
        return formatted_results
