import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class GenerationAndOptimization:
    @staticmethod
    def load_sentence_embedding_model(model_name: str):
        return SentenceTransformer(model_name)

    @staticmethod
    def build_sentence_embeddings(texts: list, model: SentenceTransformer) -> np.ndarray:
        embs = model.encode(texts, convert_to_tensor=False, show_progress_bar=True)
        arr = np.array(embs, dtype='float32')
        return arr

    @staticmethod
    def build_faiss_index(embeddings: np.ndarray):
        faiss.normalize_L2(embeddings)
        d = embeddings.shape[1]
        index = faiss.IndexFlatIP(d)
        index.add(embeddings)
        return index