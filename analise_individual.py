import pandas as pd
import os
from utils import formatar_colunas


diretorio_atual = os.path.abspath(__file__)
diretorio_raiz = os.path.dirname(diretorio_atual)

caminho_dados = os.path.join(diretorio_raiz, 'dados')

for arquivo in os.listdir(caminho_dados):
    caminho_arquivo = os.path.join(caminho_dados, arquivo)
    if 'lista' in arquivo:
        df_lista = pd.read_excel(caminho_arquivo)
        df_lista = formatar_colunas(df_lista)
        df_lista = df_lista.add_prefix('lista_')
    elif 'magazine' in arquivo:
        df_esl = pd.read_excel(caminho_arquivo)
        df_esl = formatar_colunas(df_esl)
        df_esl = df_esl.add_prefix('Esl_')
    elif 'Mobile' in arquivo:
        df_mobile = pd.read_excel(caminho_arquivo)
        df_mobile = formatar_colunas(df_mobile)
        df_mobile = df_mobile.add_prefix('Mobile_')
    elif 'bipe_produtos' in arquivo:
        df_bipe = pd.read_excel(caminho_arquivo)
        df_bipe = formatar_colunas(df_bipe)
        df_bipe = df_bipe.add_prefix('Bipe_Prod_')
    elif 'Bipe_de_notas' in arquivo:
        df_bipe_notas = pd.read_excel(caminho_arquivo, sheet_name='Plan1')
        df_bipe_notas = formatar_colunas(df_bipe_notas)
        df_bipe_notas = df_bipe_notas.add_prefix('Bipe_Notas_')
    elif 'Carreta' in arquivo:
        df_carreta = pd.read_excel(caminho_arquivo)
        df_carreta = formatar_colunas(df_carreta)
        df_carreta = df_carreta.add_prefix('Carreta_')


df_lista = df_lista.drop_duplicates(subset="lista_Pedidos",keep="first")

df_final = (pd.merge(df_lista,df_carreta[['Carreta_Pedido', 'Carreta_Nf`S', 'Carreta_Chave', 'Carreta_Tipo_Fluxo']],
                      left_on='lista_Pedidos', right_on='Carreta_Pedido', how='left').drop(columns=['Carreta_Pedido'])
                      .merge(df_esl[['Esl_Nota Fiscal/Chave Nf-E', 
                                         'Esl_Última Ocorrência/Observações', 'Esl_Pessoa/Nome',
                                           'Esl_Última Ocorrência/Data Ocorrência']], left_on='Carreta_Chave', right_on='Esl_Nota Fiscal/Chave Nf-E', how='left' 

                      ).drop(columns=['Esl_Nota Fiscal/Chave Nf-E'])
                      .merge(df_mobile[['Mobile_Pedido', 'Mobile_Tipo', 'Mobile_Entregador']], left_on='lista_Pedidos', right_on='Mobile_Pedido', how='left').drop(columns=['Mobile_Pedido'])
                      .merge(df_bipe[['Bipe_Prod_Pedido', 'Bipe_Prod_Status_Deposito']], left_on='lista_Pedidos', right_on='Bipe_Prod_Pedido', how='left').drop(columns=['Bipe_Prod_Pedido'])
                      .merge(df_bipe_notas[['Bipe_Notas_Chave','Bipe_Notas_Ocorrencia']], left_on='Carreta_Chave', right_on='Bipe_Notas_Chave', how='left').drop(columns=['Bipe_Notas_Chave'])
            )



df_final_2 = df_final.merge(df_esl[['Esl_Nota Fiscal/Chave Nf-E', 'Esl_Ocorrência/Ocorrência']], left_on='Carreta_Chave', right_on='Esl_Nota Fiscal/Chave Nf-E', how='left').drop(columns=['Esl_Nota Fiscal/Chave Nf-E'])

filtro = df_final_2['Esl_Última Ocorrência/Observações'] == 'Não informado'

df_final_2.loc[filtro, 'Esl_Última Ocorrência/Observações'] = df_final_2.loc[filtro, 'Esl_Ocorrência/Ocorrência']
df_final_2 =  df_final_2.drop(columns=['Esl_Ocorrência/Ocorrência'])

df_final_2.to_excel('Relatorio_Diario.xlsx', sheet_name='Analise', index=False)