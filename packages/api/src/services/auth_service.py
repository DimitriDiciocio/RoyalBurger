# src/services/auth_service.py

import bcrypt
import fdb
from functools import wraps
from flask import jsonify
from ..database import get_db_connection
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

def authenticate(email, password):
    """Verifica credenciais e retorna um token JWT. Agora serve para qualquer role."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Importante: busca apenas usuários ativos!
        sql = "SELECT ID, PASSWORD_HASH, ROLE FROM USERS WHERE EMAIL = ? AND IS_ACTIVE = TRUE;"
        cur.execute(sql, (email,))
        user_record = cur.fetchone()

        if user_record and bcrypt.checkpw(password.encode('utf-8'), user_record[1].encode('utf-8')):
            user_id, _, user_role = user_record
            identity_data = {"id": user_id, "role": user_role}
            access_token = create_access_token(identity=user_id, additional_claims=identity_data)
            return access_token
        return None
    except fdb.Error as e:
        print(f"Erro no banco de dados durante a autenticação: {e}")
        return None
    finally:
        if conn: conn.close()

def require_role(*roles):
    # ... (o código do decorator continua exatamente o mesmo) ...
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get("role")
            if user_role in roles:
                return f(*args, **kwargs)
            else:
                return jsonify({"msg": "Acesso não autorizado para esta função."}), 403
        return decorated_function
    return decorator