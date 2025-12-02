import requests
import json

AUTH_CREDENTIALS = ('admin', 'password')
HEADERS = {'Content-Type': 'application/json'}

while True:
    a = input(" 1./items\n 2.items/<id>\n Enter number: ")
    if a == "2":
        b = input("Enter ID: ")
        
    c = int(input("\n METHOD: \n  1.GET\n  2.POST \n  3.PUT\n  4.DELETE \n Enter number: "))

    if c == 2 or c == 3:
        test_json = input("Write your data here:") # Якщо порожньо, то використовуються готові дані
        if test_json == "":
            test_json = {
                "id": 1,
                "name": "mouse",
                "price": 222
            }

    url = "http://127.0.0.1:8000/items"
    if a == "2":
        url += "/" + b


    if c == 1:
        response = requests.get(url, auth=AUTH_CREDENTIALS)

    elif c == 2:
        response = requests.post(
                url, 
                json=test_json, 
                auth=AUTH_CREDENTIALS,
                headers=HEADERS
            )
    elif c == 3:
        response = requests.put(
                url, 
                json=test_json, 
                auth=AUTH_CREDENTIALS,
                headers=HEADERS
            )  
    elif c == 4: 
        response = requests.delete(url, auth=AUTH_CREDENTIALS)
    try:
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except requests.exceptions.JSONDecodeError:
        print("\n", response.text, "\n")
