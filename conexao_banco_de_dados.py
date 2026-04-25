import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv
load_dotenv()
from utilidades import codificar

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

def conectar():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="dados",
            user="postgres",
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except Error as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None


def inserir_usuario(nome, email, cpf, senha_hash):
    conn = conectar()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO usuarios (nome, email, cpf, senha)
            VALUES (%s, %s, %s, %s)
        """, (nome, email, cpf, senha_hash))
        
        conn.commit()
        return True
        
    except Error as e:
        print(f"Erro ao inserir usuário: {e}")
        conn.rollback()   # importante em caso de erro
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

'''
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    cpf TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
);
'''

def ver_dados(cpf, senha):
    senha = codificar(senha)
    conn = conectar()
    
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE cpf = %s AND senha = %s",
        (cpf, senha)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

def sacar(valor, cpf):
    conn = conectar()

    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE usuarios SET saldo = saldo - %s WHERE cpf = %s"
        , (valor, cpf)
    )

    conn.commit()
    cursor.close()
    conn.close()

def depositar(valor, cpf):
    conn = conectar()

    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE usuarios SET saldo = saldo + %s WHERE cpf = %s"
        , (valor, cpf)
    )

    conn.commit()
    cursor.close()
    conn.close()

def pegar_saldo(cpf):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT saldo FROM usuarios WHERE cpf = %s", (cpf,))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        return resultado[0] if resultado[0] is not None else 0
    return 0