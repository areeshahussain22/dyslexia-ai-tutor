"""
Text chunking utility for splitting large documents into semantically coherent overlapping segments.
"""
from typing import List, Dict, Any

class Chunker:
    def __init__(self, chunk_size: int = 600, chunk_overlap: int = 120):
        """
        Initialize the text chunker.
        
        Args:
            chunk_size (int): Max character count of each chunk.
            chunk_overlap (int): Inter-chunk character overlap.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Splits text into overlapping segments at paragraph or sentence boundaries.
        
        Args:
            text (str): Raw string text of the document.
            
        Returns:
            List[Dict[str, Any]]: List of chunk dicts containing chunk text and offsets.
        """
        # TODO: Implement robust semantic boundary parsing
        chunks = []
        text_len = len(text)
        start = 0
        chunk_idx = 0
        
        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            chunk_text = text[start:end]
            chunks.append({
                "chunk_id": f"chunk_{chunk_idx}",
                "text": chunk_text,
                "start_char": start,
                "end_char": end
            })
            start += (self.chunk_size - self.chunk_overlap)
            chunk_idx += 1
            
        return chunks
