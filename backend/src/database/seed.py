from sqlalchemy.orm import sessionmaker
from src.database.database import engine
from src.models.models import Loja, Produto, Fornecedor, Estoque, Compra, ItemCompra, Venda, ItemVenda
from datetime import date
from sqlalchemy.exc import IntegrityError

# Criar uma sessão do SQLAlchemy
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

def seed_data():
    try:
        # Inserindo Lojas
        lojas = [
            Loja(nome_loja="Loja Central", endereco="Rua das Flores, 123 - Centro", telefone="11987654321"),
            Loja(nome_loja="Loja Norte", endereco="Avenida Brasil, 456 - Bairro Norte", telefone="11987651234"),
            Loja(nome_loja="Loja Sul", endereco="Rua das Palmeiras, 789 - Bairro Sul", telefone="11987657890"),
            Loja(nome_loja="Loja Leste", endereco="Rua do Comércio, 321 - Bairro Leste", telefone="11987654322"),
        ]
        session.add_all(lojas)
        session.commit()

        # Inserindo Produtos
        produtos = [
            Produto(nome_produto="Camiseta Branca", descricao="Camiseta de algodão branca", preco_unitario=29.90, estoque_minimo=10),
            Produto(nome_produto="Calça Jeans", descricao="Calça jeans azul escuro", preco_unitario=89.90, estoque_minimo=5),
            Produto(nome_produto="Tênis Esportivo", descricao="Tênis para corrida", preco_unitario=199.90, estoque_minimo=3),
            Produto(nome_produto="Jaqueta de Couro", descricao="Jaqueta de couro legítimo", preco_unitario=299.90, estoque_minimo=2),
            Produto(nome_produto="Boné Preto", descricao="Boné ajustável preto", preco_unitario=49.90, estoque_minimo=8),
            Produto(nome_produto="Relógio Digital", descricao="Relógio digital à prova d'água", preco_unitario=150.00, estoque_minimo=4),
        ]
        session.add_all(produtos)
        session.commit()

        # Inserindo Fornecedores
        fornecedores = [
            Fornecedor(nome_fornecedor="Fornecedor ABC", cnpj="12345678000199", telefone="11999998888", endereco="Rua das Indústrias, 100 - SP"),
            Fornecedor(nome_fornecedor="Fornecedor XYZ", cnpj="98765432000155", telefone="11888887777", endereco="Avenida Comercial, 50 - RJ"),
            Fornecedor(nome_fornecedor="Fornecedor Moda", cnpj="56473829000133", telefone="11988887766", endereco="Rua Fashion, 200 - MG"),
        ]
        session.add_all(fornecedores)
        session.commit()

        # Inserindo Estoque
        estoques = [
            Estoque(id_loja=1, id_produto=1, quantidade=50),
            Estoque(id_loja=1, id_produto=2, quantidade=30),
            Estoque(id_loja=2, id_produto=3, quantidade=20),
            Estoque(id_loja=3, id_produto=4, quantidade=15),
            Estoque(id_loja=4, id_produto=5, quantidade=40),
            Estoque(id_loja=2, id_produto=6, quantidade=25),
            Estoque(id_loja=3, id_produto=1, quantidade=35),
            Estoque(id_loja=4, id_produto=2, quantidade=50),
            Estoque(id_loja=1, id_produto=3, quantidade=45),
            Estoque(id_loja=2, id_produto=4, quantidade=30),
        ]
        session.add_all(estoques)
        session.commit()

        # Inserindo Compras
        compras = [
            Compra(id_fornecedor=1, data_compra=date(2024, 1, 10), valor_total=1495.00),
            Compra(id_fornecedor=2, data_compra=date(2024, 1, 15), valor_total=2998.50),
            Compra(id_fornecedor=3, data_compra=date(2024, 1, 20), valor_total=4500.75),
        ]
        session.add_all(compras)
        session.commit()

        # Inserindo Itens de Compra
        itens_compra = [
            ItemCompra(id_compra=1, id_produto=1, quantidade=50, preco_unitario=29.90),
            ItemCompra(id_compra=1, id_produto=2, quantidade=20, preco_unitario=74.75),
            ItemCompra(id_compra=2, id_produto=3, quantidade=15, preco_unitario=199.90),
            ItemCompra(id_compra=3, id_produto=4, quantidade=10, preco_unitario=299.90),
            ItemCompra(id_compra=3, id_produto=5, quantidade=25, preco_unitario=49.90),
            ItemCompra(id_compra=2, id_produto=6, quantidade=30, preco_unitario=150.00),
        ]
        session.add_all(itens_compra)
        session.commit()

         # Inserindo Vendas
        vendas = [
            Venda(id_loja=1, data_venda=date(2024, 1, 22), valor_total=349.70),
            Venda(id_loja=2, data_venda=date(2024, 1, 24), valor_total=599.80),
            Venda(id_loja=3, data_venda=date(2024, 1, 25), valor_total=899.90),
            Venda(id_loja=4, data_venda=date(2024, 1, 26), valor_total=1299.90),
        ]
        session.add_all(vendas)
        session.commit()

        # Inserindo Itens de Venda
        itens_venda = [
            ItemVenda(id_venda=1, id_produto=1, quantidade=3, preco_unitario=29.90),
            ItemVenda(id_venda=1, id_produto=2, quantidade=2, preco_unitario=89.90),
            ItemVenda(id_venda=2, id_produto=3, quantidade=3, preco_unitario=199.90),
            ItemVenda(id_venda=3, id_produto=4, quantidade=1, preco_unitario=299.90),
            ItemVenda(id_venda=4, id_produto=5, quantidade=2, preco_unitario=49.90),
            ItemVenda(id_venda=3, id_produto=6, quantidade=2, preco_unitario=150.00),
        ]
        session.add_all(itens_venda)
        session.commit()

        print("✅ Dados inseridos com sucesso!")

    except IntegrityError:
        session.rollback()
        print("⚠️ Dados já foram inseridos anteriormente.")

    finally:
        session.close()

if __name__ == "__main__":
    seed_data()
