import faiss
import numpy as np
import pickle

faiss_index_en: faiss.IndexFlatL2 = None
book_id_to_idx_en: dict[int, int] = {}
idx_to_book_id_en: dict[int, int] = {}

faiss_index_ind: faiss.IndexFlatL2 = None
book_id_to_idx_ind: dict[int, int] = {}
idx_to_book_id_ind: dict[int, int] = {}

def load_index(index_path_en: str, mapping_path_en: str, index_path_ind: str, mapping_path_ind: str):
    global faiss_index_en, book_id_to_idx_en, idx_to_book_id_en, faiss_index_ind, book_id_to_idx_ind, idx_to_book_id_ind

    faiss_index_en = faiss.read_index(index_path_en)

    with open(mapping_path_en, "rb") as f:
        mappings = pickle.load(f)
        book_id_to_idx_en = mappings["book_id_to_idx_en"]
        idx_to_book_id_en = mappings["idx_to_book_id_en"]

    print(f"✅ Loaded EN FAISS index with {faiss_index_en.ntotal} vectors")
    print(f"✅ Loaded {len(book_id_to_idx_en)} book_id_to_idx mappings")
    print(f"🔹 First 5 EN book_ids: {list(book_id_to_idx_en.keys())[:5]}")

    faiss_index_ind = faiss.read_index(index_path_ind)

    with open(mapping_path_ind, "rb") as f:
        mappings = pickle.load(f)
        book_id_to_idx_ind = mappings["book_id_to_idx_ind"]
        idx_to_book_id_ind = mappings["idx_to_book_id_ind"]

    print(f"✅ Loaded ID FAISS index with {faiss_index_ind.ntotal} vectors")
    print(f"✅ Loaded {len(book_id_to_idx_ind)} book_id_to_idx mappings")
    print(f"🔹 First 5 ID book_ids: {list(book_id_to_idx_ind.keys())[:5]}")

