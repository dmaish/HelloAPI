from . import auth
from flask import request, jsonify
from app.models import User
from flask_jwt_extended import (create_access_token,
                                get_jwt_identity,
                                jwt_required,
                                get_raw_jwt)
from app import db


@auth.route("/api/auth/register", methods=['POST'])
def user_register():
    # TODO in the event of a database switch the following request with the database query
    username = request.data["username"]
    email = request.data["email"]
    password = request.data["password"]

    # checking if user already exists
    if User.get_user_by_email(email):
        response = {"message": "User already exists.Please login"}

        return jsonify(response), 202
    else:
            user = User(username=username,
                        email=email,
                        password_hash=User.password_set(password))

            # add new user to database
            db.session.add(user)
            db.session.commit()

            response = {
                "message": "You registered successfully"
            }

            return jsonify(response), 201


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































