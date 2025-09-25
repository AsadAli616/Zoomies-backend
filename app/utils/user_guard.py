from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
from ..models.user import User

def role_guard(allowed_roles):
    """
    Guard that checks:
    - JWT is valid
    - User exists in DB
    - User has one of the allowed roles
    """
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            email = get_jwt_identity()
            user = User.find_by_email(email)

            if not user:
                return jsonify({"msg": "User not found"}), 404

            if not user.get("is_active", True):
                return jsonify({"msg": "User is inactive"}), 403

            if not user.get("verified_email", False):
                return jsonify({"msg": "Email not verified"}), 403

            user_roles = user.get("roles", [])
            if not any(role in allowed_roles for role in user_roles):
                return jsonify({"msg": "Access denied: insufficient role"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
