// Função para carregar contatos da API
async function loadContacts() {
    try {
        const response = await fetch('/get_contacts');
        const contacts = await response.json();
        const contactsList = document.getElementById('contactsList');
        contactsList.innerHTML = ''; // Limpa a lista antes de adicionar novos contatos

        contacts.forEach((contact, index) => {
            const listItem = document.createElement('li');
            listItem.classList.add('contact-item');
            listItem.innerHTML = `
                Nome: ${contact.name}, Telefone: ${contact.phone}
                <button onclick="editContact(${index})">Editar</button>
                <button onclick="deleteContact(${index})">Excluir</button>
            `;
            contactsList.appendChild(listItem);
        });
    } catch (error) {
        console.error('Erro ao carregar os contatos:', error);
    }
}

// Função para editar um contato
function editContact(index) {
    fetch('/get_contacts')
        .then(response => response.json())
        .then(contacts => {
            const contact = contacts[index];
            document.getElementById('editName').value = contact.name;
            document.getElementById('editPhone').value = contact.phone;
            document.getElementById('editForm').style.display = 'block'; // Mostrar o formulário
            document.getElementById('saveEdit').setAttribute('data-index', index); // Armazena o índice no botão "Salvar"
        })
        .catch(error => console.error('Erro ao carregar contato:', error));
}

// Função para salvar a edição de um contato
async function saveEdit(event) {
    event.preventDefault(); // Previne o comportamento padrão do formulário

    const index = document.getElementById('saveEdit').getAttribute('data-index'); // Pega o índice do botão
    const name = document.getElementById('editName').value.trim();
    const phone = document.getElementById('editPhone').value.trim();

    // Verifica se os dados são válidos
    if (!name || !phone) {
        alert('Por favor, preencha todos os campos.');
        return;
    }

    // Valida o nome e o telefone
    if (!isValidName(name)) {
        alert('Nome inválido. O nome deve ter entre 3 e 50 caracteres e apenas letras.');
        return;
    }

    if (!isValidPhone(phone)) {
        alert('Telefone inválido. O telefone deve ter 13 dígitos e começar com "+"');
        return;
    }

    const updatedContact = { name, phone };

    try {
        const response = await fetch(`/edit_contacts/${index}`, { // Envia o índice correto no URL
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedContact), // Dados do contato atualizado
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message);
            loadContacts(); // Recarrega a lista de contatos após a edição
            cancelEdit(); // Fecha o formulário de edição
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error('Erro ao salvar o contato:', error);
        alert('Erro ao salvar o contato. Tente novamente.');
    }
}

document.getElementById('editForm').addEventListener('submit', saveEdit);


// Função para cancelar a edição
function cancelEdit() {
    document.getElementById('editForm').style.display = 'none'; // Esconde o formulário
}

// Função para excluir um contato
async function deleteContact(index) {
    if (confirm("Tem certeza que deseja excluir este contato?")) {
        try {
            const response = await fetch(`/delete_contact/${index}`, {
                method: 'DELETE',
            });

            const result = await response.json();
            if (response.ok) {
                alert(result.message);
                loadContacts();  // Recarregar a lista de contatos após exclusão
            } else {
                alert(result.error);
            }
        } catch (error) {
            console.error('Erro ao excluir o contato:', error);
            alert('Erro ao excluir o contato. Tente novamente.');
        }
    }
}

// Função de validação de nome
function isValidName(name) {
    if (!/^[a-zA-ZÀ-ÿ\s]{3,50}$/.test(name)) {
        alert('O nome deve ter entre 3 e 50 caracteres e conter apenas letras e espaços.');
        return false;
    }
    return true;
}

// Função de validação de telefone
function isValidPhone(phone) {
    if (!/^\+\d{13}$/.test(phone)) {
        alert('O número deve estar no formato internacional, como "+5511123451234".');
        return false;
    }
    return true;
}

// Pega os valores do formulário de adicionar contato
document.getElementById('addContactForm').addEventListener('submit', async (e) => {
    e.preventDefault(); // Evita recarregar a página

    // Pega os valores de nome e telefone, remove espaços extras
    const name = document.getElementById('name').value.trim();
    const phone = document.getElementById('phone').value.trim();

    // Valida o nome e telefone
    if (!isValidName(name) || !isValidPhone(phone)) {
        return;
    }

    try {
        // Envia os dados para o servidor
        const response = await fetch('/add_contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, phone }),
        });

        const result = await response.json();
        if (!response.ok) {
            alert(`Erro: ${result.error}`);
        } else {
            alert(result.message);
            // Limpa os campos após o envio bem-sucedido
            document.getElementById('name').value = '';
            document.getElementById('phone').value = '';
            loadContacts(); // Recarrega a lista de contatos
        }
    } catch (error) {
        alert('Erro ao conectar ao servidor. Tente novamente mais tarde.');
    }
});

// Carregar contatos ao carregar a página
document.addEventListener('DOMContentLoaded', loadContacts);
