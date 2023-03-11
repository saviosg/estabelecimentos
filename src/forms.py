from wtforms import StringField, SubmitField, validators
from flask_wtf import FlaskForm

class EstabelecimentoForm(FlaskForm):
    cnpj = StringField('CNPJ', [validators.Length(min=14, max=14), validators.Regexp('^[0-9]+$')])
    nome_fantasia = StringField('Nome fantasia', [validators.Length(min=1)])
    cep = StringField('CEP', [validators.Length(min=8, max=8), validators.Regexp('^[0-9]+$')])
    telefone = StringField('Telefone', [validators.Length(min=10, max=11), validators.Regexp('^[0-9]+$')])
    email = StringField('Email', [validators.Email()])
    submit = SubmitField('Salvar')
