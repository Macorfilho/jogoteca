import os
from jogoteca import app

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'{str(id)}-' in nome_arquivo:
            return nome_arquivo
    return 'imagem.jpg'

def deletar_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'imagem.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))