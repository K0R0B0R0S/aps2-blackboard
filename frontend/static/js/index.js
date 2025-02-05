const sideMenu = document.querySelector('aside');
const menuBtn = document.getElementById('menu-btn');
const closeBtn = document.getElementById('close-btn');

const darkMode = document.querySelector('.dark-mode');

menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
});

closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
});

darkMode.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode-variables');
    darkMode.querySelector('span:nth-child(1)').classList.toggle('active');
    darkMode.querySelector('span:nth-child(2)').classList.toggle('active');
})

document.addEventListener('DOMContentLoaded', function() {
    const socket = io();

    socket.on('estoque_alert', function(message) {
        alert(`Alerta de Estoque Baixo!\nProduto: ${message.produto}\nLoja: ${message.loja}\nQuantidade Atual: ${message.quantidade_atual}\nEstoque Mínimo: ${message.estoque_minimo}`);
    });
    
})