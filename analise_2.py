import pandas as pd
import os
diretorio_atual = os.path.abspath('__file__')
diretorio_raiz = os.path.dirname(diretorio_atual)
caminho_dados = os.path.join(diretorio_raiz, 'dados')

for arquivo in os.listdir(caminho_dados):
    caminho_arquivo = os.path.join(caminho_dados, arquivo)
    if 'CARRETA' in arquivo:
        df_carreta = pd.read_excel(caminho_arquivo)
    elif 'magazine' in arquivo:
        df_esl = pd.read_excel(caminho_arquivo)
    elif 'Mobile' in arquivo:
        df_mobile = pd.read_excel(caminho_arquivo)
    elif 'Bipe_Produtos' in arquivo:
        df_bipe = pd.read_excel(caminho_arquivo)
    elif 'Bipe_de_notas' in arquivo:
        df_bipe_notas = pd.read_excel(caminho_arquivo, sheet_name='Plan1')


dfs = [df_carreta, df_esl, df_mobile, df_bipe, df_bipe_notas ]

df_carreta[['PEDIDO', 'NF`s','CHAVE', 'DATA ENTRADA', 'TIPO_FLUXO' ]]

df_carreta = df_carreta[['PEDIDO', 'NF`s','CHAVE', 'DATA ENTRADA', 'TIPO_FLUXO' ]]

df_final = (pd.merge(df_carreta, df_esl[['Nota Fiscal/Chave NF-e',
                 'Última ocorrência/Observações',
                 'Pessoa/Nome',
                 'Última ocorrência/Data ocorrência']], left_on='CHAVE', 
                 right_on='Nota Fiscal/Chave NF-e', how='left').drop(columns=['Nota Fiscal/Chave NF-e'])
                 .merge(df_mobile[['Pedido', 'Tipo', 'Entregador']], left_on='PEDIDO', right_on='Pedido', how='left').drop(columns=['Pedido'])
                 .merge(df_bipe_notas[['NF', 'BIPE_NOTAS']], left_on='NF`s', right_on='NF', how='left').drop(columns=['NF'])
                 .merge(df_bipe[['PEDIDO_BIPE', 'BIPE_PRODUTO']], left_on='PEDIDO', right_on='PEDIDO_BIPE', how='left').drop(columns=['PEDIDO_BIPE'])
                 )

df_final_2 = pd.merge(df_final, df_esl[['Nota Fiscal/Chave NF-e','Ocorrência/Ocorrência']], left_on='CHAVE', right_on='Nota Fiscal/Chave NF-e', how='left').drop(columns=['Nota Fiscal/Chave NF-e'])

df_final_2['Última ocorrência/Observações'] = df_final_2['Última ocorrência/Observações'].fillna('Não informado')

filtro = df_final_2['Última ocorrência/Observações'] == 'Não informado'

df_final_2.loc[filtro, 'Última ocorrência/Observações'] = df_final_2.loc[filtro, 'Ocorrência/Ocorrência']

df_final_2 = df_final_2.drop(columns=['Ocorrência/Ocorrência'])

df_final_2.to_excel('Relatorio.xlsx', sheet_name='Relatorio_final', index=False)
