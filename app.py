from flask import Flask, request, render_template, jsonify
from plagiarism.detector import PlagiarismDetector
from plagiarism.utils import *
from plagiarism.json_parser_handler import *
import logging

app = Flask(__name__)
DATA_FILE = "data/documents.json"
detector = PlagiarismDetector(json_db_path=DATA_FILE)
json_handler = JsonParserHandler(DATA_FILE)
# app.config['MAX_CONTENT_LENGTH'] = 10024 * 1024 * 1024  # 200 мегабайт
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Лимит 100 MB
logging.basicConfig(level=logging.DEBUG)

# Главная страница с формой для ввода текста
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "Request data is too large!"}), 413

@app.before_request
def log_request():
    logging.debug(f"Request size: {request.content_length}")

# Обработка POST-запроса с текстом для проверки
@app.route("/check", methods=["POST"])
def check():
    # Получаем текст из формы
    input_text = process_input_text(request.form["query"])

    # Ищем совпадения с фильтрацией по порогу схожести
    results = detector.find_matches(input_text, similarity_threshold=10.0)

    # Отправляем результаты на страницу с результатами
    return render_template("result.html", input_text=input_text, results=results)

# Маршрут для отображения формы
@app.route('/add', methods=['GET'])
def add_page():
    return render_template('add.html')

# Для добавление документа в базу данных:
@app.route('/add', methods=['POST'])
def handle_add():
    title = request.form.get('document_name')
    content = request.form.get('document_content')

    if not title or not content:
        return jsonify({"status": "error", "message": "Все поля должны быть заполнены."}), 400

    # Используем класс для добавления документа
    new_document = json_handler.add_document(title, content)

    # Обновляем список документов в детекторе
    detector.refresh_documents()

    # return jsonify({"status": "success", "data": new_document})
    return render_template('index.html')

@app.route('/history', methods=['GET'])
def view_history():
    """Маршрут для просмотра истории операций."""
    history = json_handler.load_history()
    return render_template("history.html", history=history)



if __name__ == "__main__":
    # Увеличиваем максимальный размер запроса
    # app.config['MAX_CONTENT_LENGTH'] = 10024 * 1024 * 1024  # 200 мегабайт
    app.run(debug=True)
