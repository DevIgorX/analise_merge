from flask import Blueprint, render_template, url_for, request, current_app, flash, redirect
import os
import subprocess
import json
import locale


rotas = Blueprint('rotas', __name__)


@rotas.route('/')
def home():
    return render_template('analise_dataframes.html')

from flask import request

@rotas.route('/verificar', methods=['POST'])
def verficar():
    arquivos = request.files.getlist('arquivos')

    if not arquivos:
        return "Nenhum arquivo enviado", 400
    
    pasta_dados = current_app.config['DIRETORIO_DADOS']

    for arquivo in arquivos:
        arquivo.save(os.path.join(pasta_dados, arquivo.filename))

    diretorio_raiz = current_app.config['DIRETORIO_RAIZ']
    caminho_analise = os.path.join(diretorio_raiz, 'analise')

    encoding_padrao = locale.getdefaultlocale(False)



    return redirect(url_for('rotas.home'))
