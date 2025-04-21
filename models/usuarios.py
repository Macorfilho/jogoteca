from models import db

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), primary_key=True)
    nickname = db.Column(db.String(8), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Usuarios {self.nome}>'