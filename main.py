from flask import Flask, render_template, request, redirect, session, url_for
from conexao_banco_de_dados import inserir_usuario, ver_dados, depositar, sacar, pegar_saldo
import datetime
import psycopg2
from utilidades import codificar, validar_senha
import os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("key")

app = Flask(__name__)
app.secret_key = key

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

        if validar_senha(senha) == True:
            senha = codificar(senha)
        else:
            return "Erro ao cadastrar usuário. Senha inválida."

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

        user = ver_dados(confirma_cpf, confirma_senha)

        if user:
            print(user)
            nome = user[1]
            session['cpf'] = confirma_cpf
            session['nome'] = nome
            return redirect(url_for('entrada'))
        else:
            return 'Entrada inválida'

    return render_template('login.html')

@app.route('/conta', methods=['GET', 'POST'])
def entrada():
    if request.method == 'POST':

        valor = float(request.form.get('valor'))
        cpf = session.get('cpf')
        acao = request.form.get('acao')

        if acao == 'deposito':
            depositar(valor, cpf)

        elif acao == 'saque':
            sacar(valor, cpf)

    nome = session.get('nome')
    cpf = session.get('cpf')
    saldo = pegar_saldo(cpf)

    return render_template('conta.html', nome=nome, saldo=saldo)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))