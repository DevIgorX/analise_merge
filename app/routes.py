
import os
import subprocess
import locale
from datetime import datetime
from database import buscar_dados_paginados
from flask import Blueprint, render_template, url_for, request, current_app, flash, redirect, jsonify, json, send_from_directory


rotas = Blueprint('rotas', __name__)


@rotas.route('/')
def home():
    # O current_app.config['DIRETORIO_DADOS'] deve apontar para a sua pasta 'dados'
    pasta_dados = current_app.config['DIRETORIO_DADOS']
    
    # Lista os arquivos, filtrando o .gitkeep
    arquivos_no_servidor = []
    if os.path.exists(pasta_dados):
        arquivos_no_servidor = [f for f in os.listdir(pasta_dados) if f != '.gitkeep']
    
    return render_template('analise_dataframes.html', arquivos_presentes=arquivos_no_servidor)


@rotas.route('/adicionar_dados', methods=['POST'])
def adicionar_dados():
    arquivos = request.files.getlist('arquivos')
    if not arquivos:
        flash("Nenhum arquivo enviado!", "danger")
        return redirect(url_for('rotas.home'))
    
    pasta_dados = current_app.config['DIRETORIO_DADOS']
    arquivos_pulados = []

    for arquivo in arquivos:
        caminho_completo = os.path.join(pasta_dados, arquivo.filename)
        
        # VERIFICAÇÃO: Se o arquivo já existe, pula e avisa
        if os.path.exists(caminho_completo):
            arquivos_pulados.append(arquivo.filename)
            continue 
            
        arquivo.save(caminho_completo)

    if arquivos_pulados:
        flash(f"Atenção! Os seguintes arquivos já estavam no servidor e foram ignorados: {', '.join(arquivos_pulados)}", "warning")
    else:
        flash("Arquivos enviados com sucesso!", "success")

    return redirect(url_for('rotas.home'))


@rotas.route('/analisar_dados')
def analisar_dados():
    pagina = request.args.get('pagina', 1, type=int)
    processar = request.args.get('processar', 'false') == 'true'

    # Só roda o script de análise se o usuário clicou no botão pela primeira vez
    if processar:
        diretorio_raiz = current_app.config['DIRETORIO_RAIZ']
        caminho_script = os.path.join(diretorio_raiz, 'analise.py') # Corrigido o nome
        enconding_padro = locale.getpreferredencoding(False)
        
        # Roda a análise (que agora salva no banco)
        subprocess.run(['python', caminho_script], capture_output=True, text=True, encoding=enconding_padro)

    # Busca os dados do banco (seja após o processamento ou apenas mudando de página)
    itens_por_pg = 7
    lista_dados, total_itens = buscar_dados_paginados(pagina, itens_por_pg)
    
    total_paginas = (total_itens + itens_por_pg - 1) // itens_por_pg

    dados_formatados = {
        "Excel": lista_dados,
        "pagina_atual": pagina,
        "total_paginas": total_paginas
    }

    return render_template('tabela_resultado.html', dados=dados_formatados)


@rotas.route('/nova_analise', methods=['GET', 'POST'])
def deletar_arquivos():
    pasta_dados = current_app.config['DIRETORIO_DADOS']

    for arquivo in os.listdir(pasta_dados):
        caminho_arquivo = os.path.join(pasta_dados, arquivo)
        if arquivo != '.gitkeep':
            os.remove(caminho_arquivo)

    return redirect(url_for('rotas.home'))
 

@rotas.route('/baixar_relatorio')
def baixar_relatorio():
    pasta_dados = current_app.config['DIRETORIO_DADOS']
  
    data_hoje = datetime.today().strftime('%d-%m-%Y')
    nome_arquivo = f'Analise_preventiva {data_hoje}.xlsx'


    return send_from_directory(pasta_dados, nome_arquivo, as_attachment=True)
    