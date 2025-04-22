from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models.jogos import Jogos
from models import db
from models.usuarios import Usuarios
from jogoteca import app
from helpers import recupera_imagem, deletar_arquivo
import time

@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Você precisa fazer login para adicionar um jogo!')
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Você precisa fazer login para editar um jogo!')
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    jogo = Jogos.query.filter_by(id=id).first()
    capa_jogo = recupera_imagem(jogo.id)
    return render_template('editar.html', titulo='Editar Jogo', jogo=jogo, capa_jogo=capa_jogo)

@app.route('/atualizar', methods=['POST'])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']
    db.session.add(jogo)
    db.session.commit()
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    if arquivo and arquivo.filename:
        # only delete and save when a new file is uploaded
        deletar_arquivo(jogo.id)
        arquivo.save(f'{upload_path}/{jogo.id}-{timestamp}.jpg')
    flash('Jogo atualizado com sucesso!')
    return redirect(url_for('index'))

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já existe!')
        return redirect(url_for('index'))
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()
    timestamp = time.time()
    arquivo.save(f'{upload_path}/{novo_jogo.id}-{timestamp}.jpg')
    flash('Jogo adicionado com sucesso!')
    
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Você precisa fazer login para excluir um jogo!')
        return redirect(url_for('login', proxima=url_for('deletar', id=id)))
    jogo = Jogos.query.filter_by(id=id).first()
    db.session.delete(jogo)
    db.session.commit()
    deletar_arquivo(jogo.id)
    flash('Jogo excluído com sucesso!')
    return redirect(url_for('index'))
    
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Login', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nome + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário ou senha inválidos!')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Deslogado com sucesso!')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('static/uploads', nome_arquivo)
