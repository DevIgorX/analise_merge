def formatar_colunas(df):
    df.columns = df.columns.str.strip().str.lower().str.title()
    return df

