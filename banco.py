import sqlite3
import os

# Usaremos a pasta /tmp que é onde o Render permite escrita
CAMINHO_BANCO = "/tmp/notas_fiscais.db"

def conectar_banco():
    # Se estivermos rodando no Render, usa /tmp, senão usa local
    caminho = "/tmp/notas_fiscais.db" if os.path.exists("/tmp") else "notas_fiscais.db"
    conexao = sqlite3.connect(caminho)
    conexao.row_factory = sqlite3.Row
    return conexao

def criar_tabela():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            valor REAL NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()