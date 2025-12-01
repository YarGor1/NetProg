from flask import Flask, request, jsonify
from datetime import date, timedelta
import requests, os

app = Flask(__name__)

TEXT_FILE_PATH = 'data/plain_text_log.txt'

@app.route("/", methods=['GET', 'POST']) 
def hello_world():
    if request.method == "GET":
        return "Hello world!"
        
    elif request.method == "POST":
        # Отримання даних запиту як рядка (str)
        raw_text_data = request.get_data(as_text=True) 
        
        if not raw_text_data:
            return jsonify({"error": "В тілі запиту відсутні дані."}), 400

        # Запис даних у файл
        try:
            # Створюємо директорію, якщо вона не існує
            os.makedirs(os.path.dirname(TEXT_FILE_PATH), exist_ok=True)
            
            # Додати новий текст в кінець файлу
            with open(TEXT_FILE_PATH, 'a', encoding='utf-8') as f:
                f.write(raw_text_data + "\n")

            return jsonify({
                "message": "Текст успішно додано до файлу.",
            }), 201
            
        except Exception as e:
            # Обробка помилок запису
            return jsonify({"error": "Помилка при записі у файл"}), 500

@app.route("/currency", methods=['GET']) 
def get_currency():
    # http://localhost:8000/currency?time=today&value=usd
    qtime = request.args.get('time', '')
    qval = request.args.get('value', '')
    frmt = request.headers.get ('Content-Type', '')

    # Перевірка дати
    if qtime == "today":
        day = date.today()
    elif qtime == "yesterday":
        day = date.today() - timedelta(days=1)
    day = day.strftime("%Y%m%d")

    # Виконання API
    url_api = f"https://bank.gov.ua/NBU_Exchange/exchange_site?&json&valcode={qval}&start={day}&end={day}"
    api = requests.get(url_api)
    currency = api.json()
    if currency == []:
        return "No Data"
    rate = currency[0]['rate']

    # Без формату
    rez = f"{currency[0]['txt']} - {rate}"
    # Формат JSON
    if frmt == "application/json":
        rez = {"value": f"{qval}",
               "rate": f"{rate}"}
        rez = jsonify(rez)
    # Формат XML
    elif frmt == "application/xml":
         rez = f"""
<currency_data>
    <currency>{qval}</currency>
    <rate>{rate}</rate>
</currency_data>"""
    return rez

if __name__ == '__main__': 
    app.run(port=8000) 
