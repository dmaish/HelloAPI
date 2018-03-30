from . import auth
from flask import request, jsonify
from app.models import User


@auth.route("/api/auth/register", methods=['POST'])
def user_register():
    # TODO in the event of a database switch the following request with the database query
    username = request.data["username"]
    email = request.data["email"]
    password = request.data["password"]
    # checking if user already exists
    user = User.get_by_email(email)
    if not user:
        try:
            create_user = User()
            create_user.username = username
            create_user.email = email
            create_user.password_set(password)
            create_user.save_user()

            response = {
                "message": "You registered successfully"
            }
            return jsonify(response), 201
        except Exception as e:
            response = {
                "message": str(e)
            }
            return jsonify(response), 401

    else:
        response = {"message": "User already exists.Please login"}
        return response, 202







