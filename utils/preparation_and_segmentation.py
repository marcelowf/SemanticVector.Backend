import re
import spacy
nlp = spacy.load("pt_core_news_sm") 

if "sentencizer" not in nlp.pipe_names:
    nlp.add_pipe('sentencizer')

class PreparationAndSegmentation:
    @staticmethod
    def normalize_line_breaks(text: str) -> str:
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text

    @staticmethod
    def split_sentences(text: str) -> list:
        sentences = []
        for doc in nlp.pipe([text], disable=['parser', 'ner']):
            for sent in doc.sents:
                txt = sent.text.strip()
                if txt:
                    sentences.append(txt)
        return sentences

    @staticmethod
    def build_sliding_windows(sentences: list, window_size: int = 4, overlap: int = 2) -> list:
        windows = []
        for i in range(0, len(sentences), window_size - overlap):
            win = sentences[i:i+window_size]
            if win:
                windows.append(" ".join(win))
        return windows