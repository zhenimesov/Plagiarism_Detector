import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import faiss

class PlagiarismDetector:
    def __init__(self, faiss_index_path=None, json_db_path="documents.json"):
        self.faiss_index = None
        self.json_db_path = json_db_path
        self.documents = self.load_json_database()

        if faiss_index_path:
            self.faiss_index = faiss.read_index(faiss_index_path)

        self.vectorizer = TfidfVectorizer()

    def load_json_database(self):
        """Загрузка документов из JSON-базы."""
        try:
            with open(self.json_db_path, "r", encoding="utf-8") as f:
                return json.load(f)  # Загружаем JSON из файла
        except FileNotFoundError:
            print(f"Файл базы данных {self.json_db_path} не найден.")
            return []

    def refresh_documents(self):
        """Обновляет внутренний список документов из JSON-базы."""
        self.documents = self.load_json_database()

    def find_matches(self, query_text, similarity_threshold=10.0):
        """Поиск совпадений с использованием JSON-базы и фильтрация по порогу схожести."""
        if not self.documents:
            return []

        # Сбор текста документов
        texts = [doc["content"] for doc in self.documents]

        # Векторизация текста
        vectors = self.vectorizer.fit_transform(texts + [query_text])
        query_vector = vectors[-1]
        document_vectors = vectors[:-1]

        # Расчет схожести
        similarities = cosine_similarity(query_vector, document_vectors).flatten()

        # Формирование результата с фильтрацией по порогу схожести
        results = []
        for i, similarity in enumerate(similarities):
            if similarity * 100 > similarity_threshold:  # Фильтруем по схожести
                results.append({
                    "document_id": self.documents[i]["id"],
                    "title": self.documents[i]["title"],
                    "content": self.documents[i]["content"],
                    "similarity": round(similarity * 100, 2)
                })
        return sorted(results, key=lambda x: x["similarity"], reverse=True)


