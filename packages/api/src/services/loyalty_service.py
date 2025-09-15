# src/services/loyalty_service.py

import fdb
from ..database import get_db_connection
from ..services import settings_service # 1. Import do novo serviço de configurações

def _get_order_total(order_id, cur):
    """Função auxiliar para calcular o total de um pedido."""
    sql = "SELECT SUM(QUANTITY * UNIT_PRICE) FROM ORDER_ITEMS WHERE ORDER_ID = ?;"
    cur.execute(sql, (order_id,))
    result = cur.fetchone()
    return result[0] if result and result[0] is not None else 0

def _create_loyalty_account_if_not_exists(user_id, cur):
    """Garante que o usuário tenha uma entrada na tabela LOYALTY_POINTS."""
    sql = """
        MERGE INTO LOYALTY_POINTS lp
        USING (SELECT ? AS USER_ID FROM RDB$DATABASE) AS new_data
        ON (lp.USER_ID = new_data.USER_ID)
        WHEN NOT MATCHED THEN
            INSERT (USER_ID) VALUES (new_data.USER_ID);
    """
    cur.execute(sql, (user_id,))

def add_points_for_order(user_id, order_id, cur):
    """Calcula e adiciona pontos de fidelidade para um pedido."""
    # ... (esta função continua exatamente a mesma que você já tinha)
    try:
        _create_loyalty_account_if_not_exists(user_id, cur)
        order_total = _get_order_total(order_id, cur)
        points_to_add = int(order_total / settings_service.get_setting('LOYALTY_POINTS_TO_REAL_RATIO', 100)) # Melhoria: Usando a configuração
        if points_to_add > 0:
            sql_update_balance = "UPDATE LOYALTY_POINTS SET ACCUMULATED_POINTS = ACCUMULATED_POINTS + ? WHERE USER_ID = ?;"
            cur.execute(sql_update_balance, (points_to_add, user_id))
            sql_insert_history = """
                INSERT INTO LOYALTY_POINTS_HISTORY (USER_ID, POINTS, EXPIRES_AT, REASON)
                VALUES (?, ?, DATEADD(90 DAY TO CURRENT_DATE), ?);
            """
            cur.execute(sql_insert_history, (user_id, points_to_add, f"Pedido ID: {order_id}"))
        return True
    except fdb.Error as e:
        print(f"Erro ao adicionar pontos de fidelidade: {e}")
        raise e

# 2. AQUI ESTÁ A FUNÇÃO AUXILIAR QUE FALTAVA
def get_user_balance_points(user_id, cur):
    """Função auxiliar para pegar o saldo atual de pontos dentro de uma transação."""
    sql = "SELECT (ACCUMULATED_POINTS - SPENT_POINTS) FROM LOYALTY_POINTS WHERE USER_ID = ?;"
    cur.execute(sql, (user_id,))
    result = cur.fetchone()
    return result[0] if result else 0

def redeem_points_for_discount(user_id, points_to_redeem, order_id, cur):
    """Valida e aplica o resgate de pontos para um pedido."""
    if points_to_redeem <= 0:
        return 0.0

    current_balance = get_user_balance_points(user_id, cur)
    if points_to_redeem > current_balance:
        raise ValueError("Pontos para resgate insuficientes.")

    conversion_ratio = settings_service.get_setting('LOYALTY_POINTS_TO_REAL_RATIO', 100)
    if conversion_ratio <= 0:
        raise ValueError("Taxa de conversão de pontos inválida no sistema.")

    discount_amount = points_to_redeem / conversion_ratio

    sql_update_balance = "UPDATE LOYALTY_POINTS SET SPENT_POINTS = SPENT_POINTS + ? WHERE USER_ID = ?;"
    cur.execute(sql_update_balance, (points_to_redeem, user_id))

    sql_insert_history = """
        INSERT INTO LOYALTY_POINTS_HISTORY (USER_ID, POINTS, REASON)
        VALUES (?, ?, ?);
    """
    cur.execute(sql_insert_history, (user_id, -points_to_redeem, f"Resgate no Pedido ID: {order_id}"))

    return discount_amount

def get_loyalty_balance(user_id):
    """Busca o saldo de pontos de um usuário."""
    # ... (esta função continua exatamente a mesma que você já tinha)
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql = "SELECT ACCUMULATED_POINTS, SPENT_POINTS FROM LOYALTY_POINTS WHERE USER_ID = ?;"
        cur.execute(sql, (user_id,))
        row = cur.fetchone()
        if row:
            return {"accumulated_points": row[0], "spent_points": row[1], "current_balance": row[0] - row[1]}
        return {"accumulated_points": 0, "spent_points": 0, "current_balance": 0}
    except fdb.Error as e:
        print(f"Erro ao buscar saldo de pontos: {e}")
        return None
    finally:
        if conn: conn.close()

def get_loyalty_history(user_id):
    """Busca o histórico de transações de pontos de um usuário."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql = """
            SELECT POINTS, REASON, EARNED_AT 
            FROM LOYALTY_POINTS_HISTORY 
            WHERE USER_ID = ? 
            ORDER BY EARNED_AT DESC;
        """
        cur.execute(sql, (user_id,))
        history = []
        for row in cur.fetchall():
            history.append({
                "points": row[0],
                "reason": row[1],
                "date": row[2].strftime('%Y-%m-%d %H:%M:%S')
            })
        return history
    except fdb.Error as e:
        print(f"Erro ao buscar histórico de pontos: {e}")
        return [] # Retorna lista vazia em caso de erro
    finally:
        if conn: conn.close()