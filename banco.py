import sqlite3
from datetime import datetime


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


def adicionar_coluna_data():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("PRAGMA table_info(movimentacoes)")
    colunas = cursor.fetchall()

    nomes_colunas = [coluna[1] for coluna in colunas]

    if "data" not in nomes_colunas:
        cursor.execute("""
            ALTER TABLE movimentacoes
            ADD COLUMN data TEXT
        """)

    conexao.commit()
    conexao.close()


def inserir_movimentacao(tipo, descricao, valor):
    conexao = conectar()
    cursor = conexao.cursor()

    data = datetime.now().strftime("%d/%m/%Y")

    cursor.execute("""
        INSERT INTO movimentacoes (tipo, descricao, valor, data)
        VALUES (?, ?, ?, ?)
    """, (tipo, descricao, valor, data))

    conexao.commit()
    conexao.close()

def listar_movimentacoes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, tipo, descricao, valor, data
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

def calcular_saldo_do_dia():
    conexao = conectar()
    cursor = conexao.cursor()

    data_atual = datetime.now().strftime("%d/%m/%Y")

    cursor.execute("""
        SELECT 
            SUM(CASE WHEN tipo = 'entrada' THEN valor ELSE 0 END),
            SUM(CASE WHEN tipo = 'despesa' THEN valor ELSE 0 END)
        FROM movimentacoes
        WHERE data = ?
    """, (data_atual,))

    resultado = cursor.fetchone()

    conexao.close()

    total_entradas = resultado[0] or 0
    total_despesas = resultado[1] or 0

    saldo = total_entradas - total_despesas

    return total_entradas, total_despesas, saldo


def buscar_por_data(data):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, tipo, descricao, valor, data
        FROM movimentacoes
        WHERE data = ? 
    """, (data,))

    movimentacoes = cursor.fetchall()

    conexao.close()

    return movimentacoes

def calcular_saldo_periodo(data_inicial, data_final):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            SUM(CASE WHEN tipo = 'entrada' THEN valor ELSE 0 END),
            SUM(CASE WHEN tipo = 'despesa' THEN valor ELSE 0 END)
        FROM movimentacoes
        WHERE data BETWEEN ? AND ?
    """, (data_inicial, data_final))

    resultado = cursor.fetchone()

    conexao.close()

    total_entradas = resultado[0] or 0
    total_despesas = resultado[1] or 0

    saldo = total_entradas - total_despesas

    return total_entradas, total_despesas, saldo