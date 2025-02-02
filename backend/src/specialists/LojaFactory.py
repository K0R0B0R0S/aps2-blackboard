from .LojaA import LojaA
from .LojaB import LojaB

# Vantagens de Usar o Factory Method:

# Desacoplamento -> O código que usa o Factory não precisa saber detalhes sobre qual classe específica de loja está sendo instanciada. Isso melhora a manutenibilidade e a flexibilidade do código.
# Facilidade de expansão -> Se você adicionar mais tipos de lojas no futuro, só precisará atualizar a fábrica, sem alterar o código que utiliza as lojas.
# Organização -> O Factory ajuda a manter o código mais organizado e evita a repetição de código para a criação de objetos complexos.

class LojaFactory:
    @staticmethod
    def criar_loja(tipo_loja, blackboard, nome_loja, endereco, telefone):
        """Método de fábrica para criar lojas de diferentes tipos."""
        if tipo_loja == 'LojaA':
            loja = LojaA(blackboard)
            blackboard.adicionar_loja(nome_loja, endereco, telefone)  # Usando método de adicionar loja no blackboard
            return loja
        elif tipo_loja == 'LojaB':
            loja = LojaB(blackboard)
            blackboard.adicionar_loja(nome_loja, endereco, telefone)  # Usando método de adicionar loja no blackboard
            return loja
        else:
            raise ValueError(f"Tipo de loja {tipo_loja} não reconhecido")
