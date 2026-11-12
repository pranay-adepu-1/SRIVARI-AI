import math
import re
from typing import List, Dict, Any, Tuple
from collections import Counter

class HybridSearchEngine:
    """
    Lightweight, high-performance hybrid vector and BM25 search engine
    optimized for English and Telugu devotional vocabulary.
    """
    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.doc_term_freqs: List[Counter] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_length: float = 0.0
        self.idf: Dict[str, float] = {}
        self.vocab: Dict[str, int] = {}

    def _tokenize(self, text: str) -> List[str]:
        if not text:
            return []
        # Support Telugu Unicode \u0C00-\u0C7F and alphanumeric
        tokens = re.findall(r'[\u0C00-\u0C7Fa-zA-Z0-9]+', text.lower())
        return [t for t in tokens if len(t) > 1]

    def index_documents(self, docs: List[Dict[str, Any]]) -> None:
        """
        Indices documents with title, content, and metadata.
        """
        self.documents = docs
        self.doc_term_freqs = []
        self.doc_lengths = []
        doc_count = len(docs)
        if doc_count == 0:
            return

        df = Counter()
        for doc in docs:
            combined_text = f"{doc.get('title_en', '')} {doc.get('title_te', '')} {doc.get('content_en', '')} {doc.get('content_te', '')}"
            tokens = self._tokenize(combined_text)
            tf = Counter(tokens)
            self.doc_term_freqs.append(tf)
            self.doc_lengths.append(len(tokens))
            for word in tf.keys():
                df[word] += 1

        self.avg_doc_length = sum(self.doc_lengths) / max(1, doc_count)
        
        # Calculate BM25 IDF
        self.idf = {}
        for word, freq in df.items():
            self.idf[word] = math.log(1.0 + (doc_count - freq + 0.5) / (freq + 0.5))

    def search(self, query: str, top_k: int = 4, k1: float = 1.5, b: float = 0.75) -> List[Tuple[Dict[str, Any], float]]:
        """
        Returns top_k documents scored by hybrid BM25 and term overlap.
        """
        if not self.documents:
            return []

        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        scores = [0.0] * len(self.documents)

        for i, tf in enumerate(self.doc_term_freqs):
            doc_len = self.doc_lengths[i]
            score = 0.0
            for token in query_tokens:
                if token in tf:
                    freq = tf[token]
                    idf_val = self.idf.get(token, 0.1)
                    numerator = freq * (k1 + 1.0)
                    denominator = freq + k1 * (1.0 - b + b * (doc_len / max(1.0, self.avg_doc_length)))
                    score += idf_val * (numerator / max(0.001, denominator))
            
            # Boost matches in titles
            doc = self.documents[i]
            title_text = f"{doc.get('title_en', '')} {doc.get('title_te', '')}".lower()
            for token in query_tokens:
                if token in title_text:
                    score += 2.0

            scores[i] = score

        ranked_indices = sorted(range(len(scores)), key=lambda idx: scores[idx], reverse=True)
        results = []
        for idx in ranked_indices[:top_k]:
            if scores[idx] > 0.1:
                results.append((self.documents[idx], scores[idx]))

        return results

search_engine = HybridSearchEngine()

