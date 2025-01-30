from datetime import datetime
from src.models.blackboard import Blackboard

class GerenciadorDeEstoque:
    def __init__(self, blackboard):
        self.blackboard = blackboard

    def verificar_estoque_minimo(self):
        produtos = self.blackboard.listar_produtos()
        for produto in produtos:
            estoque = self.blackboard.listar_estoque_por_produto(produto.id_produto)
            for item in estoque:
                if item.quantidade < produto.estoque_minimo:
                    print(f"ALERTA: Estoque baixo para o produto {produto.nome_produto} na loja {item.id_loja}.")

    def sugerir_reposicao(self):
        produtos = self.blackboard.listar_produtos()
        for produto in produtos:
            estoque = self.blackboard.listar_estoque_por_produto(produto.id_produto)
            for item in estoque:
                if item.quantidade < produto.estoque_minimo:
                    quantidade_reposicao = produto.estoque_minimo - item.quantidade
                    print(f"Sugestão: Repor {quantidade_reposicao} unidades do produto {produto.nome_produto} na loja {item.id_loja}.")

    def sugerir_transferencias(self):
        produtos = self.blackboard.listar_produtos()
        for produto in produtos:
            estoque = self.blackboard.listar_estoque_por_produto(produto.id_produto)
            lojas_com_excesso = [item for item in estoque if item.quantidade > produto.estoque_minimo * 1.5]
            lojas_com_falta = [item for item in estoque if item.quantidade < produto.estoque_minimo]

            for falta in lojas_com_falta:
                for excesso in lojas_com_excesso:
                    quantidade_transferencia = min(excesso.quantidade - produto.estoque_minimo, produto.estoque_minimo - falta.quantidade)
                    if quantidade_transferencia > 0:
                        print(f"Sugestão: Transferir {quantidade_transferencia} unidades do produto {produto.nome_produto} da loja {excesso.id_loja} para a loja {falta.id_loja}.")

    def gerar_ordem_compra(self):
        produtos = self.blackboard.listar_produtos()
        for produto in produtos:
            estoque = self.blackboard.listar_estoque_por_produto(produto.id_produto)
            for item in estoque:
                if item.quantidade < produto.estoque_minimo:
                    quantidade_compra = produto.estoque_minimo * 2 - item.quantidade
                    print(f"Ordem de compra: Comprar {quantidade_compra} unidades do produto {produto.nome_produto} para a loja {item.id_loja}.")

    def registrar_movimentacao(self, tipo, id_produto, id_loja, quantidade):
        movimentacao = {
            'tipo': tipo,
            'id_produto': id_produto,
            'id_loja': id_loja,
            'quantidade': quantidade,
            'data': datetime.now()
        }
        self.blackboard.adicionar_movimentacao(movimentacao)


if __name__ == "__main__":
    from src.database.database import SessionLocal, engine, Base

    db = SessionLocal()

    blackboard = Blackboard(db)

    blackboard = Blackboard()
    gerenciador = GerenciadorDeEstoque(blackboard)
    gerenciador.verificar_estoque_minimo()
    gerenciador.sugerir_reposicao()
    gerenciador.sugerir_transferencias()
    gerenciador.gerar_ordem_compra()