from flask import Flask, render_template, request, redirect, session, flash
from models.jogo import Jogo

jogo1 = Jogo('God of War', 'Ação', 'PS4')
jogo2 = Jogo('Fifa 22', 'Esporte', 'PS4')
jogo3 = Jogo('Minecraft', 'Aventura', 'PC')
lista = [jogo1, jogo2, jogo3]

app = Flask(__name__)

app.secret_key = 'alura'

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Você precisa fazer login para adicionar um jogo!')
        return redirect('/login')
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html', titulo='Login')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if 'alohomora' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash(session['usuario_logado'] + ' logado com sucesso!')
        return redirect('/')
    else:
        flash('Usuário ou senha inválidos!')
        return redirect('/login')
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Deslogado com sucesso!')
    return redirect('/')
    

app.run(debug=True)