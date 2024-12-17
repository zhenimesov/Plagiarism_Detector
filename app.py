from flask import Flask, request, render_template
from plagiarism.detector import PlagiarismDetector
from plagiarism.utils import *

app = Flask(__name__)
detector = PlagiarismDetector(json_db_path="data/documents.json")

# Главная страница с формой для ввода текста
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Обработка POST-запроса с текстом для проверки
@app.route("/check", methods=["POST"])
def check():
    # Получаем текст из формы
    input_text = process_input_text(request.form["query"])

    # Ищем совпадения с фильтрацией по порогу схожести
    results = detector.find_matches(input_text, similarity_threshold=10.0)

    # Отправляем результаты на страницу с результатами
    return render_template("result.html", input_text=input_text, results=results)


if __name__ == "__main__":
    app.run(debug=True)
