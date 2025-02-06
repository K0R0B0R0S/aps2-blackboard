import re
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, TextAreaField, DecimalField, SelectField, DateField, FloatField, HiddenField
from flask import session
from wtforms.validators import DataRequired, Length, Optional, Regexp, NumberRange
from wtforms import ValidationError
from datetime import datetime

class LojaForm(Form):
    loja_id = HiddenField()
    nome_loja = StringField('*Nome da Loja', validators=[DataRequired(), Length(max=100)])
    endereco = StringField('*Endereço', validators=[DataRequired(), Length(max=200)])
    telefone = StringField('*Telefone', validators=[DataRequired(), Length(max=15)])
    tipo_loja = SelectField('Tipo de Loja', choices=[('', 'Selecione um tipo...'), ('LojaA', 'Loja A'), ('LojaB', 'Loja B')], validators=[DataRequired()])

class ProdutoForm(Form):
    produto_id = HiddenField()
    nome_produto = StringField('Nome do Produto', validators=[DataRequired()])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    preco_unitario = DecimalField('Preço Unitário', validators=[DataRequired(), NumberRange(min=0)])
    estoque_minimo = IntegerField('Estoque Mínimo', validators=[DataRequired(), NumberRange(min=0)])
    
class EstoqueForm(Form):
    id_loja = IntegerField('*ID Loja', validators=[DataRequired()])
    id_produto = SelectField('*ID Produto', validators=[DataRequired()])
    quantidade = IntegerField('*Quantidade', validators=[DataRequired()])

class FornecedorForm(Form):
    fornecedor_id = HiddenField()
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
    id_loja = SelectField('*Loja', validators=[DataRequired()], coerce=int)
    id_produto = SelectField('*Produto', validators=[DataRequired()], coerce=int)
    quantidade = IntegerField('*Quantidade', validators=[DataRequired()])
    preco_unitario = DecimalField('*Preço Unitário', validators=[DataRequired()])
    data_venda = DateField('*Data da Venda', validators=[DataRequired()], default=datetime.now())

class ItemVendaForm(Form):
    id_venda = IntegerField('*ID Venda', validators=[DataRequired()])
    id_produto = IntegerField('*ID Produto', validators=[DataRequired()])
    quantidade = IntegerField('*Quantidade', validators=[DataRequired()])
    preco_unitario = DecimalField('*Preço Unitário', validators=[DataRequired()])