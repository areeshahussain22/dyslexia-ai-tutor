"""
Document loader service for importing study files.
Extracts raw text from sources such as PDFs and plain text files.
"""
from pathlib import Path
from pypdf import PdfReader

class DocumentLoader:
    def __init__(self):
        """Initialize the document loader."""
        pass
        
    def load_pdf(self, file_path: str) -> str:
        """
        Extracts raw text content from a PDF file using pypdf.
        
        Args:
            file_path (str): The absolute path to the PDF document.
            
        Returns:
            str: Combined text content of all pages.
        """
        try:
            reader = PdfReader(file_path)
            texts = []
            for page in reader.pages:
                text = page.extract_text() or ""
                if text.strip():
                    texts.append(text.strip())
            return "\n\n".join(texts)
        except Exception as exc:
            return f"Error extracting PDF text: {exc}"
        
    def load_text(self, file_path: str) -> str:
        """
        Extracts raw text content from a plain text file.
        
        Args:
            file_path (str): The path to the text file.
            
        Returns:
            str: Text content of the file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"
