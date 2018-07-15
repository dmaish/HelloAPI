import re

from flask import request, jsonify

from app import db
from app.models import User


def user_register():
    """method to register new user"""
    username = request.data["username"]
    email = request.data["email"],
    password = request.data["password"]

    if not username:
        return jsonify({
            "message": "please make sure to type in your username"
        })
    if not email:
        return jsonify({
            "message: please make sure to type in your username"
        })

    elif password == "" or password == " ":
        return jsonify({
            "message": "please make sure to type in your password"
        })
    elif len(password) < 8:
        return jsonify({
            "message: password must have 8 or more characters"
        })
    elif len(username) < 5:
        return jsonify({
            "message: username must have 5 or more characters"
        })

    else:
        # checking if user already exists
        if User.get_user_by_email(email):
            response = {"message": "User already exists.Please login"}

            return jsonify(response), 202
        else:
            if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
                user = User(username=username.strip(),
                            email=email.strip(),
                            password=password.strip())

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

