class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha
    def __str__(self):
        return f'Usuario: {self.nome}'