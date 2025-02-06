from sqlalchemy.orm import Session
from src.models.models import Loja, Produto, Estoque, Venda, Compra, ItemCompra, ItemVenda, Fornecedor
from src.models.exceptions import ErroBancoException, QuantidadeInvalidaException, EstoqueInsuficienteException
from datetime import date

class Blackboard:
    _instance = None

    def __new__(cls, db_session=None):
        """
        Método para garantir que só haverá uma instância de Blackboard (implementação do SINGLETON).
        
        Esse método é responsável por garantir que apenas uma instância da classe Blackboard seja criada. 
        Se já existe uma instância, ele simplesmente retorna essa instância. 
        Caso contrário, ele cria uma nova instância e a armazena no atributo estático _instance.
        
        """
        
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # Cria a instância
            cls._instance.db_session = db_session  # Inicializa a sessão de banco de dados
        return cls._instance  # Retorna a instância única

    def __init__(self, db_session: Session=None):
        """
        Inicia a instância do Blackboard com uma sessão de banco de dados, se necessário.
        """
        
        if db_session is not None:
            self.db = db_session

    # CRUD para Loja
    def adicionar_loja(self, nome_loja: str, endereco: str, telefone: str):
        """
        Adiciona uma nova loja ao banco de dados.

        Args:
            nome_loja (str): O nome da loja a ser adicionada.
            endereco (str): O endereço da loja.
            telefone (str): O telefone de contato da loja.

        Returns:
            Loja: A instância da loja recém-adicionada.
        """

        nova_loja = Loja(nome_loja=nome_loja, endereco=endereco, telefone=telefone)
        self.db.add(nova_loja)
        self.db.commit()
        self.db.refresh(nova_loja)
        return nova_loja
    
    def atualizar_loja(self, loja_id: int, nome_loja: str, endereco: str, telefone: str):
        """
        Atualiza os dados de uma loja no banco de dados.

        Args:
            loja_id (int): O ID da loja a ser atualizada.
            nome_loja (str): O novo nome da loja.
            endereco (str): O novo endereço da loja.
            telefone (str): O novo telefone da loja.

        Returns:
            Loja: A loja atualizada, se a atualização for bem-sucedida.
            None: Se a loja com o ID fornecido não for encontrada.
        """
        
        loja: Loja = self.obter_loja(loja_id)
        if loja:
            loja.nome_loja = nome_loja
            loja.endereco = endereco
            loja.telefone = telefone
            self.db.commit()
            self.db.refresh(loja)
            return loja
        return

    def obter_loja(self, loja_id: int):
        """
        Obtém uma loja do banco de dados com base no ID fornecido.

        Args:
            loja_id (int): O ID da loja a ser obtida.

        Returns:
            Loja: A loja correspondente ao ID fornecido, ou None se não for encontrada.
        """
        
        return self.db.query(Loja).filter(Loja.id_loja == loja_id).first()

    def listar_lojas(self):
        """
        Lista todas as lojas do banco de dados.

        Returns:
            list: Uma lista de objetos Loja representando todas as lojas no banco de dados.
        """
        
        return self.db.query(Loja).all()

    # CRUD para Produto
    def adicionar_produto(self, nome_produto: str, descricao: str, preco_unitario: float, estoque_minimo: int):
        """
        Adiciona um novo produto ao banco de dados.

        Args:
            nome_produto (str): O nome do produto a ser adicionado.
            descricao (str): A descrição do produto.
            preco_unitario (float): O preço unitário do produto.
            estoque_minimo (int): A quantidade mínima de estoque do produto.

        Returns:
            Produto: O objeto Produto recém-adicionado ao banco de dados.
        """
        
        novo_produto = Produto(nome_produto=nome_produto, descricao=descricao, preco_unitario=preco_unitario, estoque_minimo=estoque_minimo)
        self.db.add(novo_produto)
        self.db.commit()
        self.db.refresh(novo_produto)
        return novo_produto
    
    def atualizar_produto(self, produto_id: int, nome_produto: str, descricao: str, preco_unitario: float, estoque_minimo: int):
        """
        Atualiza os dados de um produto no banco de dados.
        Args:
            produto_id (int): O ID do produto.
            nome_produto (str): O nome do produto.
            descricao (str): A descrição do produto.
            preco_unitario (float): O preço unitário do produto.
            estoque_minimo (int): O estoque mínimo do produto.
        Returns:
            Produto: O objeto de produto atualizado.
        """
        
        produto: Produto = self.obter_produto(produto_id)
        if produto:
            produto.nome_produto = nome_produto
            produto.descricao = descricao
            produto.preco_unitario = preco_unitario
            produto.estoque_minimo = estoque_minimo
            self.db.commit()
            self.db.refresh(produto)
            return produto
        return

    def obter_produto(self, produto_id: int):
        """
        Obtém um produto do banco de dados.
        Args:
            produto_id (int): O ID do produto.
        Returns:
            Produto: O objeto de produto encontrado.
        """
        
        return self.db.query(Produto).filter(Produto.id_produto == produto_id).first()

    def listar_produtos(self):
        """
        Lista todos os produtos do banco de dados.
        Returns:
            list: Uma lista de objetos Produto representando todos os produtos.
        """
        
        return self.db.query(Produto).all()

    # Operações no Estoque
    def adicionar_estoque(self, loja_id: int, produto_id: int, quantidade: int):
        """
        Adiciona ou atualiza um item de estoque no banco de dados.
        Args:
            loja_id (int): O ID da loja.
            produto_id (int): O ID do produto.
            quantidade (int): A quantidade a ser adicionada ao estoque.
        Returns:
            Estoque: O objeto de estoque adicionado ou atualizado.
        """
        try:
            estoque = self.db.query(Estoque).filter_by(id_loja=loja_id, id_produto=produto_id).first()

            if estoque:
                # Se existir, incrementa a quantidade
                estoque.quantidade += quantidade
            else:
                # Se não existir, cria um novo registro
                estoque = Estoque(id_loja=loja_id, id_produto=produto_id, quantidade=quantidade)
                self.db.add(estoque)

            self.db.commit()
            self.db.refresh(estoque)
            return estoque
        except Exception as e:
            self.db.rollback()
            raise ErroBancoException(f"Erro ao adicionar ou atualizar estoque: {e}")
    
    def atualizar_estoque(self, loja_id: int, produto_id: int, quantidade: int):
        """
        Atualiza a quantidade de um item de estoque no banco de dados.
        Args:
            loja_id (int): O ID da loja.
            produto_id (int): O ID do produto.
            quantidade (int): A quantidade a ser adicionada ao estoque.
        Returns:
            Estoque: O objeto de estoque atualizado.
        """
        
        estoque = self.obter_estoque(loja_id, produto_id)
        if estoque:
            estoque.quantidade += quantidade
            self.db.commit()
            self.db.refresh(estoque)
            return estoque
        return None

    def obter_estoque(self, loja_id: int, produto_id: int):
        """
        Obtém um item de estoque do banco de dados.
        Args:
            loja_id (int): O ID da loja.
            produto_id (int): O ID do produto.
        Returns:
            Estoque: O objeto de estoque encontrado.
        """
        
        return self.db.query(Estoque).filter(Estoque.id_loja == loja_id, Estoque.id_produto == produto_id).first()
    
    def obter_estoque_por_loja(self, loja_id: int):
        """
        Obtém o estoque de todos os produtos em uma loja específica.
        
        Args:
            loja_id (int): O ID da loja.
        
        Returns:
            list: Uma lista de objetos Estoque representando o estoque de todos os produtos na loja.
        """
        estoque = self.db.query(Estoque).filter(Estoque.id_loja == loja_id).all()
        
        return estoque

    def listar_estoque_por_produto(self, produto_id: int):
        """
        Retorna o estoque de um produto em todas as lojas.
        Args:
            produto_id (int): O ID do produto.
        Returns:
            list: Uma lista de objetos Estoque representando o estoque do produto em todas as lojas.
        """
        
        return self.db.query(Estoque).filter(Estoque.id_produto == produto_id).all()

    # Operações de Venda
    def registrar_venda(self, loja_id: int, produtos: list, data_venda: date):
        """
        Registra uma venda no sistema.
        
        Args:
            loja_id (int): O ID da loja.
            produtos (list): Uma lista de tuplas contendo (produto_id, quantidade, preco_unitario).
            data_venda (date): Data da venda.

        Returns:
            Venda: O objeto de venda registrado.

        Raises:
            QuantidadeInvalidaException: Se a quantidade do produto for inválida.
            EstoqueInsuficienteException: Se não houver estoque suficiente.
            ErroBancoException: Para outros erros do banco de dados.
        """
        try:
            total_venda = sum(produto[1] * produto[2] for produto in produtos)

            for produto_id, quantidade, preco_unitario in produtos:
                if quantidade <= 0:
                    raise QuantidadeInvalidaException("A quantidade do item deve ser maior que zero.")

            venda = Venda(id_loja=loja_id, valor_total=total_venda, data_venda=data_venda)
            self.db.add(venda)
            self.db.flush()

            itens_venda = []
            for produto_id, quantidade, preco_unitario in produtos:
                item_venda = ItemVenda(id_venda=venda.id_venda, id_produto=produto_id, 
                                    quantidade=quantidade, preco_unitario=preco_unitario)
                self.db.add(item_venda)
                itens_venda.append(item_venda)

            self.db.commit()
            self.db.refresh(venda) 

            return venda

        except QuantidadeInvalidaException:
            self.db.rollback()
            raise

        except Exception as e:
            self.db.rollback()

            error_message = str(e)

            if "chk_quantidade_positiva_item_venda" in error_message:
                raise QuantidadeInvalidaException("A quantidade do item deve ser maior que zero.")
            elif "Estoque insuficiente" in error_message:
                raise EstoqueInsuficienteException("Não há estoque suficiente para completar a venda.")
            else:
                raise ErroBancoException(f"Erro desconhecido ao registrar venda: {e}")

    def listar_vendas(self):
        """
        Retorna uma lista de todas as vendas do banco de dados.
        Returns:
            list: Uma lista de objetos Venda representando todas as vendas.
        """
        
        vendas = self.db.query(Venda).order_by(Venda.data_venda.desc()).all()
        for venda in vendas:
            venda.itens = ', '.join([
            f"{self.obter_produto(item.id_produto).nome_produto} (Qtd: {item.quantidade})"
            for item in self.db.query(ItemVenda).filter(ItemVenda.id_venda == venda.id_venda).all()
            ])

            # Adicionando o nome da loja associada à venda
            venda.nome_loja = venda.loja.nome_loja  # Acesse o nome da loja diretamente
        return vendas

    # Operações de Compra
    
    def registrar_compra(self, fornecedor_id: int, produtos: list):
        """
        Registra uma compra no sistema.
        Args:
            fornecedor_id (int): O ID do fornecedor.
            produtos (list): Uma lista de tuplas contendo (produto_id, quantidade, preco_unitario).
        Returns:
            Compra: O objeto de compra registrado.
        """
        
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

    def listar_compras(self):
        """
        Retorna uma lista de todas as compras do banco de dados.
        Retorna:
            list: Uma lista de objetos Compra representando todas as compras.
        """
        
        return self.db.query(Compra).order_by(Compra.data_compra.desc()).all()
    
    def listar_fornecedores(self):
        """
        Lista todas os fornecedores do banco de dados.

        Returns:
            list: Uma lista de objetos Fornecedor representando todas os fornecedores no banco de dados.
        """
        
        return self.db.query(Fornecedor).all()
    
    def adicionar_fornecedor(self, nome_fornecedor: str, cnpj: str, telefone: float, endereco: int):
        """
        Adiciona um novo fornecedor ao banco de dados.

        Args:
            nome_produto (str): O nome do produto a ser adicionado.
            descricao (str): A descrição do produto.
            preco_unitario (float): O preço unitário do produto.
            estoque_minimo (int): A quantidade mínima de estoque do produto.

        Returns:
            Produto: O objeto Produto recém-adicionado ao banco de dados.
        """
        
        novo_forncedor = Fornecedor(nome_fornecedor=nome_fornecedor, cnpj=cnpj, telefone=telefone, endereco=endereco)
        self.db.add(novo_forncedor)
        self.db.commit()
        self.db.refresh(novo_forncedor)
        return novo_forncedor
    
    def obter_fornecedor(self, fornecedor_id: int):
        """
        Obtém um produto do banco de dados.
        Args:
            produto_id (int): O ID do produto.
        Returns:
            Produto: O objeto de produto encontrado.
        """
        
        return self.db.query(Fornecedor).filter(Fornecedor.id_fornecedor == fornecedor_id).first()

    def atualizar_fornecedor(self, fornecedor_id: int, nome_fornecedor: str, cnpj: str, telefone:str, endereco:str):
        """
        Atualiza os dados de um fornecedor no banco de dados.

        Args:
            fornecedor_id (int): ID do fornecedor.
            nome_fornecedor (str): Nome do fornecedor.
            cnpj (str): CNPJ do fornecedor.
            telefone (str): Telefone do fornecedor.
            endereco (str): Endereço do fornecedor.

        Returns:
            Fornecedor: O fornecedor atualizado se bem-sucedido.
            None: Se o fornecedor não for encontrado.
        """
        fornecedor: Fornecedor = self.obter_fornecedor(fornecedor_id)

        if fornecedor:
            fornecedor.nome_fornecedor = nome_fornecedor
            fornecedor.cnpj = cnpj
            fornecedor.telefone = telefone
            fornecedor.endereco = endereco
            self.db.commit()
            self.db.refresh(fornecedor)
            return fornecedor
        return None