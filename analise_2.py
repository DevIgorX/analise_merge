import pandas as pd
import os
diretorio_atual = os.path.abspath(__file__)
diretorio_raiz = os.path.dirname(diretorio_atual)
caminho_dados = os.path.join(diretorio_raiz, 'dados')

for arquivo in os.listdir(caminho_dados):
    caminho_arquivo = os.path.join(caminho_dados, arquivo)
    if 'CARRETA' in arquivo:
        df_carreta = pd.read_excel(caminho_arquivo)
        df_carreta.columns = df_carreta.columns.str.strip().upper()
        df_carreta = df_carreta.add_prefix('CARRETA_')
    elif 'magazine' in arquivo:
        df_esl = pd.read_excel(caminho_arquivo)
        df_esl.columns = df_esl.columns.str.strip().upper()
        df_esl = df_esl.add_prefix('ESL_')
    elif 'Mobile' in arquivo:
        df_mobile = pd.read_excel(caminho_arquivo)
        df_mobile.columns = df_mobile.str.strip().upper()
        df_mobile = df_mobile.add_prefix('MOBILE_')
    elif 'Bipe_Produtos' in arquivo:
        df_bipe = pd.read_excel(caminho_arquivo)
        df_bipe.columns = df_bipe.columns.str.strip().upper()
        df_bipe = df_bipe.add_prefix('Bipe_PROD')
    elif 'Bipe_de_notas' in arquivo:
        df_bipe_notas = pd.read_excel(caminho_arquivo, sheet_name='Plan1')
        df_bipe_notas.columns = df_bipe_notas.columns.str.strip().upper()
        df_bipe_notas = df_bipe_notas.add_prefix('Bipe_notas_')

        


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
                 .merge(df_bipe[['PEDIDOS', 'STATUS_DEPOSITO']], left_on='PEDIDO', right_on='PEDIDOS', how='left').drop(columns=['PEDIDOS'])
                 )

df_final_2 = pd.merge(df_final, df_esl[['Nota Fiscal/Chave NF-e','Ocorrência/Ocorrência']], left_on='CHAVE', right_on='Nota Fiscal/Chave NF-e', how='left').drop(columns=['Nota Fiscal/Chave NF-e'])

df_final_2['Última ocorrência/Observações'] = df_final_2['Última ocorrência/Observações'].fillna('Não informado')

filtro = df_final_2['Última ocorrência/Observações'] == 'Não informado'

df_final_2.loc[filtro, 'Última ocorrência/Observações'] = df_final_2.loc[filtro, 'Ocorrência/Ocorrência']

df_final_2 = df_final_2.drop(columns=['Ocorrência/Ocorrência'])

df_final_2.to_excel('Relatorio.xlsx', sheet_name='Relatorio_final', index=False)
