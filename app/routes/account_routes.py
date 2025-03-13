from flask import Blueprint, request, jsonify
from app import db
from app.models import Account
from flask_jwt_extended import jwt_required, get_jwt_identity

account_bp = Blueprint("account_bp", __name__)

# Get all accounts
@account_bp.route("", methods=["GET"])
@jwt_required()
def get_accounts():
    user_id = get_jwt_identity()
    accounts = Account.query.filter_by(user_id=user_id).all()
    result = [{"id": acc.id, "account_type": acc.account_type, "balance": acc.balance} for acc in accounts]
    return jsonify(result), 200

# Get a specific account by ID
@account_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_account(id):
    account = Account.query.get(id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({
        "id": account.id,
        "account_type": account.account_type,
        "balance": account.balance
    }), 200

# Create a new account
@account_bp.route("", methods=["POST"])
@jwt_required()
def create_account():
    data = request.get_json()
    account_type = data.get("account_type")

    if account_type not in ["savings", "checking"]:
        return jsonify({"error": "Invalid account type"}), 400

    user_id = get_jwt_identity()
    new_account = Account(user_id=user_id, account_type=account_type)
    db.session.add(new_account)
    db.session.commit()

    return jsonify({
        "message": f"{account_type.capitalize()} account created successfully",
        "account_id": new_account.id
    }), 201
