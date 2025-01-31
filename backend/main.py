import os
from flask import Flask, render_template, request, redirect, url_for
from src.database.database import SessionLocal, engine, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.models import Loja
# from src.specialists.LojaA import LojaA
# from src.specialists.LojaB import LojaB
from src.specialists.LojaFactory import LojaFactory
from src.models.blackboard import Blackboard
from src.models.formularios import LojaForm, ProdutoForm, VendaForm, ItemVendaForm

# Criando o aplicativo Flask
app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static'))

# Criando as tabelas no banco de dados, caso ainda não existam
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Criando o blackboard ao iniciar o backend
blackboard = Blackboard(db)

@app.route("/")
def read_root():
    lojas = blackboard.listar_lojas()
    produtos = blackboard.listar_produtos()
    return render_template('index.html', lojas=lojas, produtos=produtos)

@app.route('/produtos', methods=['GET', 'POST', 'PUT'])
def listar_produtos():
    produtos = blackboard.listar_produtos()  # Busca a lista de produtos
    form = ProdutoForm(request.form)

    if request.method == 'POST' and form.validate():
        nome_produto = form.nome_produto.data
        descricao = form.descricao.data
        preco_unitario = form.preco_unitario.data
        estoque_minimo = form.estoque_minimo.data

        # Adiciona o produto ao Blackboard
        blackboard.adicionar_produto(nome_produto, descricao, preco_unitario, estoque_minimo)

        return redirect(url_for('listar_produtos'))
    
    if request.method == 'PUT' and form.validate():
        id_produto = form.id_produto.data
        nome_produto = form.nome_produto.data
        descricao = form.descricao.data
        preco_unitario = form.preco_unitario.data
        estoque_minimo = form.estoque_minimo.data

        # Atualiza o produto no Blackboard
        blackboard.atualizar_produto(id_produto, nome_produto, descricao, preco_unitario, estoque_minimo)

        return redirect(url_for('listar_produtos'))

    return render_template('controle_produtos.html', produtos=produtos, form=form)

@app.route('/vendas', methods=['GET', 'POST'])
def listar_vendas():

    form = VendaForm(request.form)

    # Preenche o campo de seleção com as lojas disponíveis
    lojas_choices = [(loja.id_loja, loja.nome_loja) for loja in blackboard.listar_lojas()]
    lojas_choices.insert(0, (-1, 'Selecione uma loja'))
    form.id_loja.choices = lojas_choices

    # Preenche o campo de seleção com os produtos disponíveis
    produtos_choices = [(produto.id_produto, produto.nome_produto) for produto in blackboard.listar_produtos()]
    produtos_choices.insert(0, (-1, 'Selecione um produto'))
    form.id_produto.choices = produtos_choices

    vendas = blackboard.listar_vendas()  # Busca a lista de vendas
    
    if request.method == 'POST' and form.validate():

        id_loja = form.id_loja.data
        produto_id = form.id_produto.data
        quantidade = form.quantidade.data
        preco_unitario = form.preco_unitario.data
        data_venda = form.data_venda.data

        # Adiciona a venda ao Blackboard
        blackboard.registrar_venda(id_loja, [(produto_id, quantidade, preco_unitario)], data_venda)

        return redirect(url_for('listar_vendas'))

    return render_template('controle_vendas.html', vendas=vendas, form=form)

@app.route('/compras', methods=['GET'])
def listar_compras():
    compras = blackboard.listar_compras()
    return render_template('controle_compras.html', compras=compras)

# Rota para exibir as lojas
@app.route('/lojas', methods=['GET', 'POST'])
def listar_lojas():

    lojas = blackboard.listar_lojas()  # Usando o método do Blackboard para buscar lojas

    form = LojaForm(request.form)

    if request.method == 'POST' and form.validate():
        
        nome_loja = form.nome_loja.data
        endereco = form.endereco.data
        telefone = form.telefone.data

        # Usando a instância global do Blackboard para adicionar a loja
        blackboard.adicionar_loja(nome_loja, endereco, telefone)

        return redirect(url_for('listar_lojas'))

    return render_template('controle_lojas.html', lojas=lojas, form=form)

@app.route('/ver_estoque_lojas', methods=['GET'])
def ver_estoque_lojas():

    loja_a = LojaFactory('LojaA', blackboard)
    loja_b = LojaFactory('LojaB', blackboard)

    print("Loja A:")
    loja_a.verificar_estoque()

    print("Loja B:")
    loja_b.verificar_estoque()

    return "Verifique o console para a lista de produtos em cada loja."

if __name__ == "__main__":
    app.run(debug=True)