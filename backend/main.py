import os
from flask import Flask, render_template, request, redirect, url_for
from src.database.database import SessionLocal, engine, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.models import Loja
# from src.specialists.LojaA import LojaA
# from src.specialists.LojaB import LojaB
# from src.specialists.LojaC import LojaC
from src.specialists.LojaFactory import LojaFactory
from src.models.blackboard import Blackboard
from src.models.formularios import LojaForm

# Criando o aplicativo Flask
app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static'))

# Criando as tabelas no banco de dados, caso ainda não existam
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Criando o blackboard ao iniciar o backend
blackboard = Blackboard(db)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao sistema!"}


@app.get("/home")
def read_root_TEST():
    return render_template('index.html')

# @app.get("/controle_estoque")
# def read_root_estoque():
#     return render_template('controle_estoque.html', form=form, loja=loja)

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

    return render_template('controle_estoque.html', lojas=lojas, form=form)

# Rota para ver o estoque das lojas
@app.route('/ver_estoque_lojas', methods=['GET'])
def ver_estoque_lojas():

    loja_a = LojaFactory('LojaA', blackboard)
    loja_b = LojaFactory('LojaB', blackboard)
    loja_c = LojaFactory('LojaC', blackboard)

    print("Loja A:")
    loja_a.verificar_estoque()

    print("Loja B:")
    loja_b.verificar_estoque()

    print("Loja C:")
    loja_c.verificar_estoque()

    return "Verifique o console para a lista de produtos em cada loja."


if __name__ == "__main__":
    app.run(debug=True)