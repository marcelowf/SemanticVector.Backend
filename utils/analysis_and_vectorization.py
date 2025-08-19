import spacy
nlp = spacy.load("pt_core_news_sm")   
stop_words = nlp.Defaults.stop_words

class AnalysisAndVectorization:    
    # @staticmethod
    async def clean_and_lemmatize_texts(texts: list) -> list:
        cleaned = []
        for doc in nlp.pipe(texts, disable=['parser','ner']):
            tokens = []
            for token in doc:
                if token.is_alpha and token.lemma_.lower() not in stop_words:
                    tokens.append(token.lemma_.lower())
            cleaned.append(" ".join(tokens))
        return cleaned

    # async def extract_entities(sentences: list) -> dict:
    #     entities = {}
    #     for doc in nlp.pipe(sentences, disable=['parser']):
    #         for ent in doc.ents:
    #             key = ent.text.strip()
    #             entities.setdefault(key, []).append(doc.text)
    #     return entities

    # async def build_tfidf(texts_clean: list) -> (TfidfVectorizer, np.ndarray):
    #     vectorizer = TfidfVectorizer(ngram_range=(1,2), sublinear_tf=True)
    #     tfidf_matrix = vectorizer.fit_transform(texts_clean)
    #     return vectorizer, tfidf_matrix
