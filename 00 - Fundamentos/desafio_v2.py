def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Operação - Depósito: R$ {valor:.2f}\n"
        print(f"Novo saldo: R$ {saldo:.2f}")
    else:
        print("Algo deu errado! Verifique o valor inserido.")
    
    return saldo, extrato

def sacar (*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_saques >= limite_saques:
        print("Algo deu errado! Limite de saque diário excedido.")
    elif valor > limite:
        print("Algo deu errado! Valor de saque excede o limite.")
    elif valor > saldo:
        print("Algo deu errado! Saldo insuficiente.")
    elif valor > 0:
        saldo -= valor
        numero_saques += 1
        extrato += f"Operação - Saque: R$ {valor:.2f}\n"
        print(f"Novo saldo: R$ {saldo:.2f}")
    else:
        print("Algo deu errado! Verifique o valor inserido.")
    
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print(" Extrato ".center(40, "="))
    if extrato:
        print(extrato)
    else:
        print("Não foram realizadas operações")
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("=".center(40, "="))

def filtrar_usuario(cpf, lista_usuarios):
    for usuario in lista_usuarios:
        if usuario["cpf"] == cpf:
            return usuario 
    

def criar_usuario(lista_usuarios):
    cpf = input("Informe o número do CPF: ")
    check_usuario = filtrar_usuario(cpf, lista_usuarios)

    if check_usuario != None:
        print("Algo deu errado! Usuário já existente.")
        return None
    else:
        nome = input("Nome completo: ")
        data_nascimento = input("Data de Nascimento (DD-MM-AAAA): ")
        endereco = input("Endereço (Logradouro, Número - Bairro - Cidade/Sigla do Estado): ")

        lista_usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
        return print("Usuário Criado!")

def criar_conta(agencia, numero_conta, lista_usuarios):
    cpf = input("Informe o número do CPF: ")
    check_usuario = filtrar_usuario(cpf, lista_usuarios)

    if check_usuario != None:
        print("Conta Criada!")
        conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": check_usuario}
        return conta
    else:
        print("Algo deu errado! Usuário não encontrado.")
        return None


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    lista_usuarios = [] # É um dicionário.
    lista_contas = [] # É um dicionário.
    numero_contas = 1

    menu = """ 
=================Banco==================
1 - Depositar
2 - Sacar
3 - Extrato
4 - Criar Usuário
5 - Criar Conta

0 - Sair
========================================
=> """

    while True:
        opcao = int(input(menu))

        if opcao == 1: # Opção "Depositar".
            valor = float(input("Valor a ser depósitado: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == 2: # Opção "Sacar".
            valor = float(input("Valor a ser sacado: "))
            saldo, extrato, numero_saques = sacar(saldo=saldo,
                                                  valor=valor,
                                                  extrato=extrato,
                                                  limite=limite,
                                                  numero_saques = numero_saques,
                                                  limite_saques = LIMITE_SAQUES)
            
        elif opcao == 3: # Opção "Extrato".
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == 4: # Opção "Novo Usuário".
            criar_usuario(lista_usuarios)

        elif opcao == 5: # Opção "Nova Conta".
            check_conta = criar_conta(AGENCIA, numero_contas, lista_usuarios)
            
            if check_conta == True:
                lista_contas.append(check_conta)
                numero_contas += 1

        elif opcao == 0: # Opção "Sair"
            break
        else:
            print("Algo deu errado! Selecione novamente a operação desejada.")
        
main()

