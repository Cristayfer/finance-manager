import tkinter as tk
from tkinter import messagebox
from banco import (
    calcular_saldo, 
    inserir_movimentacao, 
    listar_movimentacoes,
    editar_movimentacao,
    excluir_movimentacao
)

def iniciar_interface():


    janela = tk.Tk()

    janela.title("Controle financeiro")
    janela.geometry("1200x800")
    janela.resizable(False, False)

    total_entradas, total_despesas, saldo = calcular_saldo()

    def formatar_valor(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    titulo = tk.Label(
        janela,
        text="CONTROLE FINANCEIRO",
        font=("Arial", 24, "bold")
    )

    titulo.pack(pady=30)

    frame_cartoes = tk.Frame(janela)
    frame_cartoes.pack(pady=20)

    cartao_saldo = tk.Frame(
        frame_cartoes,
        width=250,
        height=150,
        relief="solid",
        borderwidth=1

    )

    cartao_saldo.pack(side="left", padx=10)
    cartao_saldo.pack_propagate(False)

    tk.Label(
        cartao_saldo,
        text="Saldo atual",
        font=("Arial", 14)
    ).pack(pady=(20, 10))

    label_saldo = tk.Label(
        cartao_saldo,
        text=formatar_valor(saldo),
        font=("Arial", 22, "bold")
    )
    label_saldo.pack()


    cartao_entradas = tk.Frame(
        frame_cartoes,
        width=250,
        height=150,
        relief="solid",
        borderwidth=1
    )

    cartao_entradas.pack(side="left", padx=10)
    cartao_entradas.pack_propagate(False)

    tk.Label(
        cartao_entradas,
        text="Total de entradas",
        font=("Arial", 14)
    ).pack(pady=(20, 10))

    label_entradas = tk.Label(
        cartao_entradas,
        text=formatar_valor(total_entradas),
        font=("Arial", 22, "bold")
    )
    label_entradas.pack()


    cartao_despesas = tk.Frame(
        frame_cartoes,
        width=250,
        height=150,
        relief="solid",
        borderwidth=1
    )

    cartao_despesas.pack(side="left", padx=10)
    cartao_despesas.pack_propagate(False)


    tk.Label(
        cartao_despesas,
        text="Total de despesas",
        font=("Arial", 14)
    ).pack(pady=(20, 10))

    label_despesas = tk.Label(
        cartao_despesas,
        text=formatar_valor(total_despesas),
        font=("Arial", 22, "bold")
    )
    label_despesas.pack()

    def atualizar_interface():
        total_entradas, total_despesas, saldo = calcular_saldo()

        label_saldo.config(
            text=formatar_valor(saldo)
        )

        label_entradas.config(
            text=formatar_valor(total_entradas)
        )

        label_despesas.config(
            text=formatar_valor(total_despesas)
        )

        carregar_movimentacoes()


    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=30)

    def nova_entrada():
        janela_entrada = tk.Toplevel(janela)
        janela_entrada.title("Nova entrada")
        janela_entrada.geometry("400x300")
        janela_entrada.resizable(False, False)

        tk.Label(
            janela_entrada,
            text="Nova entrada",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        tk.Label(
            janela_entrada,
            text="Descrição:"
        ).pack()

        campo_descricao = tk.Entry(
            janela_entrada,
            width=35
        )
        campo_descricao.pack(pady=5)

        tk.Label(
            janela_entrada,
            text="Valor:"
        ).pack()

        campo_valor = tk.Entry(
            janela_entrada,
            width=35
        )
        campo_valor.pack(pady=5)

        def cadastrar():
            descricao = campo_descricao.get()
            valor = campo_valor.get()

            if descricao == "" or valor == "":
                return

            valor = valor.replace(",", ".")

            try:
                valor = float(valor)
            except ValueError:
                return

            inserir_movimentacao(
                "entrada",
                descricao,
                valor
            )

            atualizar_interface()
            janela_entrada.destroy()

        botao_cadastrar = tk.Button(
            janela_entrada,
            text="Cadastrar",
            width=20,
            command=cadastrar
        )
        botao_cadastrar.pack(pady=25)

        janela_entrada.bind("<Return>", lambda event: cadastrar())

    def nova_despesa():
        janela_despesa = tk.Toplevel(janela)
        janela_despesa.title("Nova despesa")
        janela_despesa.geometry("400x300")
        janela_despesa.resizable(False, False)

        tk.Label(
            janela_despesa,
            text="Nova despesa",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        tk.Label(
            janela_despesa,
            text="Descrição:"
        ).pack()

        campo_descricao = tk.Entry(
            janela_despesa,
            width=35
        )
        campo_descricao.pack(pady=5)

        tk.Label(
            janela_despesa,
            text="Valor:"
        ).pack()

        campo_valor = tk.Entry(
            janela_despesa,
            width=35
        )
        campo_valor.pack(pady=5)

        def cadastrar():
            descricao = campo_descricao.get()
            valor = campo_valor.get()

            if descricao == "" or valor == "":
                return

            valor = valor.replace(",", ".")

            try:
                valor = float(valor)
            except ValueError:
                return

            inserir_movimentacao(
                "despesa",
                descricao,
                valor
            )
            
            atualizar_interface()
            janela_despesa.destroy()

        botao_cadastrar = tk.Button(
            janela_despesa,
            text="Cadastrar",
            width=20,
            command=cadastrar
        )
        botao_cadastrar.pack(pady=25)

        janela_despesa.bind("<Return>", lambda event: cadastrar())
        
    tk.Button(
        frame_botoes,
        text="+ Nova entrada",
        font=("Arial", 12, "bold"),
        width=18,
        command=nova_entrada
    ).pack(side="left", padx=10)

    tk.Button(
        frame_botoes,
        text="+ Nova despesa",
        font=("Arial", 12, "bold"),
        width=18,
        command=nova_despesa
    ).pack(side="left", pady=10)

    tk.Label(
        janela,
        text="Movimentações",
        font=("Arial", 18, "bold")
    ).pack(pady=(10, 5))

    frame_movimentacoes = tk.Frame(janela)
    frame_movimentacoes.pack()

    def carregar_movimentacoes():
        for widget in frame_movimentacoes.winfo_children():
            widget.destroy()

        movimentacoes = listar_movimentacoes()


        largura_data = 120
        largura_tipo = 100
        largura_descricao = 220
        largura_valor = 120
        largura_acoes = 180

        larguras = [
            largura_data,
            largura_tipo,
            largura_descricao,
            largura_valor,
            largura_acoes
        ]


        tabela = tk.Frame(
            frame_movimentacoes,
            bg="#f4f4f4"
        )

        tabela.pack()

        # Define as larguras FIXAS das colunas
        for coluna, largura in enumerate(larguras):
            tabela.grid_columnconfigure(
                coluna,
                minsize=largura,
                weight=0
            )


        cabecalhos = [
            "DATA",
            "TIPO",
            "DESCRIÇÃO",
            "VALOR",
            "AÇÕES"
        ]

        for coluna, texto in enumerate(cabecalhos):

            tk.Label(
                tabela,
                text=texto,
                font=("Arial", 9, "bold"),
                bg="#f4f4f4",
                fg="#555555"
            ).grid(
                row=0,
                column=coluna,
                sticky="nsew",
                pady=(0, 8)
            )

        for linha, movimentacao in enumerate(
            movimentacoes,
            start=1
        ):

            id_mov, tipo, descricao, valor, data = movimentacao

            tk.Label(
                tabela,
                text=data,
                font=("Arial", 9),
                bg="white",
                fg="#333333",
                highlightbackground="#dddddd",
                highlightthickness=1
            ).grid(
                row=linha,
                column=0,
                sticky="nsew",
                padx=(0, 1),
                pady=3,
                ipady=7
            )

            cor_tipo = (
                "#198754"
                if tipo == "entrada"
                else "#dc3545"
            )

            tk.Label(
                tabela,
                text=tipo.capitalize(),
                font=("Arial", 9, "bold"),
                bg="white",
                fg=cor_tipo,
                highlightbackground="#dddddd",
                highlightthickness=1
            ).grid(
                row=linha,
                column=1,
                sticky="nsew",
                padx=(0, 1),
                pady=3,
                ipady=7
            )


            tk.Label(
                tabela,
                text=descricao,
                font=("Arial", 9),
                bg="white",
                fg="#222222",
                anchor="w",
                highlightbackground="#dddddd",
                highlightthickness=1
            ).grid(
                row=linha,
                column=2,
                sticky="nsew",
                padx=(0, 1),
                pady=3,
                ipady=7
            )

            tk.Label(
                tabela,
                text=formatar_valor(valor),
                font=("Arial", 9, "bold"),
                bg="white",
                fg="#222222",
                anchor="e",
                highlightbackground="#dddddd",
                highlightthickness=1
            ).grid(
                row=linha,
                column=3,
                sticky="nsew",
                padx=(0, 1),
                pady=3,
                ipady=7
            )

            frame_acoes = tk.Frame(
                tabela,
                bg="white",
                highlightbackground="#dddddd",
                highlightthickness=1
            )

            frame_acoes.grid(
                row=linha,
                column=4,
                sticky="nsew",
                pady=3
            )

            tk.Button(
                frame_acoes,
                text="Editar",
                font=("Arial", 8),
                width=7,
                relief="flat",
                bg="#eeeeee",
                activebackground="#dddddd",
                command=lambda id_mov=id_mov,
                tipo=tipo,
                descricao=descricao,
                valor=valor: editar_janela(
                    id_mov,
                    tipo,
                    descricao,
                    valor
                )
            ).pack(
                side="left",
                padx=5,
                pady=5
            )

            tk.Button(
                frame_acoes,
                text="Excluir",
                font=("Arial", 8),
                width=7,
                relief="flat",
                bg="#eeeeee",
                activebackground="#dddddd",
                command=lambda id_mov=id_mov: excluir(id_mov)
            ).pack(
                side="left",
                padx=2,
                pady=5
            )

    def excluir(id_movimentacao):
        resposta = messagebox.askquestion(
            "Confirmar exclusão",
            "Deseja realmente excluir esta movimentação?"
        )

        if resposta:
            excluir_movimentacao(id_movimentacao)
            atualizar_interface()


    def editar_janela(id_mov, tipo, descricao, valor):

        janela_edicao = tk.Toplevel(janela)
        janela_edicao.title("Editar movimentação")
        janela_edicao.geometry("400x350")
        janela_edicao.resizable(False, False)

        tk.Label(
            janela_edicao,
            text="Editar movimentação",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        tk.Label(
            janela_edicao,
            text="Descrição:"
        ).pack()

        campo_descricao = tk.Entry(
            janela_edicao,
            width=35
        )
        campo_descricao.pack(pady=5)

        campo_descricao.insert(0, descricao)

        tk.Label(
            janela_edicao,
            text="Valor:"
        ).pack()

        campo_valor = tk.Entry(
            janela_edicao,
            width=35
        )
        campo_valor.pack(pady=5)

        campo_valor.insert(0, str(valor).replace(".", ","))

        def salvar():

            nova_descricao = campo_descricao.get()
            novo_valor = campo_valor.get()

            if nova_descricao == "" or novo_valor == "":
                return

            novo_valor = novo_valor.replace(",", ".")

            try:
                novo_valor = float(novo_valor)
            except ValueError:
                return

            editar_movimentacao(
                id_mov,
                tipo,
                nova_descricao,
                novo_valor
            )

            janela_edicao.destroy()

            atualizar_interface()

        tk.Button(
            janela_edicao,
            text="Salvar",
            width=20,
            command=salvar
        ).pack(pady=25)

        janela_edicao.bind(
            "<Return>",
            lambda event: salvar()
        )

    carregar_movimentacoes()

    
    janela.mainloop()

