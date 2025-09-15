# src/database.py

import fdb
from .config import Config

def get_db_connection():
    """
    Cria e retorna uma nova conexão com o banco de dados Firebird.
    """
    try:
        # Tenta estabelecer a conexão usando as credenciais do config.py
        conn = fdb.connect(
            dsn=Config.FIREBIRD_DSN,
            user=Config.FIREBIRD_USER,
            password=Config.FIREBIRD_PASSWORD,
            charset='UTF-8' # É uma boa prática definir o charset
        )
        return conn
    except fdb.Error as e:
        # Em caso de erro, imprime a mensagem e retorna None
        print(f"Erro ao conectar ao Firebird: {e}")
        return None