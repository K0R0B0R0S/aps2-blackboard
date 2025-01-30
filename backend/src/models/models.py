from sqlalchemy import (
    Column, Integer, String, Text, Numeric, Date, ForeignKey, UniqueConstraint, Index, CheckConstraint
)
from sqlalchemy.orm import relationship
from src.database.database import Base

# Modelo Loja
class Loja(Base):
    __tablename__ = 'loja'

    id_loja = Column(Integer, primary_key=True, autoincrement=True)
    nome_loja = Column(String(100), nullable=False)
    endereco = Column(String(200), nullable=False)
    telefone = Column(String(15), nullable=False)

    # Relacionamentos
    estoques = relationship("Estoque", back_populates="loja")
    vendas = relationship("Venda", back_populates="loja")

# Modelo Produto
class Produto(Base):
    __tablename__ = 'produto'

    id_produto = Column(Integer, primary_key=True, autoincrement=True)
    nome_produto = Column(String(100), nullable=False)
    descricao = Column(Text)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    estoque_minimo = Column(Integer, nullable=False)

    # Relacionamentos
    estoques = relationship("Estoque", back_populates="produto")
    itens_venda = relationship("ItemVenda", back_populates="produto")
    itens_compra = relationship("ItemCompra", back_populates="produto")

# Modelo Estoque
class Estoque(Base):
    __tablename__ = 'estoque'

    id_estoque = Column(Integer, primary_key=True, autoincrement=True)
    id_loja = Column(Integer, ForeignKey('loja.id_loja'), nullable=False)
    id_produto = Column(Integer, ForeignKey('produto.id_produto'), nullable=False)
    quantidade = Column(Integer, nullable=False)

    # Constraints
    __table_args__ = (
        UniqueConstraint('id_loja', 'id_produto', name='uq_estoque_loja_produto'),
        Index('idx_estoque_produto', 'id_produto'),
        CheckConstraint('quantidade >= 0', name='chk_quantidade_positiva'),
    )

    # Relacionamentos
    loja = relationship("Loja", back_populates="estoques")
    produto = relationship("Produto", back_populates="estoques")

# Modelo Fornecedor
class Fornecedor(Base):
    __tablename__ = 'fornecedor'

    id_fornecedor = Column(Integer, primary_key=True, autoincrement=True)
    nome_fornecedor = Column(String(100), nullable=False)
    cnpj = Column(String(14), nullable=False, unique=True)
    telefone = Column(String(15), nullable=False)
    endereco = Column(String(200), nullable=False)

    # Relacionamentos
    compras = relationship("Compra", back_populates="fornecedor")

# Modelo Compra
class Compra(Base):
    __tablename__ = 'compra'

    id_compra = Column(Integer, primary_key=True, autoincrement=True)
    id_fornecedor = Column(Integer, ForeignKey('fornecedor.id_fornecedor'), nullable=False)
    data_compra = Column(Date, nullable=False)
    valor_total = Column(Numeric(10, 2), nullable=False)

    # Relacionamentos
    fornecedor = relationship("Fornecedor", back_populates="compras")
    itens_compra = relationship("ItemCompra", back_populates="compra")

# Modelo ItemCompra
class ItemCompra(Base):
    __tablename__ = 'item_compra'

    id_item_compra = Column(Integer, primary_key=True, autoincrement=True)
    id_compra = Column(Integer, ForeignKey('compra.id_compra'), nullable=False)
    id_produto = Column(Integer, ForeignKey('produto.id_produto'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)

    # Relacionamentos
    compra = relationship("Compra", back_populates="itens_compra")
    produto = relationship("Produto", back_populates="itens_compra")

# Modelo Venda
class Venda(Base):
    __tablename__ = 'venda'

    id_venda = Column(Integer, primary_key=True, autoincrement=True)
    id_loja = Column(Integer, ForeignKey('loja.id_loja'), nullable=False)
    data_venda = Column(Date, nullable=False)
    valor_total = Column(Numeric(10, 2), nullable=False)

    # Relacionamentos
    loja = relationship("Loja", back_populates="vendas")
    itens_venda = relationship("ItemVenda", back_populates="venda")

    # Índices
    __table_args__ = (
        Index('idx_venda_loja', 'id_loja'),
    )

# Modelo ItemVenda
class ItemVenda(Base):
    __tablename__ = 'item_venda'

    id_item_venda = Column(Integer, primary_key=True, autoincrement=True)
    id_venda = Column(Integer, ForeignKey('venda.id_venda'), nullable=False)
    id_produto = Column(Integer, ForeignKey('produto.id_produto'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)

    # Relacionamentos
    venda = relationship("Venda", back_populates="itens_venda")
    produto = relationship("Produto", back_populates="itens_venda")

Base = Base
