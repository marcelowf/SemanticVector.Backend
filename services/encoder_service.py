import logging
from fastapi import HTTPException, status
import numpy as np
from utils.preparation_and_segmentation import PreparationAndSegmentation
from utils.analysis_and_vectorization import AnalysisAndVectorization
from .redis_service import RedisService
import pickle

embed_model = None

class EncoderService:
    @staticmethod
    def set_model(model):
        global embed_model
        embed_model = model

    @staticmethod
    def encode_embedding(messages: list[str]):
        if embed_model is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Serviço de Embedding indisponível.")

        try:
            all_processed_texts = []
            
            for message in messages:
                normalized_text = PreparationAndSegmentation.normalize_line_breaks(message)
                sentences = PreparationAndSegmentation.split_sentences(normalized_text)

                if not sentences:
                    raise ValueError("Sentenças inválidas para geração de Embeddings.")

                windows = PreparationAndSegmentation.build_sliding_windows(sentences, window_size=4, overlap=2)
                windows_clean = AnalysisAndVectorization.clean_and_lemmatize_texts(windows)
                
                all_processed_texts.extend(windows_clean)

            embeddings = embed_model.encode(all_processed_texts)
            embeddings_list = embeddings.tolist()

            index_name = "default_index"
            
            for i, (text, emb) in enumerate(zip(all_processed_texts, embeddings)):
                key = f"{index_name}:{i}"
                RedisService.set(key, pickle.dumps({"text": text, "embedding": emb.tolist()}))

            return embeddings_list

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro inesperado na geração de Embeddings: {str(e)}")
