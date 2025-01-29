import re
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, TextAreaField, DecimalField, SelectField, DateField, FloatField
from flask import session
from wtforms.validators import DataRequired, Length, Optional, Regexp, NumberRange
from wtforms import ValidationError
from datetime import datetime

class LojaForm(Form):
    nome_loja = StringField('*Nome da Loja', validators=[DataRequired(), Length(max=100)])
    endereco = StringField('*Endereço', validators=[DataRequired(), Length(max=200)])
    telefone = StringField('*Telefone', validators=[DataRequired(), Length(max=15)])

class ProdutoForm(Form):
    nome_produto = StringField('Nome do Produto', validators=[DataRequired()])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    preco_unitario = DecimalField('Preço Unitário', validators=[DataRequired(), NumberRange(min=0)])
    estoque_minimo = IntegerField('Estoque Mínimo', validators=[DataRequired(), NumberRange(min=0)])
    
class EstoqueForm(Form):
    id_loja = IntegerField('*ID Loja', validators=[DataRequired()])
    id_produto = IntegerField('*ID Produto', validators=[DataRequired()])
    quantidade = IntegerField('*Quantidade', validators=[DataRequired()])

class FornecedorForm(Form):
    nome_fornecedor = StringField('*Nome do Fornecedor', validators=[DataRequired(), Length(max=100)])
    cnpj = StringField('*CNPJ', validators=[DataRequired(), Length(max=14)])
    telefone = StringField('*Telefone', validators=[DataRequired(), Length(max=15)])
    endereco = StringField('*Endereço', validators=[DataRequired(), Length(max=200)])

class CompraForm(Form):
    id_fornecedor = IntegerField('*ID Fornecedor', validators=[DataRequired()])
    data_compra = DateField('*Data da Compra', validators=[DataRequired()])
    valor_total = DecimalField('*Valor Total', validators=[DataRequired()])

class ItemCompraForm(Form):
    id_compra = IntegerField('*ID Compra', validators=[DataRequired()])
    id_produto = IntegerField('*ID Produto', validators=[DataRequired()])
    quantidade = IntegerField('*Quantidade', validators=[DataRequired()])
    preco_unitario = DecimalField('*Preço Unitário', validators=[DataRequired()])

class VendaForm(Form):
    id_loja = IntegerField('*ID Loja', validators=[DataRequired()])
    data_venda = DateField('*Data da Venda', validators=[DataRequired()])
    valor_total = DecimalField('*Valor Total', validators=[DataRequired()])

class ItemVendaForm(Form):
    id_venda = IntegerField('*ID Venda', validators=[DataRequired()])
    id_produto = IntegerField('*ID Produto', validators=[DataRequired()])
    quantidade = IntegerField('*Quantidade', validators=[DataRequired()])
    preco_unitario = DecimalField('*Preço Unitário', validators=[DataRequired()])