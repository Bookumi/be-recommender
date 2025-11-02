from surprise import SVD
import pickle

svd_model: SVD | None = None
user_items: dict[int, list[int]] | None = None

def load_svd_and_user_items_dict(file_path: str):
  global svd_model, user_items

  with open(file_path, "rb") as f:
    data = pickle.load(f)
  
  svd_model = data["model"]
  user_items = data["train_user_items"]

  print("✅ Loaded SVD model and user-item mappings")
  print(f"Total users in training data: {len(user_items)}")
  if len(user_items) > 0:
        example_user = list(user_items.keys())[0]
        print(f"Example user: {example_user}, liked books: {user_items[example_user][:5]}")