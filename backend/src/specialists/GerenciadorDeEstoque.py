
class GerenciadorDeEstoque:
    def __init__(self, blackboard):
        self.blackboard = blackboard

    def adicionar_produto_estoque(self, nome_produto, descricao, preco_unitario, estoque_minimo):
        """Adiciona um novo produto no estoque"""
        self.blackboard.registrar_produto(nome_produto, descricao, preco_unitario, estoque_minimo)
        print(f"Produto {nome_produto} adicionado ao estoque.")

    def atualizar_estoque(self, id_produto, id_loja, quantidade):
        """Atualiza a quantidade de um produto no estoque de uma loja"""
        self.blackboard.atualizar_estoque(id_produto, id_loja, quantidade)
        print(f"Estoque do produto {id_produto} atualizado na loja {id_loja}.")
