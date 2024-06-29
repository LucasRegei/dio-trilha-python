from abc import ABC, abstractmethod

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = [] # Lista de Contas

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)
    
    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf

    @property
    def nome(self):
        return self._nome
    
    @property
    def data_nascimento(self):
        return self._data_nascimento
    
    @property
    def cpf(self):
        return self._cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    def sacar(self, valor):
        saldo = self.saldo
      
        if valor > saldo:
            print("Algo deu errado! Saldo insuficiente.")
            return False
        elif valor > 0:
            self._saldo -= valor
            saldo = self.saldo
            print(f"Novo saldo: R$ {saldo:.2f}")
            return True
        else:
            print("Algo deu errado! Verifique o valor inserido.")
            return False
        
    def depositar(self, valor):

        if valor > 0:
            self._saldo += valor
            saldo = self.saldo
            print(f"Novo saldo: R$ {saldo:.2f}")
            return True
        else:
            print("Algo deu errado! Verifique o valor inserido.")
            return False
        
    @classmethod
    def nova_conta(self, cliente, numero):
        return self(cliente, numero)
    
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

class ContaCorrente(Conta):
    def __init__(self, numero, cliente):
        super().__init__(numero, cliente)
        self._limite = 500
        self._limite_saques = 3
    
    def sacar(self, valor):
        limite = self._limite
        limite_saques = self._limite_saques
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes 
            if transacao["tipo"] == "Saque"]
        ) # Verifica o numero de saques, usando o tamanho da lista e o tipo de transação.


        if numero_saques >= limite_saques:
            print("Algo deu errado! Limite de saque diário excedido.")
            return False
        elif valor > limite:
            print("Algo deu errado! Valor de saque excede o limite.")
            return False
        else:
            return super().sacar(valor) # Retorna a função "sacar" da classe "Pai".
    
    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saques(self):
        return self._limite_saques

class Transacao(ABC): # Interface utilizando o "Abstract Base Class"
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor) == True:
            conta.historico.adicionar_transacao(self)
    
    @property
    def valor(self):
        return self._valor

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor) == True:
            conta.historico.adicionar_transacao(self)
    
    @property
    def valor(self):
        return self._valor

class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor
            })

    @property
    def transacoes(self):
        return self._transacoes

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes 
                          if cliente.cpf == cpf]
    
    if clientes_filtrados:
        return clientes_filtrados[0]
    else:
        return None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Algo deu errado! Cliente não possui conta.")
        return None
    else:
        return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o número do CPF: ")
    check_cliente = filtrar_cliente(cpf, clientes)

    if not check_cliente:
        print("Algo deu errado! Cliente não encontrado.")
        return None
    else:
        valor = float(input("Valor a ser depósitado: "))
        transacao = Deposito(valor)
        conta = recuperar_conta_cliente(check_cliente)

        if conta == None:
            return None
        else:
            check_cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o número do CPF: ")
    check_cliente = filtrar_cliente(cpf, clientes)

    if not check_cliente:
        print("Algo deu errado! Cliente não encontrado.")
        return None
    else:
        valor = float(input("Valor a ser sacado: "))
        transacao = Saque(valor)
        conta = recuperar_conta_cliente(check_cliente)

        if not conta:
            return None
        else:
            check_cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o número do CPF: ")
    check_cliente = filtrar_cliente(cpf, clientes)

    if not check_cliente:
        print("Algo deu errado! Cliente não encontrado.")
        return None
    else:
        conta = recuperar_conta_cliente(check_cliente)
       
        if not conta:
            return None
        else:
            print(" Extrato ".center(40, "="))
            transacoes = conta.historico.transacoes
            extrato = ""

            if not transacoes:
                print("Não foram realizadas operações")
            else:
                for transacao in transacoes:
                    extrato += f"\n{transacao['tipo']}: R${transacao['valor']:.2f}"
            
            print(extrato)
            print("=".center(40, "="))

def criar_cliente(clientes):
    cpf = input("Informe o número do CPF: ")
    check_cliente = filtrar_cliente(cpf, clientes)

    if check_cliente:
        print("Algo deu errado! Cliente já existe.")
        return None
    else:
        nome = input("Nome completo: ")
        data_nascimento = input("Data de Nascimento (DD-MM-AAAA): ")
        endereco = input("Endereço (Logradouro, Número - Bairro - Cidade/Sigla do Estado): ")

        cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
        clientes.append(cliente)
        print("Usuário Criado!")


def criar_conta(clientes, numero_conta, contas):
    cpf = input("Informe o número do CPF: ")
    check_cliente = filtrar_cliente(cpf, clientes)

    if not check_cliente:
        print("Algo deu errado! Cliente não encontrado.")
        return None
    else:
        conta = ContaCorrente.nova_conta(cliente=check_cliente, numero=numero_conta)
        contas.append(conta)
        check_cliente.contas.append(conta)
        print("Conta Criada!")


def main():
    clientes = []
    contas =  []
    num_contas = len(contas) + 1

    menu = """ 
================ Banco =================
1 - Depositar
2 - Sacar
3 - Extrato
4 - Criar Cliente
5 - Criar Conta

0 - Sair
========================================
=> """

    while True:
        opcao = int(input(menu))

        if opcao == 1: # Opção "Depositar".
            depositar(clientes)

        elif opcao == 2: # Opção "Sacar".
            sacar(clientes)
            
        elif opcao == 3: # Opção "Extrato".
            exibir_extrato(clientes)

        elif opcao == 4: # Opção "Novo Cliente".
            criar_cliente(clientes)

        elif opcao == 5: # Opção "Nova Conta".
            criar_conta(clientes, num_contas, contas)

        elif opcao == 0: # Opção "Sair"
            break
        else:
            print("Algo deu errado! Selecione novamente a operação desejada.")
        
main()

