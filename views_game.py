from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models.jogos import Jogos
from models import db
from jogoteca import app
from helpers import recupera_imagem, deletar_arquivo, FormularioJogo
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
    form = FormularioJogo()
    return render_template('novo.html', titulo='Novo Jogo', form=form)

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Você precisa fazer login para editar um jogo!')
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    jogo = Jogos.query.filter_by(id=id).first()
    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    capa_jogo = recupera_imagem(jogo.id)
    return render_template('editar.html', titulo='Editar Jogo', id=id, capa_jogo=capa_jogo, form=form)

@app.route('/atualizar', methods=['POST'])
def atualizar():
    form = FormularioJogo(request.form)
    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data
        db.session.add(jogo)
        db.session.commit()
        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        if arquivo and arquivo.filename:
            deletar_arquivo(jogo.id)
            arquivo.save(f'{upload_path}/{jogo.id}-{timestamp}.jpg')
        flash('Jogo atualizado com sucesso!')
    return redirect(url_for('index'))

@app.route('/criar', methods=['POST'])
def criar():
    form = FormularioJogo(request.form)  
    if not form.validate_on_submit():
        flash('Formulário inválido!')
        return redirect(url_for('novo'))
    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data
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

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('static/uploads', nome_arquivo)
