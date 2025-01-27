from .LojaA import LojaA
from .LojaB import LojaB
from .LojaC import LojaC

# Vantagens de Usar o Factory Method:

# Desacoplamento -> O código que usa o Factory não precisa saber detalhes sobre qual classe específica de loja está sendo instanciada. Isso melhora a manutenibilidade e a flexibilidade do código.
# Facilidade de expansão -> Se você adicionar mais tipos de lojas no futuro, só precisará atualizar a fábrica, sem alterar o código que utiliza as lojas.
# Organização -> O Factory ajuda a manter o código mais organizado e evita a repetição de código para a criação de objetos complexos.

class LojaFactory:
    @staticmethod
    def criar_loja(tipo_loja, blackboard):
        """Método de fábrica para criar lojas de diferentes tipos."""
        if tipo_loja == 'LojaA':
            return LojaA(blackboard)
        elif tipo_loja == 'LojaB':
            return LojaB(blackboard)
        elif tipo_loja == 'LojaC':
            return LojaC(blackboard)
        else:
            raise ValueError(f"Tipo de loja {tipo_loja} não reconhecido")