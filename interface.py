import tkinter as tk
from banco import calcular_saldo, inserir_movimentacao, listar_movimentacoes

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

    # =========================
    # CABEÇALHO
    # =========================

    cabecalho = tk.Frame(
        frame_movimentacoes
    )
    cabecalho.pack()

    tk.Label(
        cabecalho,
        text="DATA",
        font=("Arial", 10, "bold"),
        width=12
    ).grid(row=0, column=0, padx=5, pady=5)

    tk.Label(
        cabecalho,
        text="TIPO",
        font=("Arial", 10, "bold"),
        width=12
    ).grid(row=0, column=1, padx=5, pady=5)

    tk.Label(
        cabecalho,
        text="DESCRIÇÃO",
        font=("Arial", 10, "bold"),
        width=25
    ).grid(row=0, column=2, padx=5, pady=5)

    tk.Label(
        cabecalho,
        text="VALOR",
        font=("Arial", 10, "bold"),
        width=15
    ).grid(row=0, column=3, padx=5, pady=5)


    # =========================
    # MOVIMENTAÇÕES
    # =========================

    for movimentacao in movimentacoes:

        id_mov, tipo, descricao, valor, data = movimentacao

        linha = tk.Frame(
            frame_movimentacoes,
            relief="solid",
            borderwidth=1
        )

        linha.pack(pady=2)

        tk.Label(
            linha,
            text=data,
            width=12
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Label(
            linha,
            text=tipo.capitalize(),
            width=12
        ).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            linha,
            text=descricao,
            width=25,
            anchor="w"
        ).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(
            linha,
            text=formatar_valor(valor),
            width=15
        ).grid(row=0, column=3, padx=5, pady=5)

carregar_movimentacoes()

    
janela.mainloop()

