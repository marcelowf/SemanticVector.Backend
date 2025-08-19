import logging
from fastapi import HTTPException, status
from utils.preparation_and_segmentation import PreparationAndSegmentation
from utils.analysis_and_vectorization import AnalysisAndVectorization

embed_model = None

class EncoderService:
    @staticmethod
    def set_model(model):
        global embed_model
        embed_model = model

    @staticmethod
    def encode_embedding(message: str):
        if embed_model is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                detail="O serviço de embedding não está disponível. Tente novamente mais tarde."
            )

        try:
            text = PreparationAndSegmentation.normalize_line_breaks(message)
            sentences = PreparationAndSegmentation.split_sentences(text)

            if not sentences:
                raise ValueError("O texto de entrada não pôde ser segmentado em sentenças válidas.")

            windows = PreparationAndSegmentation.build_sliding_windows(sentences, window_size=4, overlap=2)
            windows_clean = AnalysisAndVectorization.clean_and_lemmatize_texts(windows)

            embeddings = embed_model.encode(windows_clean)
            embeddings_list = embeddings.tolist()
            return embeddings_list

        except ValueError as ve:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

        except Exception as e:
            logging.error(f"Erro inesperado durante a geração do embedding: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro interno no servidor.")