
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

    enconding_padro = locale.getpreferredencoding(False)

    resultado = subprocess.run(['python', caminho_scrip], capture_output=True, text=True, encoding=enconding_padro)

    if resultado.returncode == 0:
        dados_tabela = json.loads(resultado.stdout)
        return render_template('tabela_resultado.html', dados=dados_tabela)
    else:
        return 'não deu certo aqui'

   
