from . import auth
from flask import request, jsonify
from app.old_models import User, Blacklist
from flask_jwt_extended import (create_access_token,
                                get_jwt_identity,
                                jwt_required,
                                get_raw_jwt)


@auth.route("/api/auth/register", methods=['POST'])
def user_register():
    # TODO in the event of a database switch the following request with the database query
    username = request.data["username"]
    email = request.data["email"]
    password = request.data["password"]
    # checking if user already exists
    user = User.get_by_email(email)
    if not user:
            create_user = User()
            create_user.username = username
            create_user.email = email
            create_user.password_set(password)
            create_user.save_user()

            response = {
                "message": "You registered successfully"
            }

            return jsonify(response), 201

    else:
        response = {"message": "User already exists.Please login"}

        return jsonify(response), 202


@auth.route("/api/auth/login", methods=["POST"])
def user_login():
    """method to handle login of registered users"""
    email = request.data["email"]
    password = request.data["password"]
    user = User.get_by_email(email)

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
@jwt_required
def password_reset():
    email = get_jwt_identity()
    user = User.get_by_email(email)
    new_password = request.data["password"]
    user.password_set(new_password)

    response = jsonify({"message": "password reset successful"})

    return response, 200


@auth.route("/api/auth/logout", methods=["DELETE"])
@jwt_required
def logout():
    """endpoint for revoking the current users json web token"""
    jti = get_raw_jwt()['jti']
    Blacklist().blacklist.append(jti)
    return jsonify({"message": "Successfully logged out"})































