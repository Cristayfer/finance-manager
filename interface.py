import tkinter as tk
from banco import calcular_saldo

janela = tk.Tk()

janela.title("Controle financeiro")
janela.geometry("900x600")
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

tk.Label(
    cartao_saldo,
    text=formatar_valor(saldo),
    font=("Arial", 22, "bold")
).pack()


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

tk.Label(
    cartao_entradas,
    text=formatar_valor(total_entradas),
    font=("Arial", 22, "bold")
).pack()


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

tk.Label(
    cartao_despesas,
    text=formatar_valor(total_despesas),
    font=("Arial", 22, "bold")
).pack()


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
    ).pack(pady=25)

def nova_despesa():
    janela_despesa = tk.Toplevel(janela)
    janela_despesa.title("Nova despesa")
    janela_despesa.geometry("400x300")
    janela_despesa.resizable(False, False)

    tk.Label(
        janela_despesa,
        text="Nova despesa",
        font=("Arial", 20, "bold")
    ).pack(pady=25)

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



janela.mainloop()

