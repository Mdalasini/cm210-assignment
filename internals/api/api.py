from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from ..services.users import UserService
from ..services.books import BookService
from ..services.borrows import BorrowService
from ..models.models import UserCredentials, NewUser, NewBook, NewBorrow
from ..middleware.session import Middleware
from pydantic import ValidationError
from dataclasses import asdict

app = Flask(__name__)
CORS(app)

# TODO:
# [x] /login (get)
# [x] /all/books (get)
# [x] /all/borrows (get)
# [x] /user/borrows (get)
# [x] /new/user (post)
# [x] /new/book (post)
# [x] /new/borrow (post)
# [x] /new/return (post)


@app.route("/login", methods=["POST"])
def login():
    try:
        user = UserCredentials(**request.get_json())

        if not UserService.username_exists(user.username):
            return jsonify({"error": "User does not exist"})

        summary = UserService.get_user_summary(user)
        if summary is None:
            return jsonify({"error": "Incorrect password"})

        token = Middleware.create_token(summary)
        resp = make_response("Logged in")
        resp.set_cookie("token", token)
        return resp

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400


@app.route("/all/books", methods=["GET"])
def all_books():
    books = BookService.get_all()
    return jsonify([asdict(book) for book in books])


@app.route("/all/borrows", methods=["GET"])
def all_borrows():
    borrows = BorrowService.get_all()
    return jsonify([asdict(borrow) for borrow in borrows])


@app.route("/user/borrows", methods=["GET"])
def user_borrows():
    user_id = request.args.get("id", type=int)
    if user_id is None:
        return jsonify({"error": "Invalid arguments"}), 401

    try:
        borrows = BorrowService.get_users(user_id)
        return jsonify([asdict(borrow) for borrow in borrows])
    except ValueError as e:
        return jsonify({"error": str(e)}), 401


@app.route("/new/user", methods=["POST"])
def sign_up():
    try:
        user = NewUser(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    try:
        summary = UserService.new_user(user)
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    token = Middleware.create_token(summary)
    resp = make_response("Logged in")
    resp.set_cookie("token", token)
    return resp


@app.route("/new/book", methods=["POST"])
# @Middleware.require_admin()
def new_book():
    try:
        book = NewBook(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    try:
        BookService.new_book(book)
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    return jsonify({"message": "Book created successfully"}), 200


@app.route("/new/borrow", methods=["POST"])
# @Middleware.require_patron()
def new_borrow():
    try:
        borrow = NewBorrow(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    try:
        BorrowService.new_borrow(borrow, 1)  # ! use current user's id
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    return jsonify({"message": "Book borrowed successfully"}), 200


@app.route("/new/return", methods=["POST"])
# @Middleware.require_patron()
def new_return():
    borrow_id = request.args.get("id", type=int)
    if borrow_id is None:
        return jsonify({"error": "Invalid arguments"}), 401

    try:
        BorrowService.new_return(borrow_id, 1)  # ! use current user's id
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    return jsonify({"message": "Borrow returned successfully"}), 200
