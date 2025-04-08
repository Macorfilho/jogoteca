from flask import Flask, render_template, request, redirect
from models.jogo import Jogo

jogo1 = Jogo('God of War', 'Ação', 'PS4')
jogo2 = Jogo('Fifa 22', 'Esporte', 'PS4')
jogo3 = Jogo('Minecraft', 'Aventura', 'PC')
lista = [jogo1, jogo2, jogo3]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect('/')
    

app.run(debug=True)