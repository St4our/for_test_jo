from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index() -> json:
    if request.method == "POST":
        data = request.get_json()
        # Здесь вы можете обработать данные, например, сохранить их в базе данных
        print(data) # Просто выводим данные в консоль для примера
        return jsonify({'status': 'success'})
    else:    
        return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
