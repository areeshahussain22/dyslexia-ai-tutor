import unittest
import sys
from pathlib import Path

# Add project root directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.rag.chunker import Chunker
from src.rag.document_loader import DocumentLoader

class TestRAGPipeline(unittest.TestCase):
    def setUp(self):
        self.loader = DocumentLoader()
        self.chunker = Chunker(chunk_size=100, chunk_overlap=20)

    def test_text_loader(self):
        test_file = Path(__file__).resolve().parent / "test_sample.txt"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Hello world, this is study content.")
            
        content = self.loader.load_text(str(test_file))
        self.assertEqual(content, "Hello world, this is study content.")
        
        # Cleanup
        if test_file.exists():
            test_file.unlink()

    def test_chunker_splitting(self):
        text = "This is a long string of test content used to evaluate text chunk boundary splitting."
        chunks = self.chunker.split_text(text)
        self.assertTrue(len(chunks) > 0)
        self.assertEqual(chunks[0]["chunk_id"], "chunk_0")

if __name__ == "__main__":
    unittest.main()
