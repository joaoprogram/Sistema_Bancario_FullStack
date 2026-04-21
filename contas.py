class Conta():
    def __init__(self, nome, cpf, senha):
        self.nome = nome
        self.cpf = cpf
        self.senha = senha
        self.saldo = 0

    def criar__conta(self, nome, cpf, senha):
        return Conta(nome, cpf, senha)

    def deposito(self, valor):
        self.saldo += valor
    
    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
            return True
        return False
    
    def mostrar_saldo(self):
        print(f"Saldo: R$ {self.saldo}")