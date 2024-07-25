from flask import Flask, jsonify
from flask_smorest import Api
from db import db
import os
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from blocklist import BLOCKLIST
from flask_cors import CORS

from model import AdminUserModel, InvestorModel, BusinessStartUpModel

from views.adminUser import blp as admin_user_blp
from views.login import blp as login_blp
from views.businessStartUps import blp as business_start_up_blp
from views.investor import blp as investor_blp
from views.businessInvestment import blp as business_investment_blp
from views.returnOnInvestment import blp as return_on_investment_blp
from views.conversation import blp as conversation_blp
from views.trends import blp as trends_blp
from views.insight import blp as insight_blp


def main_app(app: Flask):
    app.secret_key = 'oBQ4GBTlzpSwE2OCGzRCGcXVANO9bsYZL_Cf3CSEXPs'

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "INVEST-IQ REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.1.0"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/invest-iq-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    migrate = Migrate(app, db)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = 'alpha-and-omega'
    jwt = JWTManager(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # this fx is invoked When a fresh token is required but a non-fresh token is provided
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    # whenever we receive a jwt this fx run and check if the token is in the block list
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    # whenever we receive a jwt this fx run and check if the user still exist in DB
    @jwt.token_verification_loader
    def check_if_token_is_valid(header, payload):
        if not 'isAdmin' in payload:
            return False
        userType = payload['isAdmin']
        userEmail = payload['sub']
        if userType == 'admin':
            try:
                user = AdminUserModel.find_by_email(userEmail)
                return user.isActive
            except:
                return False
        elif userType == 'business-startup':
            try:
                user = BusinessStartUpModel.find_by_email(userEmail)
                return user.isActive
            except:
                return False
        else:
            try:
                user = InvestorModel.find_by_email(userEmail)
                return user.isActive
            except:
                return False

    # invoked when the token used is not valid
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    # when the above fx return true, this fx is invoked to indicate that the token is expired/logout
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401,

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401,

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    api.register_blueprint(admin_user_blp)
    api.register_blueprint(login_blp)
    api.register_blueprint(business_start_up_blp)
    api.register_blueprint(investor_blp)
    api.register_blueprint(business_investment_blp)
    api.register_blueprint(return_on_investment_blp)
    api.register_blueprint(conversation_blp)
    api.register_blueprint(trends_blp)
    api.register_blueprint(insight_blp)

    return app
