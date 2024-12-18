import os
import json

class JsonParserHandler:
    def __init__(self, json_db_path):
        """Инициализация класса с путем к JSON-файлу."""
        self.json_db_path = json_db_path

    def load_data(self):
        """Загружает данные из JSON-файла."""
        if os.path.exists(self.json_db_path):  # Проверяем существование файла
            with open(self.json_db_path, "r", encoding="utf-8") as file:
                return json.load(file)
        return []

    def save_data(self, data):
        """Сохраняет данные в JSON-файл."""
        with open(self.json_db_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def add_document(self, title, content):
        """Добавляет новый документ в JSON-файл."""
        data = self.load_data()
        new_id = max((item["id"] for item in data), default=0) + 1  # Генерация нового ID
        new_document = {"id": new_id, "title": title, "content": content}
        data.append(new_document)
        self.save_data(data)
        return new_document
