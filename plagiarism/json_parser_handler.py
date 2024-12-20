import os
import json
from datetime import datetime


class JsonParserHandler:
    def __init__(self, json_db_path, history_db_path="data/history.json"):
        """Инициализация класса с путями к JSON-файлам."""
        self.json_db_path = json_db_path
        self.history_db_path = history_db_path

    def load_data(self):
        """Загружает данные из JSON-файла."""
        if os.path.exists(self.json_db_path):
            with open(self.json_db_path, "r", encoding="utf-8") as file:
                return json.load(file)
        return []

    def save_data(self, data):
        """Сохраняет данные в JSON-файл."""
        with open(self.json_db_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def add_document(self, title, content):
        """Добавляет новый документ в JSON-файл и записывает в историю."""
        data = self.load_data()
        new_id = max((item["id"] for item in data), default=0) + 1
        new_document = {"id": new_id, "title": title, "content": content}
        data.append(new_document)
        self.save_data(data)

        # Сохраняем операцию в историю добавлений
        self.add_to_history("additions", f"Добавлен документ: {title}")
        return new_document

    def add_to_history(self, category, operation, details=None):
        """Добавляет запись в историю операций."""
        history = self.load_history()
        if category not in history:
            history[category] = []

        history[category].append({
            "operation": operation,
            "details": details or {},
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        with open(self.history_db_path, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4, ensure_ascii=False)

    def load_history(self):
        """Загружает историю операций."""
        if os.path.exists(self.history_db_path):
            with open(self.history_db_path, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}
