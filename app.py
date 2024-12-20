from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# Inicializa ou carrega os dados do JSON
data_file = "data.json"
try:
    with open(data_file, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {"contacts": [], "logs": []}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_contact', methods=['POST'])
def add_contact():
    new_contact = request.json
    data["contacts"].append(new_contact)
    save_data()
    return jsonify({"message": "Contato adicionado com sucesso!"}), 201

@app.route('/get_contacts', methods=['GET'])
def get_contacts():
    return jsonify(data["contacts"])

@app.route('/log_activity', methods=['POST'])
def log_activity():
    log_entry = request.json
    data["logs"].append(log_entry)
    save_data()
    return jsonify({"message": "Log registrado."}), 201

def save_data():
    with open(data_file, "w") as f:
        json.dump(data, f)

if __name__ == '__main__':
    app.run(debug=True)
