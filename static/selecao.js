// Função para carregar contatos
function fetchContacts() {
    fetch('/get_contacts')
        .then(response => response.json())
        .then(data => {
            const contactsList = document.getElementById('contactsList');
            contactsList.innerHTML = '';  // Limpa a tabela antes de carregar os dados

            data.forEach(contact => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><input type="checkbox" class="contactCheckbox" value="${contact.phone}"></td>
                    
                    <td>${contact.name}</td>
                    <td>${contact.phone}</td>
                `;
                contactsList.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Erro ao carregar os contatos:', error);
        });
}


// Função para selecionar/desmarcar todos os contatos
function selectAllContacts() {
    const checkboxes = document.querySelectorAll('.contactCheckbox');
    const selectAll = document.getElementById('selectAll');
    checkboxes.forEach(checkbox => checkbox.checked = selectAll.checked);
}

// // Função para enviar a mensagem
// async function sendMessage() {
//     const selectedContacts = [];
//     const checkboxes = document.querySelectorAll('.contactCheckbox:checked');
//     checkboxes.forEach(checkbox => {
//         selectedContacts.push(checkbox.value);  // Pega o número de telefone
//     });

//     const message = prompt("Digite a mensagem que deseja enviar:");

//     if (selectedContacts.length > 0 && message) {
//         try {
//             const response = await fetch('/send_message', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify({ contacts: selectedContacts, message: message }),
//             });

//             const result = await response.json();
//             if (response.ok) {
//                 alert(result.message);
//                 // Abrir links do WhatsApp
//                 result.links.forEach(link => {
//                     window.open(link, '_blank');
//                 });
//             } else {
//                 alert(`Erro: ${result.error}`);
//             }
//         } catch (error) {
//             console.error('Erro ao enviar a mensagem:', error);
//             alert('Erro ao enviar a mensagem. Tente novamente.');
//         }
//     } else {
//         alert("Selecione pelo menos um contato e digite uma mensagem.");
//     }
// }


// Função para enviar a mensagem
async function sendMessage() {
    const selectedContacts = [];
    const checkboxes = document.querySelectorAll('.contactCheckbox:checked');
    checkboxes.forEach(checkbox => {
        selectedContacts.push(checkbox.value);  // Pega o número de telefone
    });

    const messageTextarea = document.getElementById('messageTextarea');
    const message = messageTextarea.value.trim();

    if (selectedContacts.length > 0 && message) {
        const encodedMessage = encodeURIComponent(message);

        // Abre uma nova aba para cada contato com a mensagem já preenchida
        selectedContacts.forEach(contact => {
            const whatsappLink = `https://wa.me/${contact}?text=${encodedMessage}`;
            window.open(whatsappLink, '_blank');  // Abre o link do WhatsApp em uma nova aba
        });
    } else {
        alert("Selecione pelo menos um contato e digite uma mensagem.");
    }
}

// Carrega os contatos assim que a página for carregada
window.onload = fetchContacts;


// Carrega os contatos assim que a página for carregada
window.onload = fetchContacts;


// Carrega os contatos assim que a página for carregada
window.onload = fetchContacts;

// Carrega os contatos assim que a página for carregada
window.onload = fetchContacts;
