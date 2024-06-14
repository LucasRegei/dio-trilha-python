menu = """
=================Banco==================
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
========================================
=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == "d": # Bloco da opção de Depósito
        valor = float(input("Valor a ser depósitado: "))
        if valor > 0:
            saldo += valor
            extrato += f"Operação - Depósito: R$ {valor:.2f}\n"
            print(f"Novo saldo: R$ {saldo:.2f}")
        else:
            print("Algo deu errado! Verifique o valor inserido.")
    elif opcao == "s": # Bloco da opção de Saque
        valor = float(input("Valor a ser sacado: "))
        if numero_saques >= LIMITE_SAQUES:
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
    elif opcao == "e": #Bloco da opção de Extrato
        print(" Extrato ".center(40, "="))
        if extrato:
            print(extrato)
        else:
            print("Não foram realizadas operações")
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("========================================")
    elif opcao == ("q"):
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
