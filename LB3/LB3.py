from flask import Flask, request, jsonify
import requests, os, json, base64

TEXT_FILE_PATH = 'passwords.json'  # файл з логінами та паролями
FILE_PATH = 'inventory.json'       # каталог товарів

def load_inventory():
    # Зчитує дані з JSON-файлу і повертає список товарів
    if not os.path.exists(FILE_PATH) or os.path.getsize(FILE_PATH) == 0:
        return []
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_inventory(data):
    # Зберігає список товарів у JSON-файл
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def check_auth():
    # Перевірка автентифікації
    frmt = request.headers.get('Authorization', '')
    if not frmt:
        return 0
    encdt = frmt.split(' ')[1]
    decdt = base64.b64decode(encdt).decode('utf-8')
    with open(TEXT_FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for i in data:
        pswd = i['login'] + ':' + i['password']
        if decdt == pswd:
            return 1
    return 0
     
     
app = Flask(__name__)

@app.route("/items", methods=['GET', 'POST']) 
def all_info():
    
    if not check_auth():
        return jsonify({"error": "Not Authenticated"}), 404
    
    if request.method == "GET":
       return load_inventory()
        
    elif request.method == "POST":
        json_data = request.json 
        ctlg = load_inventory()
        if not json_data:
            return jsonify({"error": "No data in body"}), 400

        json_data['id'] = ctlg[-1]['id'] + 1
        ctlg.append(json_data)
        save_inventory(ctlg)
        return jsonify({"OK": "Data received"}), 201
        

@app.route("/items/<iid>", methods=['GET', 'PUT', 'DELETE']) 
def get_item(iid):

    if not check_auth():
        return jsonify({"error": "Not Authenticated"}), 404
        
    all_data = load_inventory()      
   
       
    if request.method == "GET":
        for i in all_data:
            if i['id'] == int(iid):
                return i
        return jsonify({"error": "No data received"}), 404
        
    elif request.method == "PUT":
        json_data = request.json 
        for i in all_data:
            if i['id'] == int(iid):                  
                i['name'] = json_data.get('name', i['name']) 
                i['price'] = json_data.get('price', i['price'])  
                save_inventory(all_data)
                return jsonify({"OK": "Data received"}), 201
        return jsonify({"error": "Incorrect data received"}), 404  
  
    elif request.method == "DELETE":
        for i in all_data:
            if i['id'] == int(iid):
                all_data.remove(i)
                save_inventory(all_data)
                return jsonify({"OK": "Data received"}), 201
        return jsonify({"error": "No ID found"}), 404


if __name__ == '__main__': 
    app.run(port=8000) 
