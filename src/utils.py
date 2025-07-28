from sentence_transformers import SentenceTransformer
import numpy as np

def load_embedding_model(model_dir):
    return SentenceTransformer(model_dir)

def embed_text(text_list, model):
    return model.encode(text_list, convert_to_numpy=True, show_progress_bar=False)

def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
