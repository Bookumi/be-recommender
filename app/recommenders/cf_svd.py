from surprise import SVD
from typing import Optional
import pickle

svd_model: Optional[SVD] = None
user_items: Optional[dict[int, list[int]]] = None

def load_svd_and_user_items_dict(file_path: str):
  global svd_model, user_items

  with open(file_path, "rb") as f:
    data = pickle.load(f)
  
  svd_model = data["model"]
  user_items = data["train_user_items"]

  print("✅ Loaded SVD model and user-item mappings")
  print(f"Total users in training data: {len(user_items)}")
  if len(user_items) > 0:
        example_user = list(user_items.keys())[100]
        print(f"Example user: {example_user}, liked books: {user_items[example_user][:5]}")

def get_similiar_user(liked_books: list[int]) -> Optional[int]:
  if not user_items:
      return None
   
  bset_user = None
  best_overlap = 0

  for uid, books in user_items.items():
     overlap = len(set(books) & set(liked_books))
     if overlap > best_overlap:
        best_overlap = overlap
        best_user = uid
        
  return best_user 
