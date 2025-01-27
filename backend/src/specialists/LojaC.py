
class LojaC:
    def __init__(self, blackboard):
        self.blackboard = blackboard

    def verificar_estoque(self):
        produtos = self.blackboard.listar_produtos()
        for produto in produtos:
            print(f"Produto: {produto.nome_produto}, Estoque Mínimo: {produto.estoque_minimo}")