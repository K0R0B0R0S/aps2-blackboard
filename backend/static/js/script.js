
// Ação do botão para "Gerar Sugestões"
document.getElementById('reposicao-btn').addEventListener('click', function() {
    alert('Gerando sugestões de reposição...');

    // Aqui você pode implementar o código para gerar sugestões de reposição
    // Como exemplo, vamos apenas mostrar um alerta (poderia ser uma chamada para uma API, por exemplo)
});

// Formulário de registro de venda
document.getElementById('form-venda').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o envio do formulário

    let loja = document.getElementById('loja').value;
    let produto = document.getElementById('produto').value;
    let quantidade = document.getElementById('quantidade').value;
    let data = document.getElementById('data').value;

    if (loja && produto && quantidade && data) {
        alert('Venda registrada!\n' +
            'Loja: ' + loja + '\n' +
            'Produto: ' + produto + '\n' +
            'Quantidade: ' + quantidade + '\n' +
            'Data: ' + data);
        
        // Aqui você poderia fazer um envio para o backend, registrando a venda
    } else {
        alert('Por favor, preencha todos os campos.');
    }
});

// Formulário de adição de loja
document.getElementById('form-adicionar-loja').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o envio do formulário

    let nomeLoja = document.getElementById('nome_loja').value;
    let endereco = document.getElementById('endereco').value;
    let telefone = document.getElementById('telefone').value;

    if (nomeLoja && endereco && telefone) {
        alert('Loja adicionada!\n' +
            'Nome: ' + nomeLoja + '\n' +
            'Endereço: ' + endereco + '\n' +
            'Telefone: ' + telefone);

        // Aqui você poderia fazer uma requisição para adicionar a loja no banco de dados

        // Após adicionar a loja, você pode redirecionar ou atualizar a tabela de lojas
        location.reload(); // Recarregar a página para ver a loja adicionada (exemplo)
    } else {
        alert('Por favor, preencha todos os campos.');
    }
});
