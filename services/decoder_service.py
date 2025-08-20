import json
import logging
import pickle
import numpy as np
from fastapi import HTTPException, status
from .redis_service import RedisService
from utils.preparation_and_segmentation import PreparationAndSegmentation
from utils.analysis_and_vectorization import AnalysisAndVectorization

embed_model = None

def deserialize(value: bytes):
    try:
        return pickle.loads(value)
    except Exception:
        try:
            return json.loads(value.decode("utf-8"))
        except Exception:
            return None

class DecoderService:
    @staticmethod
    def set_model(model):
        global embed_model
        embed_model = model

    @staticmethod
    async def decode_embedding(message: str):
        if embed_model is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Serviço de Embedding indisponível.")

        try:
            normalized_text = PreparationAndSegmentation.normalize_line_breaks(message)
            sentences = PreparationAndSegmentation.split_sentences(normalized_text)

            if not sentences:
                raise ValueError("Sentenças inválidas para decodificação.")

            windows = PreparationAndSegmentation.build_sliding_windows(sentences, window_size=4, overlap=2)
            windows_clean = AnalysisAndVectorization.clean_and_lemmatize_texts(windows)
            
            if not windows_clean:
                return "Nenhum texto processado para decodificação."
                
            input_embedding = embed_model.encode(windows_clean[0])
            input_embedding = np.array(input_embedding)

            similarity_threshold = 0.75 

            keys = RedisService.get_all_keys("default_index:*")
            keys = [k for k in keys if k != "default_index:counter"]

            if not keys:
                return {"message": "Nenhum dado encontrado para decodificação."}

            serialized_data_list = RedisService.mget(keys)
            
            results = []
            
            for serialized_data in serialized_data_list:
                if not serialized_data:
                    continue

                data = deserialize(serialized_data)
                if not data or "embedding" not in data:
                    continue

                try:
                    db_embedding = np.array(data["embedding"])
                    
                    similarity = np.dot(input_embedding, db_embedding) / (np.linalg.norm(input_embedding) * np.linalg.norm(db_embedding))
                    
                    if similarity >= similarity_threshold:
                        results.append({"similarity": similarity, "original_text": data.get("original_text", data.get("text"))})
                except Exception as e:
                    logging.warning(f"Erro ao processar um embedding: {e}")
                    continue

            results.sort(key=lambda x: x["similarity"], reverse=True)
            top_5_results = results[:5]

            if top_5_results:
                return {"results": top_5_results}
            else:
                return {"message": "Nenhum texto similar encontrado acima do limiar."}

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro inesperado na decodificação de Embeddings: {str(e)}")
