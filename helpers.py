import os
from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'{str(id)}-' in nome_arquivo:
            return nome_arquivo
    return 'imagem.jpg'

def deletar_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'imagem.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
        
class FormularioJogo(FlaskForm):
    nome = (StringField('Nome do Jogo' , [validators.DataRequired(), validators.Length(min=1, max=50)]))
    categoria = (StringField('Categoria' , [validators.DataRequired(), validators.Length(min=1, max=40)]))
    console = (StringField('Console' , [validators.DataRequired(), validators.Length(min=1, max=20)]))
    salvar = (SubmitField('Salvar'))
    
class FormularioLogin(FlaskForm):
    nickname = (StringField('Nickname' , [validators.DataRequired(), validators.Length(min=1, max=8)]))
    senha = (PasswordField('Senha' , [validators.DataRequired(), validators.Length(min=1, max=100)]))
    login = (SubmitField('Login'))