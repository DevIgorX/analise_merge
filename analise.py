import pandas as pd


df_preventiva = pd.read_excel('PREVENTIVA.xlsx')
df_carreta = pd.read_excel('CARRETA.xlsx')
df_esl = pd.read_excel('ESL.xlsx')
df_mobile = pd.read_excel('MOBILE.xlsx')
df_bipe = pd.read_excel('BIPE.xlsx')
df_bipe_notas = pd.read_excel('BIPE DE NOTAS.xlsx')


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
            df_bipe[['PEDIDO', 'INFO']],
            left_on='PEDIDO 1P/FULL',
            right_on='PEDIDO',
            how='left'
        )
        .drop(columns=['PEDIDO'])

        .merge(
            df_bipe_notas[['NF', 'OCORRENCIA']],
            left_on='NF`s',
            right_on='NF',
            how='left'
        )
        .drop(columns=['NF'])
)


colunas_datas = [
    'PREVISÃO ENTREGA',
    'Última ocorrência/Data ocorrência'
]

for col in colunas_datas:
    df_final[col] = pd.to_datetime(df_final[col], errors='coerce')


with pd.ExcelWriter(
    '29-12-2025.xlsx',
    engine='xlsxwriter',
    datetime_format='dd/mm/yyyy'
) as writer:
    
    df_final.to_excel(
        writer,
        sheet_name='Relatorio_diario',
        index=False
    )

