# global imports
from flask import request, jsonify
from app.models import UsersModel, Blacklist
from flask_jwt_extended import (create_access_token,
                                jwt_required,
                                get_raw_jwt)
# local imports
from . import auth


@auth.route("/api/auth/register", methods=['POST'])
def user_register():
    """method to create new user"""
    username = request.data["username"]
    email = request.data["email"]
    password_with_spaces = request.data["password"]

    # remove trailing spaces in password
    password = "".join(password_with_spaces.split(password_with_spaces))

    # checking if user already exists
    user = UsersModel.get_by_email(email)
    if not user:
        try:
            password = UsersModel.password_set(password)
            create_user = UsersModel(username, email, password)
            create_user.save_user()

            response = {
                "message": "You registered successfully"
            }
            return jsonify(response)
        except Exception as e:
            response = {
                "message": str(e)
            }
            return jsonify(response), 401

    else:
        response = jsonify({"message": "User already exists.Please login"})
        return response, 409


@auth.route("/api/auth/login", methods=["POST"])
def user_login():
    """method to login registered users"""
    email = request.data["email"]
    user = UsersModel.get_by_email(email)
    password_with_spaces = request.data["password"]
    # remove trailing spaces in password
    password = "".join(password_with_spaces.split(password_with_spaces))

    # get the user if they exist and if they gave valid password...
    if user and user.check_password(password):
            # generate the access token
            access_token = create_access_token(identity=email)
            if access_token:
                response = {
                    "message": "You logged in successfully",
                    "access_token": access_token
                }

                return jsonify(response), 200

    else:
        # user doesn't exist
        response = {
            "message": "Invalid email or password, Please try again"
        }
        return jsonify(response), 401


@auth.route("/api/auth/reset-password", methods=["POST"])
def password_reset():
    """method to reset user password"""
    new_password = request.data["password"]
    UsersModel().password_set(new_password)

    response = jsonify({"message": "password reset successful",
                        "new": new_password})

    return response, 200


@auth.route("/api/auth/logout", methods=["DELETE"])
@jwt_required
def logout():
    """endpoint for revoking the current users json web token"""
    jti = get_raw_jwt()['jti']
    Blacklist().blacklist.append(jti)
    return jsonify({"message": "Successfully logged out"})
