# Найти ошыбку в коде:

from flask import Flask

app = Flask(__name__)

@app.route(")
def index():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)

# Ошибка в декораторе маршрута. Строка в @app.route не закрыта кавычкой.