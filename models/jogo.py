class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

    def __str__(self):
        return f'Nome: {self.nome}, Categoria: {self.categoria}, Console: {self.console}'