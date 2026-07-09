import sqlite3

# 1. Função para abrir a conexão com o arquivo do banco
def conectar_banco():
    conexao = sqlite3.connect("notas_fiscais.db")
    conexao.row_factory = sqlite3.Row # Retorna os dados em um formato de dicionário fácil de ler
    return conexao

# 2. Função para criar a nossa tabela na primeira vez que rodarmos
def criar_tabela():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # O comando SQL para criar a "planilha" do banco de dados
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