import pandas as pd
from datetime import datetime
import os

caminho_script = os.path.abspath(__file__)
diretorio_raiz = os.path.dirname(caminho_script)
caminho_dados = os.path.join(diretorio_raiz, 'dados')



for arquivo in os.listdir(caminho_dados):
    caminho_arquivo = os.path.join(caminho_dados, arquivo)

    if 'Preventiva' in arquivo:
        df_preventiva = pd.read_excel(caminho_arquivo)
        df_preventiva.columns = df_preventiva.columns.str.strip().str.upper()
        df_preventiva = df_preventiva.add_prefix('PREVENTIVA_')
    elif 'CARRETA' in arquivo:
        df_carreta = pd.read_excel(caminho_arquivo)
        df_carreta.columns = df_carreta.columns.str.strip().str.upper()
        df_carreta = df_carreta.add_prefix('CARRETA_')
    elif 'magazine' in arquivo:
        df_esl = pd.read_excel(caminho_arquivo)
        df_esl.columns = df_esl.columns.str.strip().str.upper()
        df_esl = df_esl.add_prefix('ESL_')
    elif 'Mobile' in arquivo:
        df_mobile = pd.read_excel(caminho_arquivo)
        df_mobile.columns = df_mobile.columns.str.strip().str.upper()
        df_mobile = df_mobile.add_prefix('MOBILE_')
    elif 'Bipe_Produtos' in arquivo:
        df_bipe = pd.read_excel(caminho_arquivo)
        df_bipe.columns = df_bipe.columns.str.strip().str.upper()
        df_bipe = df_bipe.add_prefix('BIPE_PROD_')
    elif 'Bipe_de_notas' in arquivo:
        df_bipe_notas = pd.read_excel(caminho_arquivo, sheet_name='Plan1')
        df_bipe_notas.columns = df_bipe_notas.columns.str.strip().str.upper()
        df_bipe_notas = df_bipe_notas.add_prefix('BIPE_NOTAS_')
        


df_final = (
    df_preventiva
        .merge(
            df_carreta[['CARRETA_PEDIDO', 'CARRETA_NF`S', 'CARRETA_CHAVE', 'CARRETA_DATA ENTRADA', 'CARRETA_TIPO_FLUXO']],
            left_on='PREVENTIVA_PEDIDO 1P/FULL',  right_on='CARRETA_PEDIDO',
            how='left'
        )
        .drop(columns=['CARRETA_PEDIDO'])

        .merge(
            df_mobile[['MOBILE_PEDIDO', 'MOBILE_TIPO', 'MOBILE_ENTREGADOR']],
            left_on='PREVENTIVA_PEDIDO 1P/FULL',
            right_on='MOBILE_PEDIDO',
            how='left'
        )
        .drop(columns=['MOBILE_PEDIDO'])

        .merge(
            df_esl[[
                'ESL_NOTA FISCAL/CHAVE NF-E',
                'ESL_ÚLTIMA OCORRÊNCIA/OBSERVAÇÕES',
                'ESL_PESSOA/NOME',
                'ESL_ÚLTIMA OCORRÊNCIA/DATA OCORRÊNCIA'
            ]],
            left_on='CARRETA_CHAVE',
            right_on='ESL_NOTA FISCAL/CHAVE NF-E',
            how='left'
        )
        .drop(columns=['ESL_NOTA FISCAL/CHAVE NF-E'])

        .merge(
            df_bipe[['BIPE_PROD_PEDIDO', 'BIPE_PROD_STATUS']],
            left_on='PREVENTIVA_PEDIDO 1P/FULL',
            right_on='BIPE_PROD_PEDIDO',
            how='left'
        )
        .drop(columns=['BIPE_PROD_PEDIDO'])

        .merge(
            df_bipe_notas[['BIPE_NOTAS_NF', 'BIPE_NOTAS_OCORRENCIA']],
            left_on='CARRETA_NF`S', 
            right_on='BIPE_NOTAS_NF',
            how='left'
        )
        .drop(columns=['BIPE_NOTAS_NF'])
)


df_final_2 = (
    pd.merge(
        df_carreta,
        df_esl[['ESL_NOTA FISCAL/CHAVE NF-E', 'ESL_OCORRÊNCIA/OCORRÊNCIA']], 
        left_on='CARRETA_CHAVE', 
        right_on='ESL_NOTA FISCAL/CHAVE NF-E', 
        how='left'
    )
    .drop(columns=['ESL_NOTA FISCAL/CHAVE NF-E'])
)


coluna_obs = 'ESL_ÚLTIMA OCORRÊNCIA/OBSERVAÇÕES'
coluna_ocorrencia = 'ESL_OCORRÊNCIA/OCORRÊNCIA'

df_final[coluna_obs] = df_final[coluna_obs].fillna('Não informado')


df_final_3 = pd.merge(
    df_final, 
    df_final_2[['CARRETA_CHAVE', coluna_ocorrencia]], 
    left_on='CARRETA_CHAVE', 
    right_on='CARRETA_CHAVE', 
    how='left'
).drop(columns=['CARRETA_CHAVE']) 


filtro = df_final_3[coluna_obs] == 'Não informado'
df_final_3.loc[filtro, coluna_obs] = df_final_3.loc[filtro, coluna_ocorrencia]

df_final_3 = df_final_3.drop(columns=['ESL_OCORRÊNCIA/OCORRÊNCIA'])


colunas_datas = [
    'CARRETA_DATA ENTRADA',
    'ESL_ÚLTIMA OCORRÊNCIA/DATA OCORRÊNCIA'
]

for col in colunas_datas:
    
    if col in df_final_3.columns:
        df_final_3[col] = pd.to_datetime(df_final_3[col], errors='coerce')


data_hoje = datetime.today().strftime('%d-%m-%Y')
nome_arquivo = f'{data_hoje}.xlsx'

with pd.ExcelWriter(
    nome_arquivo,
    engine='xlsxwriter',
    datetime_format='dd/mm/yyyy'
) as writer:
    
    df_final_3.to_excel( 
        writer,
        sheet_name='Relatorio_diario',
        index=False
    )