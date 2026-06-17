"""
Content Ingestion Agent.
Coordinates the RAG ingestion pipeline: loads files, splits text into chunks,
generates embeddings, and indexes them in ChromaDB.
"""
from typing import Dict, Any, List
from src.rag.document_loader import DocumentLoader
from src.rag.chunker import Chunker
from src.rag.embedding_service import EmbeddingService
from src.rag.vector_store import VectorStore

class ContentIngestionAgent:
    def __init__(self, document_loader: DocumentLoader, chunker: Chunker, 
                 embedding_service: EmbeddingService, vector_store: VectorStore):
        """
        Initializes the Ingestion Agent.
        
        Args:
            document_loader (DocumentLoader): Extracts text from files.
            chunker (Chunker): Splits text into chunks.
            embedding_service (EmbeddingService): Generates vector representations.
            vector_store (VectorStore): Handles vector queries and updates.
        """
        self.document_loader = document_loader
        self.chunker = chunker
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        
    def ingest_document(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Loads a document, chunks it, generates embeddings, and indexes it in the vector store.
        
        Args:
            file_path (str): Path to the target study file.
            
        Returns:
            List[Dict[str, Any]]: List of metadata-loaded text chunks created.
        """
        # TODO: Handle multi-page PDF tables or complex document metadata parsing
        if file_path.endswith(".pdf"):
            raw_text = self.document_loader.load_pdf(file_path)
        else:
            raw_text = self.document_loader.load_text(file_path)
            
        chunks = self.chunker.split_text(raw_text)
        chunk_texts = [c["text"] for c in chunks]
        
        embeddings = self.embedding_service.get_embeddings(chunk_texts)
        self.vector_store.add_chunks(chunks, embeddings)
        
        return chunks
