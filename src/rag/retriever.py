"""
Retriever service coordinating EmbeddingService and VectorStore.
Performs end-to-end question answering retrieval from plain queries.
"""
from typing import List, Dict, Any
from src.rag.embedding_service import EmbeddingService
from src.rag.vector_store import VectorStore

class Retriever:
    def __init__(self, embedding_service: EmbeddingService, vector_store: VectorStore):
        """
        Initialize the retriever coordination system.
        
        Args:
            embedding_service (EmbeddingService): Service to embed textual queries.
            vector_store (VectorStore): ChromaDB client wrapper.
        """
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Processes a natural language query, generates its vector embedding,
        and retrieves similar content chunks.
        
        Args:
            query (str): Learner's query or target topic.
            top_k (int): Number of chunks to retrieve.
            
        Returns:
            List[Dict[str, Any]]: List of matching text chunks.
        """
        # TODO: Implement retrieval workflow with fallback default search
        query_vector = self.embedding_service.get_embedding(query)
        return self.vector_store.query_similar(query_vector, top_k=top_k)
