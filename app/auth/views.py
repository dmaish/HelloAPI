import re

from flask import request, jsonify
from flask_jwt_extended import (create_access_token,
                                jwt_required,
                                get_raw_jwt)

# local imports
from . import auth
from app.models import *
from app import db, jwt
from .decorators import *


@auth.route("/", methods=['GET'])
def home():
    """Home page"""
    return jsonify(
        {
            "message": "Welcome to Hello Books"
        }
    )


@auth.route("/api/auth/register", methods=['POST'])
def user_register():
    """method to register new user"""
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if username:
        username = username.strip()
        if username == "" or username == " ":
            return jsonify({
                "message": "username field cannot be empty"
            })

        elif len(username) < 5:
            return jsonify({
                "message": "username must have 5 or more characters"
            })

    elif not username:
        return jsonify({
            "message": "please make sure to submit your username"
        })

    # email validation
    if email:
        email = email.strip()
        if email == "" or email == " ":
            return jsonify({
                "message": "email field cannot be empty"
            })
        else:
            if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
                pass
            else:
                return jsonify({
                    "message": "email submitted is not a valid email"
                })
    elif not email:
        return jsonify({
            "message": "please make sure to submit your email"
        })

    # password validation
    if password:
        password = password.strip()
        if password == "" or password == " ":
            return jsonify({
                "message": "password field cannot be empty"
            })
        if len(password) < 8:
            return jsonify({
                "message": "password must have 8 or more characters"
            })
        if not re.match("^[a-zA-Z0-9]+$", password):
            return jsonify({
                "message": "your password must contain both letters and numbers"
            })
        else:
            pass

    elif not password:
        return jsonify({
            "message": "please make sure to submit your password"
        })

    # checking if user already exists
    if User.get_user_by_email(email):
        response = {"message": "User already exists.Please login"}

        return jsonify(response), 202

    # storing user details into database
    user = User(username=username.strip(),
                email=email.strip(),
                password=password.strip())

    db.session.add(user)
    db.session.commit()

    response = {
        "message": "you registered successfully"
    }

    return jsonify(response), 201


@auth.route("/api/auth/login", methods=["POST"])
def user_login():
    """method to handle login of registered users"""
    email = request.data.get("email")
    password = request.data.get("password")

    # get the user if they exist and if they gave valid password...
    if not email:
        return jsonify("message: please make sure to type in your email")
    if not password:
        return jsonify("message: please make sure to type in your password")
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
@check_if_logged_out
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
@check_if_logged_out
def logout():
    """method for revoking the current user's json web token"""
    jti = get_raw_jwt()['jti']
    revoked_token = Revoked_Tokens(token=jti)
    db.session.add(revoked_token)
    db.session.commit()
    response = jsonify({"message": "you have successfully logged out"})
    return response, 200


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist_loader(decrypted_token):
    """jwt decorator that checks if token is revoked"""
    jti = decrypted_token['jti']
    if Revoked_Tokens.query.filter_by(token=jti).first():
        return True
    else:
        return False


