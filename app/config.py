import os

DIRETORIO_ATUAL = os.path.abspath(__file__)

DIRETORIO_APP = os.path.dirname(DIRETORIO_ATUAL)
DIRETORIO_RAIZ = os.path.dirname(DIRETORIO_APP)
DIRETORIO_DADOS = os.path.abspath(os.path.join(DIRETORIO_RAIZ, 'dados'))


SECRET_KEY = 'Alohomora'
