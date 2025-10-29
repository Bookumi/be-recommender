import faiss
import numpy as np
import pickle

faiss_index: faiss.IndexFlatL2 = None
book_id_mapping: dict[int, int] = {}

def load_index(index_path: str, mapping_path: str):
  global faiss_index, book_id_mapping

  faiss_index = faiss.read_index(index_path)

  with open(mapping_path, "rb") as f:
    book_id_mapping = pickle.load(f)
  
  print(f"Loaded FAISS index with {faiss_index.ntotal} vectors")

