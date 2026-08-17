from banco import (
    criar_tabela,
    inserir_movimentacao,
    listar_movimentacoes,
    calcular_saldo,
    excluir_movimentacao,
    editar_movimentacao,
    resumo_financeiro,
    buscar_movimentacoes
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
    print("6 - Resumo financeiro")
    print("7 - Sair")
    print("8 - Buscar movimentações")


def ler_valor():
    while True:
        try:
            valor = input("Digite o valor: ")
            valor = valor.replace(",", ".")
            valor = float(valor)

            if valor <= 0:
                print("Valor inválido. Digite um valor maior que 0.")
                continue

            return valor
        except ValueError:
            print("Valor inválido. Digite um número válido.")

def ler_descricao():
    while True:
        descricao = input("Digite a descrição: ").strip()

        if descricao:
            return descricao

        print("Descrição inválida. Digite uma descrição.")

def formatar_valor(valor):
    return f"R$ {valor:.2f}".replace(".", ",")

def cadastrar_movimentacao():
    while True:
        tipo = input("Digite o tipo (entrada/despesa): ").lower()

        if tipo == "entrada" or tipo == "despesa":
            break

        print("Tipo inválido. Digite entrada ou despesa.")

    descricao = ler_descricao()

    valor = ler_valor()

    inserir_movimentacao(tipo, descricao, valor)

    print()
    print("Movimentação cadastrada")
    print()
    print("Tipo:", tipo)
    print("Descrição:", descricao)
    print(f"Valor: {formatar_valor(valor)}")


while True:

    mostrar_menu()

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_movimentacao()

    elif opcao == "2":
        print()
        print("========== VER MOVIMENTAÇÕES ==========")
        print("1 - Todas")
        print("2 - Apenas entradas")
        print("3 - Apenas despesas")

        filtro = input("Escolha apenas uma opção: ")

        movimentacoes = listar_movimentacoes()

        if filtro == "1":
            print()
            print("========== TODAS AS MOVIMENTAÇÕES ==========")

            if not movimentacoes:
                print("Nenhuma movimentação encontrada.")
            else:
                for movimentacao in movimentacoes:
                    id_mov, tipo, descricao, valor = movimentacao

                    print(f"ID: {id_mov}")
                    print(f"Tipo: {tipo}")
                    print(f"Descrição: {descricao}")
                    print(f"Valor: {formatar_valor(valor)}")
                    print("--------------------------------")

        elif filtro == "2":
            print()
            print("========== ENTRADAS ==========")

            entradas = []

            for movimentacao in movimentacoes:
                if movimentacao[1] == "entrada":
                    entradas.append(movimentacao)

            if not entradas:
                print("Nenhuma movimentação encontrada.")

            else:
                for movimentacao in entradas:
                    id_mov, tipo, descricao, valor = movimentacao

                    print(f"ID: {id_mov}")
                    print(f"Tipo: {tipo}")
                    print(f"Descrição: {descricao}")
                    print(f"Valor: {formatar_valor(valor)}")
                    print("--------------------------------")

        elif filtro == "3":
            print()
            print("========== DESPESAS ==========")

            despesas = []

            for movimentacao in movimentacoes:
                if movimentacao[1] == "despesa":
                    despesas.append(movimentacao)

            if not despesas:
                print("Nenhuma despesa encontrada.")
            else:
                for movimentacao in despesas:
                    id_mov, tipo, descricao, valor = movimentacao

                    print(f"ID: {id_mov}")
                    print(f"Tipo: {tipo}")
                    print(f"Descrição: {descricao}")
                    print(f"Valor: {formatar_valor(valor)}")
                    print("--------------------------------")


    elif opcao == "3":
        total_entradas, total_despesas, saldo = calcular_saldo()

        print()
        print("============== SALDO ==============")
        print(f"Total de entradas: {formatar_valor(total_entradas)}")
        print(f"Total de despesas: {formatar_valor(total_despesas)}")
        print(f"Saldo Atual:       {formatar_valor(saldo)}")

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
        print(f"Valor: {formatar_valor(movimentacao_encontrada[3])}")

        while True:
            novo_tipo = input("Digite o novo tipo (entrada/despesa): ").lower()

            if novo_tipo == "entrada" or novo_tipo == "despesa":
                break

            print("Tipo inválido. Digite entrada ou despesa.")

        nova_descricao = ler_descricao()

        novo_valor = ler_valor()

        print()
        print("======= NOVOS DADOS =======")
        print(f"Tipo: {novo_tipo}")
        print(f"Descrição: {nova_descricao}")
        print(f"Valor: {formatar_valor(novo_valor)}")

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
        total_entradas, total_despesas, saldo = calcular_saldo()

        total_movimentacoes, quantidade_entradas, quantidade_despesas = resumo_financeiro()

        print()
        print("========== RESUMO FINANCEIRO ==========")
        print(f"Total de movimentações: {total_movimentacoes}")
        print(f"Quantidade de entradas: {quantidade_entradas}")
        print(f"Quantidade de despesas: {quantidade_despesas}")
        print("---------------------------------------")
        print(f"Total de entradas: {formatar_valor(total_entradas)}")
        print(f"Total despesas:    {formatar_valor(total_despesas)}")
        print(f"Saldo atual:       {formatar_valor(saldo)}")



    elif opcao == "7":
        print("Saindo do programa...")
        break

    elif opcao == "8":
        print()
        print("========== BUSCAR MOVIMENTAÇÃO ==========")

        termo = input("Digite o que deseja buscar: ").strip()

        if not termo:
            print("Digite algo para realizar a buscar.")
            continue

        movimentacoes = buscar_movimentacoes(termo)

        if not movimentacoes:
            print("Nenhuma movimentação encontrada.")
        else:
            print()
            print("========== RESULTADOS ==========")

            for movimentacao in movimentacoes:
                id_mov, tipo, descricao, valor = movimentacao

                print(f"ID: {id_mov}")
                print(f"Tipo: {tipo}")
                print(f"Descrição: {descricao}")
                print(f"Valor: {formatar_valor(valor)}")
                print("--------------------------------")

    else:
        print("Opção inválida.")
        
