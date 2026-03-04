import sqlite3
import pandas as pd
import os

# Caminho para o banco de dados na raiz do projeto
DB_PATH = 'dados_transporte.db'

def salvar_no_banco(df, nome_tabela="analise_resultado"):
    """Salva o DataFrame no SQLite, sobrescrevendo a tabela anterior."""
    conn = sqlite3.connect(DB_PATH)
    
    df.to_sql(nome_tabela, conn, if_exists='replace', index=False)#cria a tabela 'analise_resultado' automaticamente, se existir apagar e cria novamente com o if_existi
    conn.close()

def buscar_dados_paginados(pagina, itens_por_pagina=10): #o valor 10 é um valor padrão caso vc não passe nada
    """Busca apenas as linhas necessárias para a página atual."""
    conn = sqlite3.connect(DB_PATH)
    offset = (pagina - 1) * itens_por_pagina
    
    # Busca os dados limitados
    query = f"SELECT * FROM analise_resultado LIMIT {itens_por_pagina} OFFSET {offset}"
    df = pd.read_sql(query, conn) #executa uma query e transforma o resultado em um dataframe
    
    # Busca o total de registros para o cálculo de páginas no HTML
    total_registros = conn.execute("SELECT COUNT(*) FROM analise_resultado").fetchone()[0]
    conn.close()
    
    return df.to_dict(orient='records'), total_registros