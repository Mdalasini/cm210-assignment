from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timezone, timedelta
from ..models.models import UserSummary

class Middleware:
  SECRET_KEY = "$2a$12$Edu22Sp0KpEoLdKUsfdp.O9IEV5e/qKOcmTng2uvalFZfr16fSSK."

  @staticmethod
  def create_token(user: UserSummary):
    payload = {
      "user_id": user.user_id,
      "user_type": user.user_type,
      "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    return jwt.encode(payload, Middleware.SECRET_KEY, algorithm="HS256")

  @staticmethod
  def decode_Token(token: str):
    try:
      return jwt.decode(token, Middleware.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
      return None

  @staticmethod
  def require_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
      token = request.cookies.get("token")
      if not token:
        return jsonify({"error": "No token"}), 401

      session = Middleware.decode_Token(token)
      if not session:
        return jsonify({
          "error": "Invalid or expired token"
        }), 401

      if session.get("user_type") != "admin":
        return jsonify({
          "error": "Admin access required"
        }), 403

      return f(*args, **kwargs)
    return wrapper

  @staticmethod
  def require_patron(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
      token = request.cookies.get("token")
      if not token:
        return jsonify({"error": "No token"}), 401

      session = Middleware.decode_Token(token)
      if not session:
        return jsonify({
          "error": "Invalid or expired token"
        }), 401

      if session.get("user_type") != "patron":
        return jsonify({
          "error": "Patron access required"
        }), 403

      return f(user=session, *args, **kwargs)
    return wrapper