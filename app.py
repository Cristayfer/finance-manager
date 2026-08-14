from banco import criar_tabela, inserir_movimentacao, listar_movimentacoes, calcular_saldo
criar_tabela()

def mostrar_menu():
    print("================================")
    print("     CONTROLE FINANCEIRO")
    print("================================")


    print("1 - Nova movimentação")
    print("2 - Ver movimentação")
    print("3 - Ver saldo")
    print("4 - Sair")

def cadastrar_movimentacao():
    while True:
        tipo = input("Digite o tipo (entrada/despesa): ").lower()

        if tipo == "entrada" or tipo == "despesa":
            break
        print("Tipo inválido. Digite entrada ou despesa.")

    descricao = input("Digite a descrição: ")

    try:
        valor = float(input("Digite o valor: "))
    except ValueError:
        print("Valor inválido!")
        return
    
    inserir_movimentacao(tipo, descricao, valor)
    print()
    print("Movimentação cadastrada")
    print()
    print("Tipo:", tipo)
    print("Descrição:", descricao)
    print("Valor: R$", valor)

    

while True:

    mostrar_menu()

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_movimentacao()

    elif opcao == "2":
        movimentacoes = listar_movimentacoes()

        print()
        print("========== MOVIMENTAÇÕES ==========")

        if not movimentacoes:
            print("Nenhuma movimentação encontrada.")
        else:
            for movimentacao in movimentacoes:
                id_mov, tipo, descricao, valor = movimentacao

                print(f"ID: {id_mov}")
                print(f"Tipo: {tipo}")
                print(f"Descrição: {descricao}")
                print(f"Valor: R$ {valor:.2f}")
                print("--------------------------------")

    elif opcao == "3":
        total_entradas, total_despesas, saldo = calcular_saldo()

        print()
        print("============== SALDO ==============")
        print(f"Total de entradas: R$ {total_entradas:.2f}")
        print(f"Total de despesas: R$ {total_despesas:.2f}")
        print(f"Saldo Atual:       R$ {saldo:.2f}")

    elif opcao == "4":
        print("Saindo do programa...")
        break

    else:
        print("Opção inválida.")
        

