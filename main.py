from flask import Flask, render_template, request, redirect, session, url_for
from contas import Conta
import hashlib
from db import inserir_usuario
import datetime

app = Flask(__name__)

def hash(txt):
    hash_obj = hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()

@app.route('/')
def home():

    return render_template('home_page.html')

@app.route('/cadastrar', methods=['POST', 'GET'])
def conta():
    if request.method == 'POST':
        nome = request.form.get('nome').capitalize()
        if 2 < len(nome) > 49:
            return 'Nome inválido'
        
        email = request.form.get('email')

        cpf = request.form.get('cpf')
        if not cpf.isdigit() or len(cpf) != 11:
            return 'CPF inválido'
        
        senha = request.form.get('senha')
        if len(senha) >= 6:
            senha = hash(senha)
        else:
            return 'Senha inválida'

        if inserir_usuario(nome, email, cpf, senha):
            return redirect(url_for('home'))
        else:
            return "Erro ao cadastrar usuário. Tente novamente."

    return render_template('cadastro.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        confirma_cpf = request.form.get('cpf_confirma')
        confirma_senha = request.form.get('senha_confirma')

        print(confirma_cpf)
        print(confirma_senha)

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)