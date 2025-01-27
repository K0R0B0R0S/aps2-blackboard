from sqlalchemy.orm import Session
from src.models.models import Loja, Produto, Estoque, Venda, Compra, ItemCompra, ItemVenda

class Blackboard:
    _instance = None

    def __new__(cls, db_session=None):
        """Método para garantir que só haverá uma instância de Blackboard (implementação do SINGLETON).
        
        Esse método é responsável por garantir que apenas uma instância da classe Blackboard seja criada. 
        Se já existe uma instância, ele simplesmente retorna essa instância. 
        Caso contrário, ele cria uma nova instância e a armazena no atributo estático _instance.
        
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # Cria a instância
            cls._instance.db_session = db_session  # Inicializa a sessão de banco de dados
        return cls._instance  # Retorna a instância única

    def __init__(self, db_session=None):
        """Inicia a instância do Blackboard com uma sessão de banco de dados, se necessário."""
        if db_session is not None:
            self.db = db_session

    # CRUD para Loja
    def adicionar_loja(self, nome_loja: str, endereco: str, telefone: str):
        nova_loja = Loja(nome_loja=nome_loja, endereco=endereco, telefone=telefone)
        self.db.add(nova_loja)
        self.db.commit()
        self.db.refresh(nova_loja)
        return nova_loja

    def obter_loja(self, loja_id: int):
        return self.db.query(Loja).filter(Loja.id_loja == loja_id).first()

    def listar_lojas(self):
        return self.db.query(Loja).all()

    # CRUD para Produto
    def adicionar_produto(self, nome_produto: str, descricao: str, preco_unitario: float, estoque_minimo: int):
        novo_produto = Produto(nome_produto=nome_produto, descricao=descricao, preco_unitario=preco_unitario, estoque_minimo=estoque_minimo)
        self.db.add(novo_produto)
        self.db.commit()
        self.db.refresh(novo_produto)
        return novo_produto

    def obter_produto(self, produto_id: int):
        return self.db.query(Produto).filter(Produto.id_produto == produto_id).first()

    def listar_produtos(self):
        return self.db.query(Produto).all()

    # Operações no Estoque
    def adicionar_estoque(self, loja_id: int, produto_id: int, quantidade: int):
        estoque = Estoque(id_loja=loja_id, id_produto=produto_id, quantidade=quantidade)
        self.db.add(estoque)
        self.db.commit()
        self.db.refresh(estoque)
        return estoque

    def obter_estoque(self, loja_id: int, produto_id: int):
        return self.db.query(Estoque).filter(Estoque.id_loja == loja_id, Estoque.id_produto == produto_id).first()

    def atualizar_estoque(self, loja_id: int, produto_id: int, quantidade: int):
        estoque = self.obter_estoque(loja_id, produto_id)
        if estoque:
            estoque.quantidade += quantidade
            self.db.commit()
            self.db.refresh(estoque)
            return estoque
        return None

    # Operações de Venda
    def registrar_venda(self, loja_id: int, produtos: list):  # produtos é uma lista de tuplas (produto_id, quantidade)
        total_venda = sum([produto[1] * produto[2] for produto in produtos])  # Calculando o valor total da venda
        venda = Venda(id_loja=loja_id, valor_total=total_venda)
        self.db.add(venda)
        self.db.commit()
        self.db.refresh(venda)

        # Criando itens de venda
        for produto_id, quantidade, preco_unitario in produtos:
            item_venda = ItemVenda(id_venda=venda.id_venda, id_produto=produto_id, quantidade=quantidade, preco_unitario=preco_unitario)
            self.db.add(item_venda)
            self.db.commit()

        return venda

    # Operações de Compra
    def registrar_compra(self, fornecedor_id: int, produtos: list):  # produtos é uma lista de tuplas (produto_id, quantidade, preco_unitario)
        valor_total = sum([produto[1] * produto[2] for produto in produtos])  # Calculando o valor total da compra
        compra = Compra(id_fornecedor=fornecedor_id, valor_total=valor_total)
        self.db.add(compra)
        self.db.commit()
        self.db.refresh(compra)

        # Criando itens de compra
        for produto_id, quantidade, preco_unitario in produtos:
            item_compra = ItemCompra(id_compra=compra.id_compra, id_produto=produto_id, quantidade=quantidade, preco_unitario=preco_unitario)
            self.db.add(item_compra)
            self.db.commit()

        return compra

    # Relacionamentos entre produtos e compras
    def listar_compras(self):
        return self.db.query(Compra).all()

    def listar_vendas(self):
        return self.db.query(Venda).all()
