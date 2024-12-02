def process_input_text(text):
    """Очистка и подготовка текста для анализа"""
    return text.lower()

def generate_report(matches):
    """Генерация отчета о совпадениях"""
    report = f"Обнаружено {len(matches)} совпадений:\n"
    for match in matches:
        report += f"- {match}\n"
    return report
