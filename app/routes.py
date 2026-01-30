
import os
import subprocess
import locale
from flask import Blueprint, render_template, url_for, request, current_app, flash, redirect, jsonify, json

rotas = Blueprint('rotas', __name__)


@rotas.route('/')
def home():
    return render_template('analise_dataframes.html')


@rotas.route('/adicionar_dados', methods=['POST'])
def adicionar_dados():
    arquivos = request.files.getlist('arquivos')

    if not arquivos:
        return "Nenhum arquivo enviado", 400
    
    pasta_dados = current_app.config['DIRETORIO_DADOS']

    for arquivo in arquivos:
        arquivo.save(os.path.join(pasta_dados, arquivo.filename))

    return redirect(url_for('rotas.home'))
   


@rotas.route('/analisar_dados', methods=['POST', 'GET'])
def analisar_dados():

    diretorio_raiz = current_app.config['DIRETORIO_RAIZ']
    caminho_scrip = os.path.join(diretorio_raiz, 'analise.py')

    enconding_padrao = locale.getpreferredencoding(False)

    resultado = subprocess.run(['python', caminho_scrip], capture_output=True, text=True, encoding=enconding_padrao)

    if resultado.returncode == 0:
        lista_completa = json.loads(resultado.stdout)
        
        # Lógica de Paginação
        itens_por_pagina = 10
        pagina = request.args.get('pagina', 1, type=int)
        
        total_itens = len(lista_completa)
        total_paginas = (total_itens + itens_por_pagina - 1) // itens_por_pagina
        
        # Calculando o início e fim da fatia
        inicio = (pagina - 1) * itens_por_pagina
        fim = inicio + itens_por_pagina
        
        dados_paginados = lista_completa[inicio:fim]
        
        dados_formatados = {
            "Excel": dados_paginados,
            "pagina_atual": pagina,
            "total_paginas": total_paginas
        }
        
        return render_template('tabela_resultado.html', dados=dados_formatados)
    else:
        return 'Erro na análise', 500



@rotas.route('/nova_analise', methods=['GET', 'POST'])
def deletar_arquivos():
    pasta_dados = current_app.config['DIRETORIO_DADOS']

    for arquivo in os.listdir(pasta_dados):
        caminho_arquivo = os.path.join(pasta_dados, arquivo)
        if arquivo != '.gitkeep':
            os.remove(caminho_arquivo)

    return redirect(url_for('rotas.home'))
 
