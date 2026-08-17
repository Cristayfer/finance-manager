import sqlite3

def conectar():
    conexao = sqlite3.connect("financeiro.db")
    return conexao


def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL
    )
""")

    conexao.commit()
    conexao.close()


def inserir_movimentacao(tipo, descricao, valor):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO movimentacoes (tipo, descricao, valor)
        VALUES (?, ?, ?)
    """, (tipo, descricao, valor))

    conexao.commit()
    conexao.close()

def listar_movimentacoes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, tipo, descricao, valor
        FROM movimentacoes
    """)

    movimentacoes = cursor.fetchall()

    conexao.close()

    return movimentacoes


def excluir_movimentacao(id_movimentacao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM movimentacoes
        WHERE id = ?
    """, (id_movimentacao,))

    if cursor.rowcount > 0:
        excluida = True
    else:
        excluida = False
    
    conexao.commit()
    conexao.close()

    return excluida

def editar_movimentacao(id_movimentacao, tipo, descricao, valor):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE movimentacoes
        SET tipo = ?, descricao = ?, valor = ?
        WHERE id = ?
    """, (tipo, descricao, valor, id_movimentacao))

    conexao.commit()
    conexao.close()

def calcular_saldo():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            SUM(CASE WHEN tipo = 'entrada' THEN valor ELSE 0 END),
            SUM(CASE WHEN tipo = 'despesa' THEN valor ELSE 0 END)
        FROM movimentacoes
    """)

    resultado = cursor.fetchone()

    conexao.close()

    total_entradas = resultado[0] or 0
    total_despesas = resultado[1] or 0

    saldo = total_entradas - total_despesas

    return total_entradas, total_despesas, saldo

def resumo_financeiro():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT 
            COUNT(*),
            SUM(CASE WHEN tipo = 'entrada' THEN 1 ELSE 0 END),
            SUM(CASE WHEN tipo = 'despesa' THEN 1 ELSE 0 END)
        FROM movimentacoes
    """)

    resultado = cursor.fetchone()

    conexao.close()

    total_movimentacoes = resultado[0]
    quantidade_entradas = resultado[1] or 0
    quantidade_despesas = resultado[2] or 0

    return total_movimentacoes, quantidade_entradas, quantidade_despesas


def buscar_movimentacoes(termo):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, tipo, descricao, valor
        FROM movimentacoes
        WHERE descricao LIKE ?
    """, (f"%{termo}%",))

    movimentacoes = cursor.fetchall()

    conexao.close()

    return movimentacoes