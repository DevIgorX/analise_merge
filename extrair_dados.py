import pdfplumber
import pandas as pd
import re
import os

pedidos = []
notas = []
#um comentario

caminho_script = os.path.abspath(__file__)
diretorio_raiz = os.path.dirname(caminho_script)
pasta_romaneio = os.path.join(diretorio_raiz,'Arquivos_pdf')
pasta_Excel = os.path.join(diretorio_raiz, 'Arquivos_xlsx')

for arquivo in os.listdir(pasta_romaneio):
    if arquivo.endswith('.pdf'):
     caminho_arquivo = os.path.join(pasta_romaneio, arquivo)
     with pdfplumber.open(caminho_arquivo) as pdf:
      for pagina in pdf.pages:
        texto = pagina.extract_text()

        if not texto:
            continue

        linhas = texto.split("\n")

        for linha in linhas:
            matches = re.findall(r'(\d{10}).*?(\d{5,8})', linha)

            for pedido, nota in matches:
                pedidos.append(pedido)
                notas.append(nota)




df = pd.DataFrame({
    "Pedido": pedidos,
    "Nota Fiscal": notas
})

df.to_excel("pedidos_notas.xlsx", index=False)

print("Planilha criada com sucesso!")