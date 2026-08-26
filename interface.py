import tkinter as tk
from tkinter import messagebox
from banco import (
    calcular_saldo, 
    inserir_movimentacao, 
    listar_movimentacoes,
    editar_movimentacao,
    excluir_movimentacao,
    buscar_movimentacoes,
    resumo_financeiro
)

janela_cadastro = None

def iniciar_interface():


    janela = tk.Tk()

    janela.title("Controle financeiro")
    janela.geometry("1200x800")
    janela.resizable(False, False)

    total_entradas, total_despesas, saldo = calcular_saldo()
    total_movimentacoes, quantidade_entradas, quantidade_despesas = resumo_financeiro()

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
        bg="#ffffff",
        highlightbackground="#e5e5e5",
        highlightthickness=1,
    )

    cartao_saldo.pack(
        side="left",
        padx=10
    )

    cartao_saldo.pack_propagate(False)

    tk.Label(
        cartao_saldo,
        text="Saldo atual",
        font=("Arial", 9, "bold"),
        bg="#ffffff",
        fg="#777777"
    ).pack(
        anchor="w",
        padx=20,
        pady=(20, 4)
    )

    label_saldo = tk.Label(
        cartao_saldo,
        text=formatar_valor(saldo),
        font=("Arial", 24, "bold"),
        bg="#ffffff",
        fg="#222222"
    )
    label_saldo.pack(
        anchor="w",
        padx=20
    )
    tk.Label(
        cartao_saldo,
        text="Disponivel",
        font=("Arial", 9),
        bg="#ffffff",
        fg="#999999"
    ).pack(
        anchor="w",
        padx=20,
        pady=(3, 0)
    )


    cartao_entradas = tk.Frame(
        frame_cartoes,
        width=250,
        height=150,
        bg="#ffffff",
        highlightbackground="#dddddd",
        highlightthickness=1,
    )

    cartao_entradas.pack(
        side="left", 
        padx=10
    )

    cartao_entradas.pack_propagate(False)

    tk.Label(
        cartao_entradas,
        text="Total de entradas",
        font=("Arial", 11),
        bg="#ffffff",
        fg="#666666"
    ).pack(
        anchor="w",
        padx=20,
        pady=(20, 5)
    )

    label_entradas = tk.Label(
        cartao_entradas,
        text=formatar_valor(total_entradas),
        font=("Arial", 24, "bold"),
        bg="#ffffff",
        fg="#198754"
    )
    label_entradas.pack(
        anchor="w",
        padx=20
    )
    label_quantidade_entradas = tk.Label(
        cartao_entradas,
        text=f"{quantidade_entradas} entradas registradas",
        font=("Arial", 9),
        bg="#ffffff",
        fg="#999999"
    )
    label_quantidade_entradas.pack(
        anchor="w",
        padx=20,
        pady=(3, 0)
    )

    cartao_despesas = tk.Frame(
        frame_cartoes,
        width=250,
        height=150,
        bg="#ffffff",
        highlightbackground="#dddddd",
        highlightthickness=1
    )

    cartao_despesas.pack(
        side="left", 
        padx=10
    )

    cartao_despesas.pack_propagate(False)

    tk.Label(
        cartao_despesas,
        text="Total de despesas",
        font=("Arial", 11),
        bg="#ffffff",
        fg="#666666"
    ).pack(
        anchor="w",
        padx=20,
        pady=(20, 5)
    )

    label_despesas = tk.Label(
        cartao_despesas,
        text=formatar_valor(total_despesas),
        font=("Arial", 24, "bold"),
        bg="#ffffff",
        fg="#dc3545"
    )
    label_despesas.pack(
        anchor="w",
        padx=20
    )
    label_quantidade_despesas = tk.Label(
    cartao_despesas,
    text=f"{quantidade_despesas} despesas registradas",
    font=("Arial", 9),
    bg="#ffffff",
    fg="#999999"
    )
    label_quantidade_despesas.pack(
        anchor="w",
        padx=20,
        pady=(3, 0)
    )

    def atualizar_interface():
        total_entradas, total_despesas, saldo = calcular_saldo()

        total_movimentacoes, quantidade_entradas, quantidade_despesas = resumo_financeiro()

        label_saldo.config(
            text=formatar_valor(saldo)
        )

        label_entradas.config(
            text=formatar_valor(total_entradas)
        )

        label_despesas.config(
            text=formatar_valor(total_despesas)
        )

        label_quantidade_entradas.config(
            text=f"{quantidade_entradas} entradas registradas"
        )

        label_quantidade_despesas.config(
            text=f"{quantidade_despesas} despesas registradas"
        )

        carregar_movimentacoes()


    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=30)

    def nova_entrada():
        global janela_cadastro

        if janela_cadastro is not None and janela_cadastro.winfo_exists():
            janela_cadastro.lift()
            janela_cadastro.focus_force()
            return
        
        janela_cadastro = tk.Toplevel(janela)
        janela_cadastro.title("Nova entrada")
        janela_cadastro.geometry("400x300")
        janela_cadastro.resizable(False, False)

        def fechar_cadastro():
            global janela_cadastro

            janela_cadastro.destroy()
            janela_cadastro = None

        janela_cadastro.protocol(
            "WM_DELETE_WINDOW",
            fechar_cadastro
        )

        tk.Label(
            janela_cadastro,
            text="Nova entrada",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        tk.Label(
            janela_cadastro,
            text="Descrição:"
        ).pack()

        campo_descricao = tk.Entry(
            janela_cadastro,
            width=35
        )
        campo_descricao.pack(pady=5)

        tk.Label(
            janela_cadastro,
            text="Valor:"
        ).pack()

        campo_valor = tk.Entry(
            janela_cadastro,
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
            janela_cadastro.destroy()

        botao_cadastrar = tk.Button(
            janela_cadastro,
            text="Cadastrar",
            width=20,
            command=cadastrar
        )
        botao_cadastrar.pack(pady=25)

        janela_cadastro.bind("<Return>", lambda event: cadastrar())

    def nova_despesa():
        global janela_cadastro

        if janela_cadastro is not None and janela_cadastro.winfo_exists():
            janela_cadastro.lift()
            janela_cadastro.focus_force()
            return
        
        janela_cadastro = tk.Toplevel(janela)
        janela_cadastro.title("Nova despesa")
        janela_cadastro.geometry("400x300")
        janela_cadastro.resizable(False, False)

        tk.Label(
            janela_cadastro,
            text="Nova despesa",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        tk.Label(
            janela_cadastro,
            text="Descrição:"
        ).pack()

        campo_descricao = tk.Entry(
            janela_cadastro,
            width=35
        )
        campo_descricao.pack(pady=5)

        tk.Label(
            janela_cadastro,
            text="Valor:"
        ).pack()

        campo_valor = tk.Entry(
            janela_cadastro,
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
            janela_cadastro.destroy()

        botao_cadastrar = tk.Button(
            janela_cadastro,
            text="Cadastrar",
            width=20,
            command=cadastrar
        )
        botao_cadastrar.pack(pady=25)

        janela_cadastro.bind("<Return>", lambda event: cadastrar())


    botao_entrada_frame = tk.Frame(
        frame_botoes,
        bg="#198754",
        padx=1,
        pady=1
    )

    botao_entrada_frame.pack(
        side="left",
        padx=10
    )
        
    tk.Button(
        frame_botoes,
        text="+ Nova entrada",
        font=("Arial", 11, "bold"),
        width=18,
        bg="#ffffff",
        fg="#198754",
        activebackground="#f1f8f4",
        activeforeground="#198754",
        relief="flat",
        highlightbackground="#198754",
        highlightcolor="#198754",
        highlightthickness=1,
        cursor="hand2",
        padx=10,
        pady=5,
        command=nova_entrada
    ).pack(
        side="left", 
        padx=10
    )

    botao_despesa_frame = tk.Frame(
        frame_botoes,
        bg="#dc3545",
        padx=1,
        pady=1
    )

    botao_despesa_frame.pack(
        side="left",
        padx=10
    )

    tk.Button(
        frame_botoes,
        text="+ Nova despesa",
        font=("Arial", 11, "bold"),
        width=18,
        bg="#ffffff",
        fg="#dc3545",
        activebackground="#fdf1f2",
        activeforeground="#dc3545",
        relief="flat",
        borderwidth=0,
        cursor="hand2",
        padx=10,
        pady=5,
        command=nova_despesa
    ).pack(
        side="left", 
        pady=10
    )

    tk.Label(
        janela,
        text="Movimentações",
        font=("Arial", 18, "bold")
    ).pack(pady=(10, 5))


    frame_pesquisa = tk.Frame(
        janela,
        bg="#f4f4f4"
    )

    frame_pesquisa.pack(
        pady=(0, 10)
    )


    campo_busca = tk.Entry(
        frame_pesquisa,
        font=("Arial", 9),
        width=35,
        relief="flat",
        bg="white",
        fg="#999999",
        insertbackground="#333333"
    )

    campo_busca.insert(0, "Buscar descrição...")

    def entrar_busca(event):
        if campo_busca.get() == "Buscar descrição...":
            campo_busca.delete(0, tk.END)
            campo_busca.config(fg="#333333")

    def sair_busca(event):
        if campo_busca.get() == "":
            campo_busca.insert(0, "Buscar descrição...")
            campo_busca.config(fg="#999999")

    campo_busca.bind("<FocusIn>", entrar_busca)
    campo_busca.bind("<FocusOut>", sair_busca)

    campo_busca.pack(
        side="left",
        ipady=6
    )

    def limpar_busca():
        campo_busca.delete(0, tk.END)

        campo_busca.insert(
            0,
            "Buscar descrição..."
        )

        campo_busca.config(
            fg="#999999"
        )

        campo_busca.focus()

        carregar_movimentacoes()

    botao_limpar = tk.Button(
        frame_pesquisa,
        text="Limpar",
        font=("Arial", 9, "bold"),
        bg="#f5f5f5",
        fg="#555555",
        activebackground="#e9e9e9",
        activeforeground="#333333",
        relief="flat",
        borderwidth=0,
        cursor="hand2",
        padx=12,
        pady=5,
        command=limpar_busca
    )

    botao_limpar.pack(
        side="left",
        padx=(8, 0)
    )

    

    def pesquisar(event=None):
        termo = campo_busca.get().strip()

        if termo == "":
            carregar_movimentacoes()
            return

        movimentacoes = buscar_movimentacoes(termo)

        carregar_movimentacoes(movimentacoes)

    campo_busca.bind("<Return>", pesquisar)

    frame_movimentacoes = tk.Frame(
        janela,
        bg="#f4f4f4"
    )

    frame_movimentacoes.pack(
        fill="x",
        padx=20
)


    def carregar_movimentacoes(movimentacoes=None):
        for widget in frame_movimentacoes.winfo_children():
            widget.destroy()

        if movimentacoes is None:
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
                fg="#198754" if tipo == "entrada" else "#dc3545",
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
                font=("Arial", 8, "bold"),
                width=7,
                relief="flat",
                bg="#f5f5f5",
                fg="#555555",
                activebackground="#e9e9e9",
                activeforeground="#333333",
                cursor="hand2",
                borderwidth=1,
                command=lambda id_mov=id_mov,
                                tipo=tipo,
                                descricao=descricao,
                                valor=valor:editar_janela(
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
                font=("Arial", 8, "bold"),
                width=7,
                relief="flat",
                bg="#fff5f5",
                fg="#dc3545",
                activebackground="#fde2e2",
                activeforeground="#b02a37",
                borderwidth=0,
                cursor="hand2",
                command=lambda id_mov=id_mov: excluir(id_mov)
            ).pack(
                side="left",
                padx=2,
                pady=5
            )

    def excluir(id_movimentacao):
        janela_exclusao = tk.Toplevel(janela)

        janela_exclusao.title("Confirmar exclusão?")
        janela_exclusao.geometry("360x200")
        janela_exclusao.resizable(False, False)
        janela_exclusao.configure(bg="white")

        janela_exclusao.transient(janela)
        janela_exclusao.grab_set()

        janela_exclusao.update_idletasks()

        largura = janela_exclusao.winfo_width()
        altura = janela_exclusao.winfo_height()

        pos_x = janela.winfo_x() + (janela.winfo_width() - largura) // 2
        pos_y = janela.winfo_y() + (janela.winfo_height() - altura) // 2

        janela_exclusao.geometry(
            f"{largura}x{altura}+{pos_x}+{pos_y}"
        ) 

        tk.Label(
            janela_exclusao,
            text="Excluir movimentação?",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            pady=(25, 8)
        )

        tk.Label(
            janela_exclusao,
            text="Esta ação não poderá ser desfeita.",
            font=("Arial", 9),
            bg="white",
            fg="#777777"
        ).pack()

        frame_botoes_exclusao = tk.Frame(
            janela_exclusao,
            bg="white"
        )

        frame_botoes_exclusao.pack(
            pady=25
        )

        def confirmar_exclusao():
            excluir_movimentacao(id_movimentacao)
            janela_exclusao.destroy()
            atualizar_interface()

        tk.Button(
            frame_botoes_exclusao,
            text="Cancelar",
            font=("Arial", 9, "bold"),
            bg="#f5f5f5",
            fg="#555555",
            activebackground="#e9e9e9",
            activeforeground="#333333",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=15,
            pady=7,
            command=janela_exclusao.destroy
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            frame_botoes_exclusao,
            text="Excluir",
            font=("Arial", 9, "bold"),
            bg="#fff5f5",
            fg="#dc3545",
            activebackground="#fde2e2",
            activeforeground="#b02a37",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=15,
            pady=7,
            command=confirmar_exclusao
        ).pack(
            side="left",
            padx=5
        )


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

