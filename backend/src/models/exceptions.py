class VendaException(Exception):
    """Exceção base para erros relacionados a vendas."""
    pass

class EstoqueInsuficienteException(VendaException):
    """Lançada quando não há estoque suficiente para a venda."""
    pass

class QuantidadeInvalidaException(VendaException):
    """Lançada quando a quantidade do item é inválida (ex: negativa ou zero)."""
    pass

class ErroBancoException(VendaException):
    """Erro genérico ao interagir com o banco de dados."""
    pass