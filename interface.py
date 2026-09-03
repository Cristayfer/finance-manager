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

    cor_saldo = (
        "#198754"
        if saldo > 0
        else "#dc3545"
        if saldo < 0
        else "#777777"
    )

    barra_saldo = tk.Frame(
    cartao_saldo,
    bg=cor_saldo,
    width=5
    )

    barra_saldo.place(
    x=0,
    y=0,
    relheight=1,
    width=5
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


        cor_saldo = (
        "#198754"
        if saldo > 0
        else "#dc3545"
        if saldo < 0
        else "#777777"
        )

        label_saldo.config(
        text=formatar_valor(saldo),
        fg="#222222"
        )

        barra_saldo.config(
        bg=cor_saldo
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

    def centralizar_janela(janela_secundaria):
        janela_secundaria.update_idletasks()

        largura = janela_secundaria.winfo_width()
        altura = janela_secundaria.winfo_height()

        pos_x = janela.winfo_x() + (
        janela.winfo_width() - largura
        ) // 2

        pos_y = janela.winfo_y() + (
        janela.winfo_height() - altura
        ) // 2

        janela_secundaria.geometry(
        f"{largura}x{altura}+{pos_x}+{pos_y}"
        )

    def nova_entrada():
        global janela_cadastro

        if janela_cadastro is not None and janela_cadastro.winfo_exists():
            janela_cadastro.lift()
            janela_cadastro.focus_force()
            return
        
        janela_cadastro = tk.Toplevel(janela)
        janela_cadastro.title("Nova entrada")
        janela_cadastro.geometry("426x400")
        janela_cadastro.resizable(False, False)
        janela_cadastro.configure(bg="#f4f4f4")

        janela_cadastro.transient(janela)
        janela_cadastro.grab_set()

        centralizar_janela(janela_cadastro)

        def fechar_cadastro():
            global janela_cadastro

            janela_cadastro.destroy()
            janela_cadastro = None

        janela_cadastro.protocol(
            "WM_DELETE_WINDOW",
            fechar_cadastro
        )

        frame_cabecalho = tk.Frame(
            janela_cadastro,
            bg="#f4f4f4"
        )

        frame_cabecalho.pack(
            fill="x",
            padx=30,
            pady=(25, 15)
        )

        tk.Label(
            frame_cabecalho,
            text="Nova entrada",
            font=("Arial", 18, "bold"),
            bg="#f4f4f4",
            fg="#222222"
        ).pack(
            anchor="w"
        )

        tk.Label(
            frame_cabecalho,
            text="Adicione uma nova movimentação",
            font=("Arial", 9),
            bg="#f4f4f4",
            fg="#777777"
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        frame_descricao = tk.Frame(
            janela_cadastro,
            bg="#f4f4f4"
        )

        frame_descricao.pack(
            fill="x",
            padx=30,
            pady=5
        )

        tk.Label(
            frame_descricao,
            text="DESCRIÇÃO",
            font=("Arial", 9, "bold"),
            bg="#f4f4f4",
            fg="#555555"
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        campo_descricao = tk.Entry(
            frame_descricao,
            font=("Arial", 10),
            relief="flat",
            bg="white",
            fg="#333333",
            insertbackground="#333333"
        )

        campo_descricao.pack(
            fill="x",
            ipady=8
        )

        frame_valor = tk.Frame(
            janela_cadastro,
            bg="#f4f4f4"
        )

        frame_valor.pack(
            fill="x",
            padx=30,
            pady=10
        )

        tk.Label(
            frame_valor,
            text="VALOR",
            font=("Arial", 9, "bold"),
            bg="#f4f4f4",
            fg="#555555"
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        campo_valor = tk.Entry(
            frame_valor,
            font=("Arial", 10),
            relief="flat",
            bg="white",
            fg="#333333",
            insertbackground="#333333"
        )

        campo_valor.pack(
            fill="x",
            ipady=8
        )

        def cadastrar():
            descricao = campo_descricao.get().strip()
            valor = campo_valor.get().strip()

            if descricao == "":
                messagebox.showwarning(
                    "Campo obrigatório",
                    "Informe uma descrição para a entrada.",
                    parent=janela_cadastro
                )
                campo_descricao.focus()
                return

            if valor == "":
                messagebox.showwarning(
                    "Campo obrigatório",
                    "Informe um valor para a entrada.",
                    parent=janela_cadastro
                )
                campo_valor.focus()
                return

            valor = valor.replace(",", ".")

            try:
                valor = float(valor)
            except ValueError:
                messagebox.showwarning(
                    "Valor inválido",
                    "Informe um valor válido.\nExemplo: 50 ou 50,50.",
                    parent=janela_cadastro
                )
                campo_valor.focus()
                return

            if valor <= 0:
                messagebox.showwarning(
                    "Valor inválido",
                    "O valor deve ser maior que zero.",
                    parent=janela_cadastro
                )
                campo_valor.focus()
                return

            inserir_movimentacao(
                "entrada",
                descricao,
                valor
            )

            atualizar_interface()
            fechar_cadastro()


        frame_botoes_cadastro = tk.Frame(
            janela_cadastro,
            bg="#f4f4f4"
        )

        frame_botoes_cadastro.pack(
            pady=(15, 20)
        )

        botao_cadastrar = tk.Button(
            frame_botoes_cadastro,
            text="Cadastrar",
            font=("Arial", 9, "bold"),
            bg="#e8f5ee",
            fg="#198754",
            activebackground="#d8f0e2",
            activeforeground="#146c43",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=20,
            pady=8,
            command=cadastrar
        )
        botao_cadastrar.pack(
            side="left",
            pady=(15, 20)
        )

        botao_cancelar = tk.Button(
        frame_botoes_cadastro,
        text="Cancelar",
        font=("Arial", 9, "bold"),
        bg="#f5f5f5",
        fg="#555555",
        activebackground="#e9e9e9",
        activeforeground="#333333",
        relief="flat",
        borderwidth=0,
        cursor="hand2",
        padx=20,
        pady=8,
        command=fechar_cadastro
        )

        botao_cancelar.pack(
        side="right",
        padx=5
        )

        janela_cadastro.bind("<Return>", lambda event: cadastrar())

    def nova_despesa():
        global janela_cadastro

        if janela_cadastro is not None and janela_cadastro.winfo_exists():
            janela_cadastro.lift()
            janela_cadastro.focus_force()
            return
        
        janela_cadastro = tk.Toplevel(janela)
        janela_cadastro.title("Nova despesa")
        janela_cadastro.geometry("420x400")
        janela_cadastro.resizable(False, False)
        janela_cadastro.configure(bg="#f4f4f4")

        janela_cadastro.transient(janela)
        janela_cadastro.grab_set()

        centralizar_janela(janela_cadastro)

        def fechar_cadastro():
            global janela_cadastro

            janela_cadastro.destroy()
            janela_cadastro = None

        frame_cabecalho = tk.Frame(
            janela_cadastro,
            bg="#f4f4f4"
        )

        frame_cabecalho.pack(
            fill="x",
            padx=30,
            pady=(25, 15)
        )

        tk.Label(
            frame_cabecalho,
            text="Nova despesa",
            font=("Arial", 18, "bold"),
            bg="#f4f4f4",
            fg="#222222"
        ).pack(
            anchor="w"
        )

        tk.Label(
            frame_cabecalho,
            text="Adicione uma nova movimentação",
            font=("Arial", 9),
            bg="#f4f4f4",
            fg="#777777"
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        frame_descricao = tk.Frame(
            janela_cadastro,
            bg="#f4f4f4"
        )

        frame_descricao.pack(
            fill="x",
            padx=30,
            pady=5
        )

        tk.Label(
            frame_descricao,
            text="DESCRIÇÃO",
            font=("Arial", 9, "bold"),
            bg="#f4f4f4",
            fg="#555555"
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        campo_descricao = tk.Entry(
            frame_descricao,
            font=("Arial", 10),
            relief="flat",
            bg="white",
            fg="#333333",
            insertbackground="#333333"
        )

        campo_descricao.pack(
            fill="x",
            ipady=8
        )

        frame_valor = tk.Frame(
            janela_cadastro,
            bg="#f4f4f4"
        )

        frame_valor.pack(
            fill="x",
            padx=30,
            pady=10
        )

        tk.Label(
            frame_valor,
            text="VALOR",
            font=("Arial", 9, "bold"),
            bg="#f4f4f4",
            fg="#555555"
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        campo_valor = tk.Entry(
            frame_valor,
            font=("Arial", 10),
            relief="flat",
            bg="white",
            fg="#333333",
            insertbackground="#333333"
        )

        campo_valor.pack(
            fill="x",
            ipady=8
        )

        def cadastrar():
            descricao = campo_descricao.get().strip()
            valor = campo_valor.get().strip()

            if descricao == "":
                messagebox.showwarning(
                    "Campo obrigatório",
                    "Informe uma descrição para a despesa.",
                    parent=janela_cadastro
                )
                campo_descricao.focus()
                return

            if valor == "":
                messagebox.showwarning(
                    "Campo obrigatório",
                    "Informe um valor para a despesa.",
                    parent=janela_cadastro
                )
                campo_valor.focus()
                return

            valor = valor.replace(",", ".")

            try:
                valor = float(valor)
            except ValueError:
                messagebox.showwarning(
                    "Valor inválido",
                    "Informe um valor válido.\nExemplo: 50 ou 50,50.",
                    parent=janela_cadastro
                )
                campo_valor.focus()
                return

            if valor <= 0:
                messagebox.showwarning(
                    "Valor inválido",
                    "O valor deve ser maior que zero.",
                    parent=janela_cadastro
                )
                campo_valor.focus()
                return

            inserir_movimentacao(
                "despesa",
                descricao,
                valor
            )

            atualizar_interface()
            fechar_cadastro()


        frame_botoes_cadastro = tk.Frame(
            janela_cadastro,
            bg="#f4f4f4"
        )

        frame_botoes_cadastro.pack(
            pady=(15, 20)
        )    
        
        botao_cadastrar = tk.Button(
        frame_botoes_cadastro,
        text="Cadastrar",
        font=("Arial", 9, "bold"),
        bg="#fdecec",
        fg="#dc3545",
        activebackground="#f9dada",
        activeforeground="#b02a37",
        relief="flat",
        borderwidth=0,
        cursor="hand2",
        padx=20,
        pady=8,
        command=cadastrar
        )

        botao_cadastrar.pack(
            side="left",
            padx=5
        )
        botao_cancelar = tk.Button(
            frame_botoes_cadastro,
            text="Cancelar",
            font=("Arial", 9, "bold"),
            bg="#f5f5f5",
            fg="#555555",
            activebackground="#e9e9e9",
            activeforeground="#333333",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=20,
            pady=8,
            command=fechar_cadastro
        )
        botao_cancelar.pack(
            side="left",
            padx=5
        )
        

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
        janela_edicao.geometry("420x400")
        janela_edicao.resizable(False, False)
        janela_edicao.configure(bg="#f4f4f4")

        janela_edicao.transient(janela),
        janela_edicao.grab_set()

        centralizar_janela(janela_edicao)

        frame_cabecalho = tk.Frame(
        janela_edicao,
        bg="#f4f4f4"
        )

        frame_cabecalho.pack(
        fill="x",
        padx=30,
        pady=(25, 15)
        )

        tk.Label(
        frame_cabecalho,
        text="Editar movimentação",
        font=("Arial", 18, "bold"),
        bg="#f4f4f4",
        fg="#222222"
        ).pack(
        anchor="w"
        )

        tk.Label(
        frame_cabecalho,
        text="Altere os dados da movimentação",
        font=("Arial", 9),
        bg="#f4f4f4",
        fg="#777777"
        ).pack(
        anchor="w",
        pady=(3, 0)
        )

        frame_descricao = tk.Frame(
        janela_edicao,
        bg="#f4f4f4"
        )

        frame_descricao.pack(
        fill="x",
        padx=30,
        pady=5
        )

        tk.Label(
        frame_descricao,
        text="DESCRIÇÃO",
        font=("Arial", 9, "bold"),
        bg="#f4f4f4",
        fg="#555555"
        ).pack(
        anchor="w",
        pady=(0, 5)
        )

        campo_descricao = tk.Entry(
        frame_descricao,
        font=("Arial", 10),
        relief="flat",
        bg="white",
        fg="#333333",
        insertbackground="#333333"
        )

        campo_descricao.pack(
            fill="x",
            ipady=8
        )

        campo_descricao.insert(
            0,
            descricao
        )

        frame_valor = tk.Frame(
        janela_edicao,
        bg="#f4f4f4"
        )

        frame_valor.pack(
            fill="x",
            padx=30,
            pady=10
        )

        tk.Label(
            frame_valor,
            text="VALOR",
            font=("Arial", 9, "bold"),
            bg="#f4f4f4",
            fg="#555555"
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        campo_valor = tk.Entry(
            frame_valor,
            font=("Arial", 10),
            relief="flat",
            bg="white",
            fg="#333333",
            insertbackground="#333333"
        )

        campo_valor.pack(
            fill="x",
            ipady=8
        )

        campo_valor.insert(
            0,
            str(valor).replace(".", ",")
        )

        def salvar():

            nova_descricao = campo_descricao.get().strip()
            novo_valor = campo_valor.get().strip()

            if nova_descricao == "":
                messagebox.showwarning(
                    "Campo obrigatório",
                    "Informe uma descrição.",
                    parent=janela_edicao
                )
                campo_descricao.focus()
                return

            if novo_valor == "":
                messagebox.showwarning(
                    "Campo obrigatório",
                    "Informe um valor.",
                    parent=janela_edicao
                )
                campo_valor.focus()
                return

            novo_valor = novo_valor.replace(",", ".")

            try:
                novo_valor = float(novo_valor)

            except ValueError:
                messagebox.showwarning(
                    "Valor inválido",
                    "Informe um valor válido.\nExemplo: 50 ou 50,50.",
                    parent=janela_edicao
                )
                campo_valor.focus()
                return

            if novo_valor <= 0:
                messagebox.showwarning(
                    "Valor inválido",
                    "O valor deve ser maior que zero.",
                    parent=janela_edicao
                )
                campo_valor.focus()
                return

            editar_movimentacao(
                id_mov,
                tipo,
                nova_descricao,
                novo_valor
            )

            janela_edicao.destroy()

            atualizar_interface()

        frame_botoes_edicao = tk.Frame(
        janela_edicao,
        bg="#f4f4f4"
        )

        frame_botoes_edicao.pack(
        pady=(15, 20)
        )

        botao_salvar = tk.Button(
        frame_botoes_edicao,
        text="Salvar alterações",
        font=("Arial", 9, "bold"),
        bg="#e8f5ee",
        fg="#198754",
        activebackground="#d8f0e2",
        activeforeground="#146c43",
        relief="flat",
        borderwidth=0,
        cursor="hand2",
        padx=20,
        pady=8,
        command=salvar
        )

        botao_cancelar = tk.Button(
        frame_botoes_edicao,
        text="Cancelar",
        font=("Arial", 9, "bold"),
        bg="#f5f5f5",
        fg="#555555",
        activebackground="#e9e9e9",
        activeforeground="#333333",
        relief="flat",
        borderwidth=0,
        cursor="hand2",
        padx=20,
        pady=8,
        command=janela_edicao.destroy
        )

        botao_cancelar.pack(
        side="right",
        padx=5
        )

        botao_salvar.pack(
        side="left",
        padx=5
        )

        janela_edicao.bind(
            "<Return>",
            lambda event: salvar()
        )

    carregar_movimentacoes()

    
    janela.mainloop()

