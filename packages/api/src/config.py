# packages/src/src/config.py

import os

# 1. Encontra o caminho absoluto para a raiz do monorepo (royalburger-app/)
# Subimos 4 níveis a partir de config.py (src/ -> src/ -> packages/ -> royalburger-app/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-muito-dificil-de-adivinhar'
    DEBUG = True
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'uma-outra-chave-jwt-muito-segura'

    # --- Configurações do Banco de Dados Firebird ---
    # 2. A variável do caminho do banco fica DENTRO da classe
    # 3. Ela contém apenas o caminho do arquivo, que é o que o driver fdb espera
    DATABASE_PATH = os.path.join(PROJECT_ROOT, 'database', 'royalburger.fdb')
    FIREBIRD_USER = 'SYSDBA'
    FIREBIRD_PASSWORD = 'sysdba' # ou 'masterkey'

    # --- Configurações do Flask-Mail ---
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', '1', 't']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') # Ex: 'seu-email@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') # Ex: 'sua-senha-de-app'
    MAIL_DEFAULT_SENDER = ('Royal Burger', MAIL_USERNAME)