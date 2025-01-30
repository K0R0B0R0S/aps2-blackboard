from abc import ABC, abstractmethod

class EstrategiaReposicao(ABC):
    """
    Interface para estratégias de cálculo de reposição de estoque.
    """
    @abstractmethod
    def calcular_reposicao(self, produto, quantidade_atual):
        pass

class EstrategiaConservadora(EstrategiaReposicao):
    """
    Estratégia conservadora: repõe apenas o necessário para atingir o estoque mínimo.
    """
    def calcular_reposicao(self, produto, quantidade_atual):
        return max(0, produto.estoque_minimo - quantidade_atual)

class EstrategiaAgressiva(EstrategiaReposicao):
    """
    Estratégia agressiva: repõe o dobro do estoque mínimo menos a quantidade atual.
    """
    def calcular_reposicao(self, produto, quantidade_atual):
        return max(0, produto.estoque_minimo * 2 - quantidade_atual)

class EstrategiaPersonalizada(EstrategiaReposicao):
    """
    Estratégia personalizada: repõe com base em um fator personalizado.
    """
    def __init__(self, fator):
        self.fator = fator

    def calcular_reposicao(self, produto, quantidade_atual):
        return max(0, produto.estoque_minimo * self.fator - quantidade_atual)