from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# Caminho do arquivo JSON
data_file = "data.json"

# Tenta carregar os dados do arquivo JSON, caso contrário, inicializa os dados com estrutura vazia.
try:
    with open(data_file, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {"contacts": [], "logs": []}

# Renderizar páginas
@app.route('/')
def index():
    return render_template('index.html')  # Página inicial (index.html)

@app.route('/edit_contacts')
def edit_contacts():
    return render_template('edit_contacts.html')  # Página de edição de contatos (edit_contacts.html)

# Rota para adicionar um novo contato com método POST
@app.route('/add_contact', methods=['POST'])
def add_contact():
    try:
        new_contact = request.json
        # Validação simples dos dados recebidos
        if 'name' not in new_contact or 'phone' not in new_contact:
            return jsonify({"error": "Nome e telefone são obrigatórios!"}), 400
        
        data["contacts"].append(new_contact)  # Adiciona o novo contato à lista
        save_data()  # Salva os dados atualizados no arquivo JSON
        return jsonify({"message": "Contato adicionado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para obter todos os contatos com método GET
@app.route('/get_contacts', methods=['GET'])
def get_contacts():
    return jsonify(data["contacts"])  # Retorna os contatos armazenados no JSON

@app.route('/edit_contacts/<int:index>', methods=['PUT'])
def edit_contact(index):
    try:
        updated_contact = request.json  # Dados do contato atualizado
        # Verifique se os campos necessários estão presentes no corpo da requisição
        if not updated_contact or 'name' not in updated_contact or 'phone' not in updated_contact:
            return jsonify({"error": "Dados inválidos, 'name' e 'phone' são obrigatórios."}), 400

        print(f"Recebendo dados para o contato de índice {index}: {updated_contact}")  # Print de depuração

        if 0 <= index < len(data["contacts"]):
            # Atualiza o contato na posição indicada pelo 'index'
            data["contacts"][index] = updated_contact
            save_data()  # Salva os dados atualizados no arquivo JSON
            return jsonify({"message": "Contato atualizado com sucesso!"}), 200
        else:
            return jsonify({"error": "Contato não encontrado"}), 404

    except Exception as e:
        print(f"Erro ao processar a requisição: {str(e)}")  # Print de erro no backend
        return jsonify({"error": f"Erro ao processar a requisição: {str(e)}"}), 500




# Função para salvar os dados atualizados no arquivo JSON
def save_data():
    try:
        # Certifique-se de que o caminho do arquivo está correto
        with open(data_file, "w") as f:
            json.dump(data, f, indent=4)  # Salva os dados no arquivo com formatação
        print("Dados salvos com sucesso!")  # Mensagem de confirmação no console
    except Exception as e:
        print(f"Erro ao salvar dados: {str(e)}")  # Exibe o erro, se houver

# Rota para apagar um contato pelo índice
@app.route('/delete_contact/<int:index>', methods=['DELETE'])
def delete_contact(index):
    try:
        if 0 <= index < len(data["contacts"]):
            # Remove o contato da lista
            data["contacts"].pop(index)
            save_data()  # Salva os dados no arquivo JSON
            return jsonify({"message": "Contato deletado com sucesso!"}), 200
        else:
            return jsonify({"error": "Contato não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/selecao')
def selecao():
    return render_template('selecao.html')

import urllib.parse

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.json
        contacts = data.get("contacts")
        message = data.get("message")

        # URL encode the message to handle special characters
        encoded_message = urllib.parse.quote(message)

        # Para cada contato, você pode gerar a URL do WhatsApp
        links = []
        for contact in contacts:
            whatsapp_link = f"https://wa.me/{contact}?text={encoded_message}"
            links.append(whatsapp_link)

        return jsonify({"message": "Mensagens enviadas com sucesso!", "links": links}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao enviar mensagens: {str(e)}"}), 500









# Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True)

