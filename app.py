from banco import (
    criar_tabela,
    inserir_movimentacao,
    listar_movimentacoes,
    calcular_saldo,
    excluir_movimentacao,
    editar_movimentacao
)

criar_tabela()

def mostrar_menu():
    print("================================")
    print("     CONTROLE FINANCEIRO")
    print("================================")

    print("1 - Nova movimentação")
    print("2 - Ver movimentação")
    print("3 - Ver saldo")
    print("4 - Editar movimentação")
    print("5 - Excluir movimentação")
    print("6 - Sair")


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
        try:
            id_movimentacao = int(
                input("Digite o ID da movimentação que deseja editar: ")
            )
        except ValueError:
            print("ID inválido!")
            continue

        movimentacoes = listar_movimentacoes()
        movimentacao_encontrada = None

        for movimentacao in movimentacoes:
            if movimentacao[0] == id_movimentacao:
                movimentacao_encontrada = movimentacao
                break

        if movimentacao_encontrada is None:
            print("Movimentação não encontrada.")
            continue

        print()
        print("======= MOVIMENTAÇÃO ENCONTRADA =======")
        print(f"Tipo: {movimentacao_encontrada[1]}")
        print(f"Descrição: {movimentacao_encontrada[2]}")
        print(f"Valor: R$ {movimentacao_encontrada[3]:.2f}")

        while True:
            novo_tipo = input("Digite o novo tipo (entrada/despesa): ").lower()

            if novo_tipo == "entrada" or novo_tipo == "despesa":
                break

            print("Tipo inválido. Digite entrada ou despesa.")

        nova_descricao = input("Digite a nova descrição: ")

        try:
            novo_valor = float(input("Digite o novo valor: "))
        except ValueError:
            print("Valor inválido!")
            continue

        print()
        print("======= NOVOS DADOS =======")
        print(f"Tipo: {novo_tipo}")
        print(f"Descrição: {nova_descricao}")
        print(f"Valor: R$ {novo_valor}")

        confirmacao = input("Deseja salvar as alterações? (s/n): ").lower()

        if confirmacao == "s":
            editar_movimentacao(
                id_movimentacao,
                novo_tipo,
                nova_descricao,
                novo_valor
            )
            print("Movimentação editada com sucesso.")
        else:
            print("Edição cancelada.")


    elif opcao == "5":
        try:
            id_movimentacao = int(
                input("Digite o ID da movimentação que deseja excluir: ")
            )
        except ValueError:
            print("ID inválido!")
            continue

        confirmacao = input(
            "Tem certeza que deseja excluir? (s/n): "
        ).lower()

        if confirmacao == "s":
            excluida = excluir_movimentacao(id_movimentacao)

            if excluida:
                print("Movimentação excluída com sucesso.")
            else:
                print("Movimentação não encontrada.")
        else:
            print("Exclusão cancelada.")


    elif opcao == "6":
        print("Saindo do programa...")
        break

    else:
        print("Opção inválida.")