from flask_smorest import Blueprint, abort
from flask.views import MethodView
from model import BusinessStartUpModel
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import jwt_required
import uuid_utils as uuid

from schemas import (
    PlainStartUpSchema,
    StartUpSchema,
    PlainUpdateStartUpSchema,
    PlainStartUpDocSchema,
    PlainUpdateStartUpDocSchema,
)

blp = Blueprint(
    "BusinessStartUp", __name__, description="Operations on BusinessStartUp"
)


@blp.route("/business-startup")
class BusinessStartUp(MethodView):

    @blp.arguments(StartUpSchema)
    @blp.response(201, PlainStartUpSchema)
    # @jwt_required()
    def post(self, businessData):
        businessData["password"] = pbkdf2_sha256.hash(businessData["password"])
        user = BusinessStartUpModel(id=f"{uuid.uuid4()}", **businessData)
        try:
            user.save_to_db()
            return user
        except:
            abort(500, message="an occurred while saving user")

    @blp.response(200, PlainStartUpSchema(many=True))
    @jwt_required()
    def get(self):
        try:
            startUp = BusinessStartUpModel.query.all()
            return startUp
        except:
            abort(500, message="an occurred while saving user")


@blp.route("/business-startup/update-status/<string:userId>")
class UpdateBusinessStartUpStatus(MethodView):

    @blp.response(201, PlainStartUpSchema)
    @jwt_required()
    def patch(self, userId):
        try:
            user = BusinessStartUpModel.find_by_id(userId)
            user.isActive = not user.isActive
            user.save_to_db()
            return user
        except:
            abort(404, message="can not find user")


@blp.route("/business-startup/<string:userId>")
class OneBusinessStartUp(MethodView):

    @blp.response(201, PlainStartUpSchema)
    @jwt_required()
    def get(self, userId):
        try:
            user = BusinessStartUpModel.find_by_id(userId)
            return user
        except:
            abort(404, message="can not find user")

    @blp.arguments(PlainUpdateStartUpSchema)
    @blp.response(201, PlainStartUpSchema)
    @jwt_required()
    def patch(self, startUpData, userId):
        try:
            user = BusinessStartUpModel.find_by_id(userId)
            user.phone = startUpData.get("phone", user.phone)
            user.stage = startUpData.get("stage", user.stage)
            user.name = startUpData.get("name", user.name)
            user.profilePic = startUpData.get("profilePic", user.profilePic)
            if startUpData.get("password"):
                user.password = pbkdf2_sha256.hash(startUpData["password"])
                print("password changed")
            user.save_to_db()
            return user
        except:
            abort(404, message="can not find user")


@blp.route("/business-startup/doc/<string:userId>")
class OneBusinessDocument(MethodView):
    @blp.arguments(PlainUpdateStartUpDocSchema)
    @blp.response(201, PlainStartUpDocSchema)
    @jwt_required()
    def patch(self, startUpData, userId):
        try:
            user = BusinessStartUpModel.find_by_id(userId)
            user.document = startUpData.get("document", user.document)
            user.save_to_db()
            return user
        except:
            abort(404, message="can not find user")

    @blp.response(201, PlainStartUpDocSchema)
    @jwt_required()
    def get(self, userId):
        try:
            user = BusinessStartUpModel.find_by_id(userId)
            return user
        except:
            abort(404, message="can not find user")
