import faiss
import numpy as np
import pickle

faiss_index: faiss.IndexFlatL2 = None
book_id_to_idx: dict[int, int] = {}
idx_to_book_id: dict[int, int] = {}

def load_index(index_path: str, mapping_path: str):
    global faiss_index, book_id_to_idx, idx_to_book_id

    faiss_index = faiss.read_index(index_path)

    with open(mapping_path, "rb") as f:
        mappings = pickle.load(f)
        book_id_to_idx = mappings["book_id_to_idx"]
        idx_to_book_id = mappings["idx_to_book_id"]

    print(f"✅ Loaded FAISS index with {faiss_index.ntotal} vectors")
    print(f"✅ Loaded {len(book_id_to_idx)} book mappings")

