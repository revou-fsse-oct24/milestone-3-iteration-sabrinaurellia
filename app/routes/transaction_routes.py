from flask import Blueprint, request, jsonify
from app import db
from app.models import Transaction, Account
from flask_jwt_extended import jwt_required, get_jwt_identity

transaction_bp = Blueprint("transaction_bp", __name__)

# Get all transactions
@transaction_bp.route("", methods=["GET"])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    account_id = request.args.get("account_id")
    transactions = Transaction.query.filter_by(account_id=account_id).all() if account_id else Transaction.query.all()
    result = [{"id": txn.id, "account_id": txn.account_id, "transaction_type": txn.transaction_type, "amount": txn.amount} for txn in transactions]
    return jsonify(result), 200

# Get a specific transaction by ID
@transaction_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_transaction(id):
    txn = Transaction.query.get(id)
    if not txn:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify({
        "id": txn.id,
        "account_id": txn.account_id,
        "transaction_type": txn.transaction_type,
        "amount": txn.amount,
        "timestamp": txn.timestamp
    }), 200

# Create a new transaction
@transaction_bp.route("", methods=["POST"])
@jwt_required()
def create_transaction():
    data = request.get_json()
    account_id = data.get("account_id")
    transaction_type = data.get("transaction_type")
    amount = data.get("amount")

    if transaction_type not in ["deposit", "withdrawal"]:
        return jsonify({"error": "Invalid transaction type"}), 400

    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    if transaction_type == "withdrawal" and account.balance < amount:
        return jsonify({"error": "Insufficient funds"}), 400

    transaction = Transaction(account_id=account.id, transaction_type=transaction_type, amount=amount)
    if transaction_type == "withdrawal":
        account.balance -= amount
    elif transaction_type == "deposit":
        account.balance += amount

    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        "message": f"{transaction_type.capitalize()} successful",
        "transaction_id": transaction.id,
        "new_balance": account.balance
    }), 201
