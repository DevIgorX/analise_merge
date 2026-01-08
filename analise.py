import pandas as pd
from datetime import datetime
import os

caminho_script = os.path.abspath('__file__')
diretorio_raiz = os.path.dirname(caminho_script)
caminho_dados = os.path.join(diretorio_raiz, 'dados')



for arquivo in os.listdir(caminho_dados):
    caminho_arquivo = os.path.join(caminho_dados, arquivo)

    if 'Preventiva' in arquivo:
        df_preventiva = pd.read_excel(caminho_arquivo)
    elif 'CARRETA' in arquivo:
        df_carreta = pd.read_excel(caminho_arquivo)
    elif 'magazine' in arquivo:
        df_esl = pd.read_excel(caminho_arquivo)
    elif 'Mobile' in arquivo:
        df_mobile = pd.read_excel(caminho_arquivo)
    elif 'Bipe_Produtos' in arquivo:
        df_bipe = pd.read_excel(caminho_arquivo)
    elif 'Bipe_de_notas' in arquivo:
        df_bipe_notas = pd.read_excel(caminho_arquivo, sheet_name='Plan1')
        


dfs = [
    df_preventiva, df_carreta, df_esl,
    df_mobile, df_bipe, df_bipe_notas
]

for df in dfs:
    df.columns = df.columns.str.strip()

df_final = (
    df_preventiva
        .merge(
            df_carreta[['PEDIDO', 'NF`s', 'CHAVE', 'PREVISÃO ENTREGA', 'TIPO']],
            left_on='PEDIDO 1P/FULL',
            right_on='PEDIDO',
            how='left'
        )
        .drop(columns=['PEDIDO'])

        .merge(
            df_mobile[['Pedido', 'Tipo', 'Entregador']],
            left_on='PEDIDO 1P/FULL',
            right_on='Pedido',
            how='left'
        )
        .drop(columns=['Pedido'])

        .merge(
            df_esl[
                ['Nota Fiscal/Chave NF-e',
                 'Última ocorrência/Observações',
                 'Pessoa/Nome',
                 'Última ocorrência/Data ocorrência']
            ],
            left_on='CHAVE',
            right_on='Nota Fiscal/Chave NF-e',
            how='left'
        )
        .drop(columns=['Nota Fiscal/Chave NF-e'])

        .merge(
            df_bipe[['PEDIDO_BIPE', 'BIPE_PRODUTO']],
            left_on='PEDIDO 1P/FULL',
            right_on='PEDIDO_BIPE',
            how='left'
        )
        .drop(columns=['PEDIDO_BIPE'])

        .merge(
            df_bipe_notas[['NF', 'BIPE_DE_NOTAS']],
            left_on='NF`s',
            right_on='NF',
            how='left'
        )
        .drop(columns=['NF'])
)

df_final_2 = (pd.merge(df_carreta,df_esl[['Nota Fiscal/Chave NF-e', 'Ocorrência/Ocorrência']], left_on='CHAVE', right_on='Nota Fiscal/Chave NF-e', how='left')
              .drop(columns=['Nota Fiscal/Chave NF-e']))


df_final['Última ocorrência/Observações'] = df_final['Última ocorrência/Observações'].fillna('Não informado')


df_final_3 = pd.merge(df_final, df_final_2[['CHAVE', 'Ocorrência/Ocorrência']], left_on='CHAVE', right_on='CHAVE', how='left').drop(columns=['CHAVE'])


filtro = df_final_3['Última ocorrência/Observações'] == 'Não informado'

df_final_3.loc[filtro, 'Última ocorrência/Observações'] = df_final_3.loc[filtro, 'Ocorrência/Ocorrência']

colunas_datas = [
    'PREVISÃO ENTREGA',
    'Última ocorrência/Data ocorrência'
]

for col in colunas_datas:
    df_final_3[col] = pd.to_datetime(df_final_3[col], errors='coerce')


data_hoje = datetime.today().strftime('%d-%m-%Y')
nome_arquivo = f'{data_hoje}.xlsx'

with pd.ExcelWriter(
    nome_arquivo,
    engine='xlsxwriter',
    datetime_format='dd/mm/yyyy'
) as writer:
    
    df_final.to_excel(
        writer,
        sheet_name='Relatorio_diario',
        index=False
    )

