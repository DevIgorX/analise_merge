from flask import Blueprint, render_template, url_for, request, current_app, flash, redirect
from werkzeug.utils import secure_filename
import os



rotas = Blueprint('rotas', __name__)


@rotas.route('/')
def home():
    return render_template('analise_dataframes.html')

@rotas.route('/verificar', methods=['POST'])
def verficar():

    arquivo = request.files['arquivo']

    if not arquivo or arquivo.filename == '':
        flash('Nenhum arquivo enviado')
        return redirect(url_for('rotas.home'))
    
    upload_path = current_app.config['DIRETORIO_DADOS']
    nome_arquivo = secure_filename(arquivo.filename) 

    caminho_final = os.path.join(upload_path, nome_arquivo)

    arquivo.save(caminho_final)

    
    flash('Arquivo salvo com sucesso!')

    return redirect(url_for('rotas.home'))