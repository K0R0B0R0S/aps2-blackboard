from datetime import datetime
from typing import TYPE_CHECKING
from src.models.blackboard import Blackboard
from src.specialists.strategies.strategy import (
    EstrategiaAgressiva,
    EstrategiaConservadora,
    EstrategiaPersonalizada,
    EstrategiaReposicao
)

if TYPE_CHECKING:
    from src.models.blackboard import Blackboard

class TipoMovimentacao():
    """
    Enum para representar os tipos de movimentações, alertas, sugestões e ordens.
    Cada membro tem um valor inteiro associado.
    """
    ESTOQUE_BAIXO = 1  # Alerta de estoque abaixo do mínimo
    SUGESTAO_REPOSICAO = 2  # Sugestão de reposição de estoque
    SUGESTAO_TRANSFERENCIA = 3  # Sugestão de transferência entre lojas
    ORDEM_COMPRA = 4  # Ordem de compra para repor estoque
    ENTRADA = 5  # Movimentação de entrada no estoque
    SAIDA = 6  # Movimentação de saída no estoque

class GerenciadorDeEstoque:
    def __init__(self, blackboard: Blackboard, estrategia_reposicao=None):
        self.blackboard = blackboard
        self.estrategia_reposicao = estrategia_reposicao or EstrategiaConservadora()

    def definir_estrategia_reposicao(self, estrategia):
        """
        Define a estratégia de reposição a ser usada.
        """
        self.estrategia_reposicao = estrategia

    def verificar_estoque_minimo(self):
        """
        Verifica se o estoque está abaixo do mínimo e retorna uma lista de alertas.

        Retorno:
            List[dict]: Lista de alertas com informações sobre o produto, loja e quantidade.
        """
        alertas = []
        produtos = self.blackboard.listar_produtos()
        for produto in produtos:
            estoque = self.blackboard.listar_estoque_por_produto(produto.id_produto)
            for item in estoque:
                if item.quantidade < produto.estoque_minimo:
                    alertas.append({
                        'tipo': TipoMovimentacao.ESTOQUE_BAIXO,
                        'produto': produto.nome_produto,
                        'id_produto': produto.id_produto,
                        'loja': item.id_loja,
                        'quantidade_atual': item.quantidade,
                        'estoque_minimo': produto.estoque_minimo
                    })
        return alertas

    def sugerir_reposicao(self):
        """
        Sugere a reposição de produtos com estoque abaixo do mínimo.

        Retorno:
            List[dict]: Lista de sugestões de reposição com informações sobre o produto, loja e quantidade a repor.
        """
        sugestoes = []
        produtos = self.blackboard.listar_produtos()
        for produto in produtos:
            estoque = self.blackboard.listar_estoque_por_produto(produto.id_produto)
            for item in estoque:
                if item.quantidade < produto.estoque_minimo:
                    quantidade_reposicao = self.estrategia_reposicao.calcular_reposicao(produto, item.quantidade)
                    sugestoes.append({
                        'tipo': TipoMovimentacao.SUGESTAO_REPOSICAO,
                        'produto': produto.nome_produto,
                        'id_produto': produto.id_produto,
                        'loja': item.id_loja,
                        'quantidade_reposicao': quantidade_reposicao
                    })
        return sugestoes

    def sugerir_transferencias(self):
        """
        Sugere transferências de estoque entre lojas para equilibrar o estoque.

        Retorno:
            List[dict]: Lista de sugestões de transferência com informações sobre o produto, lojas envolvidas e quantidade a transferir.
        """
        sugestoes = []
        produtos = self.blackboard.listar_produtos()
        for produto in produtos:
            estoque = self.blackboard.listar_estoque_por_produto(produto.id_produto)
            lojas_com_excesso = [item for item in estoque if item.quantidade > produto.estoque_minimo * 1.5]
            lojas_com_falta = [item for item in estoque if item.quantidade < produto.estoque_minimo]

            for falta in lojas_com_falta:
                for excesso in lojas_com_excesso:
                    quantidade_transferencia = min(excesso.quantidade - produto.estoque_minimo, produto.estoque_minimo - falta.quantidade)
                    if quantidade_transferencia > 0:
                        sugestoes.append({
                            'tipo': TipoMovimentacao.SUGESTAO_TRANSFERENCIA,
                            'produto': produto.nome_produto,
                            'id_produto': produto.id_produto,
                            'loja_origem': excesso.id_loja,
                            'loja_destino': falta.id_loja,
                            'quantidade_transferencia': quantidade_transferencia
                        })
        return sugestoes

    def gerar_ordem_compra(self):
        """
        Gera ordens de compra para produtos com estoque abaixo do mínimo.

        Retorno:
            List[dict]: Lista de ordens de compra com informações sobre o produto, loja e quantidade a comprar.
        """
        ordens = []
        produtos = self.blackboard.listar_produtos()
        for produto in produtos:
            estoque = self.blackboard.listar_estoque_por_produto(produto.id_produto)
            for item in estoque:
                if item.quantidade < produto.estoque_minimo:
                    quantidade_compra = self.estrategia_reposicao.calcular_reposicao(produto, item.quantidade)
                    ordens.append({
                        'tipo': TipoMovimentacao.ORDEM_COMPRA,
                        'produto': produto.nome_produto,
                        'id_produto': produto.id_produto,
                        'loja': item.id_loja,
                        'quantidade_compra': quantidade_compra
                    })
        return ordens
    

if __name__ == "__main__":
    from src.database.database import SessionLocal, engine, Base

    db = SessionLocal()

    blackboard = Blackboard(db)
    blackboard = Blackboard()
    gerenciador = GerenciadorDeEstoque(blackboard, estrategia_reposicao=EstrategiaAgressiva())
    print(gerenciador.verificar_estoque_minimo())
    print(gerenciador.sugerir_reposicao())
    print(gerenciador.sugerir_transferencias())
    print(gerenciador.gerar_ordem_compra())