import pandas as pd

df_preventiva = pd.read_excel('PREVENTIVA.xlsx')
df_carreta = pd.read_excel('CARRETA.xlsx')
df_Esl = pd.read_excel('ESL.xlsx')
df_mobile = pd.read_excel('MOBILE.xlsx')
df_bipe = pd.read_excel('BIPE.xlsx')
df_bipe_de_notas = pd.read_excel("BIPE DE NOTAS.xlsx")

df_merge = pd.merge(df_preventiva, df_carreta[['PEDIDO','NF`s','CHAVE','PREVISÃO ENTREGA']], left_on='PEDIDO 1P/FULL', right_on='PEDIDO', how='left').drop(columns=['PEDIDO'])

df_merge_2 = df_merge.merge(df_mobile[['Pedido','Tipo','Entregador']], left_on='PEDIDO 1P/FULL', right_on='Pedido', how='left').drop(columns=['Pedido'])

df_merge_3 = pd.merge(df_merge_2,df_Esl[[ 'Nota Fiscal/Chave NF-e','Última ocorrência/Observações', 'Pessoa/Nome', 'Última ocorrência/Data ocorrência']], left_on='CHAVE', right_on= 'Nota Fiscal/Chave NF-e', how='left').drop(columns=['Nota Fiscal/Chave NF-e'])

df_merge_4 = pd.merge(df_merge_3, df_bipe[['PEDIDO','INFO']], left_on='PEDIDO 1P/FULL', right_on='PEDIDO', how='left').drop(columns=['PEDIDO'])

df_merge_5 = pd.merge(df_merge_4, df_bipe_de_notas[['NF', 'OCORRENCIA ']], left_on='NF`s', right_on='NF', how='left').drop(columns=['NF'])

df_merge_5.to_excel('29-12-2025.xlsx', sheet_name='Relatorio_diario', index=False)
