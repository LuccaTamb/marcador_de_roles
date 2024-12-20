### ------------------------------------------------------------- ### 
### IMPORTAÇÕES
from flask import Flask, request, jsonify, render_template
import json
import os


### ------------------------------------------------------------- ### 
### FAZER FUNCIONAR
app = Flask(__name__)
data_file = "data.json" 
try:
    with open(data_file, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {"contacts": [], "logs": []}

### ------------------------------------------------------------- ### 
### FUNÇÃO PARA SALVAR OS DADOS
def save_data():
    try:
        with open(data_file, "w") as f:
            json.dump(data, f, indent=4) 
        print("Dados salvos com sucesso!")  
    except Exception as e:
        print(f"Erro ao salvar dados: {str(e)}") 


### ------------------------------------------------------------- ### 
### OBTER TODOS OS CONTATOS
@app.route('/get_contacts', methods=['GET'])
def get_contacts():
    return jsonify(data["contacts"]) 


### ------------------------------------------------------------- ### 
### RENDER DA PAGINA
@app.route('/') #index.html
def index():
    return render_template('index.html')  

@app.route('/edit_contacts') #edit_contacts.html
def edit_contacts():
    return render_template('edit_contacts.html')  

@app.route('/selecao') #selecao.html
def selecao():
    return render_template('selecao.html')


### ------------------------------------------------------------- ### 
### ADICIONAR NOVO CONTATO
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
    

### ------------------------------------------------------------- ### 
### EDITAR CONTATOS
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


### ------------------------------------------------------------- ### 
### APAGAR CONTATO
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


### ------------------------------------------------------------- ### 
### 

### ------------------------------------------------------------- ### 
### 



### ------------------------------------------------------------- ### 
### ENVIAR MENSAGEM

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


### ------------------------------------------------------------- ### 

# Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True)