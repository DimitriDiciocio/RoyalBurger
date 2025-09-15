# src/routes/customer_routes.py

from flask import Blueprint, request, jsonify
from ..services import user_service, address_service, loyalty_service  # 1. Importa o novo serviço
from ..services.auth_service import require_role
from flask_jwt_extended import jwt_required, get_jwt  # Importa funções do JWT

customer_bp = Blueprint('customers', __name__)


# --- ROTAS DE USUÁRIO (CLIENTE) ---
# ... (as rotas de GET, POST, PUT, DELETE para /src/customers que já fizemos continuam aqui) ...
# POST /src/customers/ -> Cria um novo cliente
@customer_bp.route('/', methods=['POST'])
def create_customer_route():
    # ... (código existente)
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password') or not data.get('full_name'):
        return jsonify({"error": "Nome completo, email e senha são obrigatórios"}), 400
    new_user = user_service.create_user(data)
    if new_user:
        return jsonify(new_user), 201
    else:
        return jsonify({"error": "Não foi possível criar o usuário. O e-mail já pode estar em uso."}), 409


# GET /src/customers/ -> Rota protegida para admins/managers verem todos os clientes
@customer_bp.route('/', methods=['GET'])
@require_role('admin', 'manager')
def get_all_customers_route():
    # ... (código existente)
    customers = user_service.get_users_by_role('customer')
    return jsonify(customers), 200


# GET /src/customers/<id> -> Rota para um cliente ver seus próprios dados ou um admin ver qualquer um
@customer_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_customer_by_id_route(user_id):
    # ... (código existente)
    claims = get_jwt()
    if claims.get('role') != 'admin' and claims.get('id') != user_id:
        return jsonify({"msg": "Acesso não autorizado"}), 403
    user = user_service.get_user_by_id(user_id)
    if user and user['role'] == 'customer':
        return jsonify(user), 200
    return jsonify({"msg": "Cliente não encontrado"}), 404


# PUT /src/customers/<id> -> Rota para um cliente atualizar seus dados
@customer_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_customer_route(user_id):
    # ... (código existente)
    claims = get_jwt()
    if claims.get('id') != user_id:
        return jsonify({"msg": "Você só pode atualizar seus próprios dados"}), 403
    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição não pode ser vazio"}), 400
    if user_service.update_user(user_id, data):
        return jsonify({"msg": "Dados do cliente atualizados com sucesso"}), 200
    return jsonify({"error": "Falha ao atualizar dados do cliente"}), 404


# DELETE /src/customers/<id> -> Rota para um cliente inativar sua conta
@customer_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_customer_route(user_id):
    # ... (código existente)
    claims = get_jwt()
    if claims.get('role') != 'admin' and claims.get('id') != user_id:
        return jsonify({"msg": "Acesso não autorizado"}), 403
    if user_service.deactivate_user(user_id):
        return jsonify({"msg": "Cliente inativado com sucesso"}), 200
    return jsonify({"error": "Falha ao inativar cliente ou cliente não encontrado"}), 404


# --- ROTAS DE ENDEREÇO (ADDRESS) ---

# POST /src/customers/<user_id>/addresses -> Cria um novo endereço para o cliente
@customer_bp.route('/<int:user_id>/addresses', methods=['POST'])
@jwt_required()
def add_address_route(user_id):
    claims = get_jwt()
    # Garante que o usuário logado só pode adicionar endereços para si mesmo
    if claims.get('id') != user_id:
        return jsonify({"msg": "Acesso não autorizado"}), 403

    data = request.get_json()
    if not data or not all(k in data for k in ['city', 'neighborhood', 'street', 'number']):
        return jsonify({"error": "Campos obrigatórios: city, neighborhood, street, number"}), 400

    new_address = address_service.create_address(user_id, data)
    if new_address:
        return jsonify(new_address), 201
    return jsonify({"error": "Não foi possível adicionar o endereço"}), 500


# GET /src/customers/<user_id>/addresses -> Lista todos os endereços do cliente
@customer_bp.route('/<int:user_id>/addresses', methods=['GET'])
@jwt_required()
def get_addresses_route(user_id):
    claims = get_jwt()
    # Garante que o usuário logado só pode ver seus próprios endereços
    if claims.get('id') != user_id:
        return jsonify({"msg": "Acesso não autorizado"}), 403

    addresses = address_service.get_addresses_by_user_id(user_id)
    return jsonify(addresses), 200


# PUT /src/customers/addresses/<address_id> -> Atualiza um endereço específico
@customer_bp.route('/addresses/<int:address_id>', methods=['PUT'])
@jwt_required()
def update_address_route(address_id):
    claims = get_jwt()

    # Verificação de posse: o endereço a ser atualizado pertence ao usuário logado?
    address = address_service.get_address_by_id(address_id)
    if not address or address.get('user_id') != claims.get('id'):
        return jsonify({"msg": "Endereço não encontrado ou acesso não autorizado"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição não pode ser vazio"}), 400

    if address_service.update_address(address_id, data):
        return jsonify({"msg": "Endereço atualizado com sucesso"}), 200
    return jsonify({"error": "Falha ao atualizar endereço"}), 500


# DELETE /src/customers/addresses/<address_id> -> Deleta um endereço específico
@customer_bp.route('/addresses/<int:address_id>', methods=['DELETE'])
@jwt_required()
def delete_address_route(address_id):
    claims = get_jwt()

    # Verificação de posse
    address = address_service.get_address_by_id(address_id)
    if not address or address.get('user_id') != claims.get('id'):
        return jsonify({"msg": "Endereço não encontrado ou acesso não autorizado"}), 404

    if address_service.delete_address(address_id):
        return jsonify({"msg": "Endereço deletado com sucesso"}), 200
    return jsonify({"error": "Falha ao deletar endereço"}), 500


# --- ROTAS DE FIDELIDADE (LOYALTY) ---

# GET /src/customers/<user_id>/loyalty/balance -> Cliente consulta seu saldo de pontos
@customer_bp.route('/<int:user_id>/loyalty/balance', methods=['GET'])
@require_role('customer')
def get_loyalty_balance_route(user_id):
    claims = get_jwt()
    # Garante que o usuário logado só pode ver seu próprio saldo
    if claims.get('id') != user_id:
        return jsonify({"msg": "Acesso não autorizado"}), 403

    balance = loyalty_service.get_loyalty_balance(user_id)
    if balance is not None:
        return jsonify(balance), 200
    return jsonify({"error": "Não foi possível buscar o saldo"}), 500


# GET /src/customers/<user_id>/loyalty/history -> Cliente consulta seu histórico
@customer_bp.route('/<int:user_id>/loyalty/history', methods=['GET'])
@require_role('customer')
def get_loyalty_history_route(user_id):
    claims = get_jwt()
    # Garante que o usuário logado só pode ver seu próprio histórico
    if claims.get('role') != 'admin' and claims.get('id') != user_id:
        return jsonify({"msg": "Acesso não autorizado"}), 403

    history = loyalty_service.get_loyalty_history(user_id)
    return jsonify(history), 200