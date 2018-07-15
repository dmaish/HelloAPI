from flask import request,jsonify
from flask_jwt_extended import (create_access_token,
                                get_jwt_identity,
                                jwt_required,
                                get_raw_jwt)


from ..models import *


# method to check if user has already logged out
def check_if_logged_out(func):
    print(func)
    token = request.headers.get("Bearer Token")
    jti = token['jti']

    if Revoked_Tokens.query.filter_by(token=jti).first():
        return jsonify({
            "message": "already logged out, login again"
        })
    else:
        return None
