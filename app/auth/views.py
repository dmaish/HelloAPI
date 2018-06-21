import re

from flask import request, jsonify
from flask_jwt_extended import (create_access_token,
                                get_jwt_identity,
                                jwt_required,
                                get_raw_jwt)

# local imports
from . import auth
from app.models import *
from app import db, jwt


@auth.route("/api/auth/register", methods=['POST'])
def user_register():
    """method to register new user"""
    username = request.data["username"]
    email = request.data["email"]
    password = request.data["password"]

    # checking if user already exists

    if User.get_user_by_email(email):
        response = {"message": "User already exists.Please login"}

        return jsonify(response), 202
    else:
        if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            user = User(username=username,
                        email=email,
                        password=password)

            # add new user to database
            db.session.add(user)
            db.session.commit()

            response = {
                "message": "you registered successfully"
            }

            return jsonify(response), 201
        else:
            response = {
                "message": "please enter a valid email address"
            }
            return jsonify(response)


@auth.route("/api/auth/login", methods=["POST"])
def user_login():
    """method to handle login of registered users"""
    email = request.data["email"]
    password = request.data["password"]

    # get the user if they exist and if they gave valid password...
    registered_user = User.get_user_by_email(email)
    if registered_user is not None and registered_user.check_password(password):
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
    """method to reset password of logged in user"""
    new_password = request.data["password"]

    email = get_jwt_identity()
    user = User.get_user_by_email(email)

    user.password = new_password
    db.session.commit()

    response = jsonify({"message": "password reset successful"})

    return response, 200


@auth.route("/api/auth/logout", methods=["DELETE"])
@jwt_required
def logout():
    """method for revoking the current user's json web token"""
    jti = get_raw_jwt()['jti']
    revoked_token = Revoked_Tokens(token=jti)
    db.session.add(revoked_token)
    db.session.commit()
    response = jsonify({"message": "you have successfully logged out"})
    return response, 200


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist_loader(dycrypted_token):
    """jwt decorator that checks if token is revoked"""
    jti = dycrypted_token['jti']
    if Revoked_Tokens.query.filter_by(token=jti):
        return True



