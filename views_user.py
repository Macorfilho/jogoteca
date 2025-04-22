from jogoteca import app
from flask import render_template, request, redirect, url_for, session, flash
from models.usuarios import Usuarios
from helpers import FormularioLogin
from models import db
from flask_bcrypt import check_password_hash

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioLogin()
    return render_template('login.html', titulo='Login', proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    form = FormularioLogin(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)
    if usuario and senha:
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