from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    # Возвращаем простой текст, который точно считается всеми сервисами
    return "OK", 200 

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()