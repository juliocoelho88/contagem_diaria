import sqlite3

DB_FILE = "contagem_diaria.db"

def criar_conexao():
    return sqlite3.connect(DB_FILE)

def criar_tabela():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contagem_diaria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pelotao TEXT NOT NULL,
            data TEXT NOT NULL,
            pessoa INTEGER NOT NULL,
            carros INTEGER NOT NULL,
            motos INTEGER NOT NULL,
            qnt_ocorrencias INTEGER NOT NULL,
            flagrantes INTEGER NOT NULL,
            autuacoes INTEGER NOT NULL,
            raia INTEGER NOT NULL,
            procurado INTEGER NOT NULL,
            carro_apreendido INTEGER NOT NULL,
            moto_apreendido INTEGER NOT NULL,
            flagrantes_outros INTEGER NOT NULL,
            arma INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()
