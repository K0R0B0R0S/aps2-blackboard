import os
from flask import Flask, render_template, request, redirect, url_for, flash
from src.models.exceptions import ErroBancoException, EstoqueInsuficienteException, QuantidadeInvalidaException
from src.database.database import SessionLocal, engine, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.models import Loja
# from src.specialists.LojaA import LojaA
# from src.specialists.LojaB import LojaB
from src.specialists.LojaFactory import LojaFactory
from src.specialists.GerenciadorDeEstoque import GerenciadorDeEstoque, EstrategiaConservadora, EstrategiaAgressiva, EstrategiaPersonalizada
from src.models.blackboard import Blackboard
from src.models.formularios import LojaForm, ProdutoForm, VendaForm, ItemVendaForm, FornecedorForm
from flask_socketio import SocketIO, emit
from decimal import Decimal

# Criando o aplicativo Flask
app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static'))
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Criando as tabelas no banco de dados, caso ainda não existam
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Criando o blackboard ao iniciar o backend
blackboard = Blackboard(db)
gerenciador_estoque = GerenciadorDeEstoque(blackboard, socketio=socketio)

def formatarVendas(vendas):

    for venda in vendas:
        # Se o valor for do tipo string, converta para Decimal
        if isinstance(venda.valor_total, str):
            venda.valor_total = Decimal(venda.valor_total.replace('R$', '').replace('.', '').replace(',', '.'))

        # Agora formate o valor para o formato correto, com separação de milhar e vírgula como separador decimal
        venda.valor_total_formatado = f"R$ {venda.valor_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    return vendas


@app.route("/")
def read_root():
    lojas = blackboard.listar_lojas()
    produtos = blackboard.listar_produtos()

    vendas = blackboard.listar_vendas()  # Busca a lista de vendas

    vendas_formatadas = formatarVendas(vendas)

    return render_template('index.html', lojas=lojas, produtos=produtos, vendas=vendas_formatadas)

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

    # Preenche os selects com lojas e produtos disponíveis
    form.id_loja.choices = [(-1, 'Selecione uma loja')] + [
        (loja.id_loja, loja.nome_loja) for loja in blackboard.listar_lojas()
    ]
    form.id_produto.choices = [(-1, 'Selecione um produto')] + [
        (produto.id_produto, produto.nome_produto) for produto in blackboard.listar_produtos()
    ]

    vendas_formatadas = formatarVendas(blackboard.listar_vendas())

    if request.method == 'POST' and form.validate():
        try:
            # Obtendo dados do formulário
            id_loja = form.id_loja.data
            produto_id = form.id_produto.data
            quantidade = form.quantidade.data
            preco_unitario = form.preco_unitario.data
            data_venda = form.data_venda.data

            # Registrando a venda
            blackboard.registrar_venda(id_loja, [(produto_id, quantidade, preco_unitario)], data_venda)

            flash("Venda registrada com sucesso!", "success")
            return redirect(url_for('listar_vendas'))

        except QuantidadeInvalidaException as e:
            flash(str(e), "danger")
        
        except EstoqueInsuficienteException as e:
            flash(str(e), "danger")

        except ErroBancoException as e:
            flash(f"Erro no banco de dados: {str(e)}", "danger")

        except Exception as e:
            flash("Ocorreu um erro inesperado. Tente novamente.", "danger")

    return render_template('controle_vendas.html', vendas=vendas_formatadas, form=form)

@app.route('/fornecedores', methods=['GET', 'POST'])
def fornecedores():

    form = FornecedorForm(request.form)

    fornecedores = blackboard.listar_fornecedores()  # Busca a lista de fornecedores
    
    if request.method == 'POST' and form.validate():

        nome_fornecedor = form.nome_fornecedor.data
        cpj = form.cnpj.data
        telefone = form.telefone.data
        endereco = form.endereco.data

        # Adiciona o fornecedorer novo no banco
        blackboard.adicionar_fornecedor(nome_fornecedor, cpj, telefone, endereco)

        return redirect(url_for('fornecedores'))

    return render_template('controle_fornecedores.html', fornecedores=fornecedores, form=form)

@app.route('/compras', methods=['GET'])
def listar_compras():
    compras = blackboard.listar_compras()
    return render_template('controle_compras.html', compras=compras)

@app.route('/lojas', defaults={'loja_id': None}, methods=['GET', 'POST'])
def listar_lojas(loja_id):

    lojas = blackboard.listar_lojas()  # Usando o método do Blackboard para buscar lojas

    form = LojaForm(request.form)

    # Se a rota for chamada via POST, faz o cadastro ou atualização
    if request.method == 'POST' and form.validate():
        nome_loja = form.nome_loja.data
        endereco = form.endereco.data
        telefone = form.telefone.data
        tipo_loja = form.tipo_loja.data

        # Se a loja_id estiver presente, faz a atualização
        if loja_id:
            blackboard.atualizar_loja(loja_id, nome_loja, endereco, telefone)

            return redirect(url_for('listar_lojas'))  # Atualiza a lista
        # Caso contrário, faz a inserção de uma nova loja
        else:
            # Usando a fábrica para criar a loja e adicionar no blackboard
            LojaFactory.criar_loja(tipo_loja, blackboard, nome_loja, endereco, telefone)

            return redirect(url_for('listar_lojas'))

    return render_template('controle_lojas.html', lojas=lojas, form=form, form_title="Cadastrar Loja", button_text="Adicionar Loja")

@app.route('/editar_loja/<int:loja_id>/<string:nome_loja>/<string:endereco>/<string:telefone>', methods=['POST'])
def editar_loja(loja_id, nome_loja, endereco, telefone):
    # Atualiza a loja no banco de dados ou no Blackboard
    blackboard.atualizar_loja(loja_id, nome_loja, endereco, telefone)

    # Retorna uma resposta simples de sucesso ou redireciona, sem renderizar HTML
    return '', 204  # Retorna um status 204 sem conteúdo (sucesso)

@app.route('/ver_estoque_lojas', methods=['GET'])
def ver_estoque_lojas():

    loja_a = LojaFactory.criar_loja('LojaA', blackboard)
    loja_b = LojaFactory.criar_loja('LojaB', blackboard)
   
    print("Loja A:")
    loja_a.verificar_estoque()

    print("Loja B:")
    loja_b.verificar_estoque()

    return "Verifique o console para a lista de produtos em cada loja."

@app.route("/relatorio_estoque", methods=['GET'])
def verificar_estoque():
    estrategia = request.args.get('estrategia', 'conservadora')
    fator = request.args.get('fator', 1)

    if estrategia == 'conservadora':
        gerenciador_estoque.definir_estrategia_reposicao(EstrategiaConservadora())
    elif estrategia == 'agressiva':
        gerenciador_estoque.definir_estrategia_reposicao(EstrategiaAgressiva())
    elif estrategia == 'personalizada':
        gerenciador_estoque.definir_estrategia_reposicao(EstrategiaPersonalizada(fator=float(fator)))
    else:
        return "Estratégia inválida ou fator não fornecido para estratégia personalizada", 400

    alerta_estoque_minimo = gerenciador_estoque.verificar_estoque_minimo()
    sugestao_reposicao = gerenciador_estoque.sugerir_reposicao()

    return render_template('relatorio_estoque.html', alerta_estoque_minimo=alerta_estoque_minimo, sugestao_reposicao=sugestao_reposicao)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == "__main__":
    app.run(debug=True)