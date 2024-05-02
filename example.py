import requests

url = "http://127.0.0.1:5000/"

url += "encode"  # Зашифровать
# url += "decode"  # Расшифровать

json_body = {
    "message": "Ваше сообщение"
    # ,
    # "key": "Ключ для расшифровки" # Нужен только для расшифровки, при шифровании создается новый ключ
}

response = requests.post(url, json=json_body)
print(response.json())
