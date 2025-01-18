import sqlite3
from database.db_config import criar_conexao
import pandas as pd

def consultar_dados(filtro=None):
    conn = criar_conexao()
    cursor = conn.cursor()
    query = "SELECT * FROM contagem_diaria"
    if filtro:
        query += f" WHERE {filtro}"
    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def inserir_dados(pelotao, data, pessoa, carros, motos, qnt_ocorrencias, flagrantes, autuacoes,
                  raia, procurado, carro_apreendido, moto_apreendido, flagrantes_outros, arma):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contagem_diaria (
            pelotao, data, pessoa, carros, motos, qnt_ocorrencias, flagrantes, autuacoes, 
            raia, procurado, carro_apreendido, moto_apreendido, flagrantes_outros, arma
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (pelotao, data, pessoa, carros, motos, qnt_ocorrencias, flagrantes, autuacoes,
          raia, procurado, carro_apreendido, moto_apreendido, flagrantes_outros, arma))
    conn.commit()
    conn.close()

def alterar_registro(registro_id, coluna, valor):

    conn = criar_conexao()
    cursor = conn.cursor()

    try:
        # Usando placeholders para evitar SQL Injection
        query = f"UPDATE contagem_diaria SET {coluna} = ? WHERE id = ?"
        cursor.execute(query, (valor, registro_id))
        conn.commit()
        print(f"Registro {registro_id} atualizado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao atualizar registro: {e}")
        raise
    finally:
        conn.close()


def deletar_registro(registro_id):
    """
    Deleta um registro do banco de dados pelo ID.
    """
    conn = criar_conexao()
    cursor = conn.cursor()

    try:
        # Executa a query de deletar
        cursor.execute("DELETE FROM contagem_diaria WHERE id = ?", (registro_id,))
        conn.commit()

        # Retorna True se uma ou mais linhas foram afetadas
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao deletar registro: {e}")
        return False
    finally:
        conn.close()

    print(f"Tentando deletar registro com ID: {registro_id}")
    print(f"Número de registros afetados: {cursor.rowcount}")
def exportar_para_excel(nome_arquivo="contagem_diaria.xlsx"):
    """
    Exporta os dados da tabela `contagem_diaria` para um arquivo Excel.
    """
    conn = criar_conexao()
    query = "SELECT * FROM contagem_diaria"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Salva os dados em um arquivo Excel
    df.to_excel(nome_arquivo, index=False, engine="openpyxl")
    print(f"Dados exportados para o arquivo {nome_arquivo}.")