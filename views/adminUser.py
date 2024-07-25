from flask_smorest import Blueprint, abort
from flask.views import MethodView
from model import AdminUserModel
from schemas import PlainAdminUserSchema, PlainUpdateAdminUserSchema, AdminUserSchema
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import jwt_required
import uuid_utils as uuid

blp = Blueprint('AdminUser', __name__, description='Operations on AdminUser')


@blp.route('/admin-user')
class AdminUser(MethodView):

    @blp.arguments(AdminUserSchema)
    @blp.response(201, PlainAdminUserSchema)
    @jwt_required()
    def post(self, adminUserData):
        adminUserData['password'] = pbkdf2_sha256.hash(adminUserData['password'])
        user = AdminUserModel(id=f"{uuid.uuid4()}", **adminUserData)
        try:
            user.save_to_db()
            return user
        except:
            abort(500, message='an occurred while saving user')

    @blp.response(200, PlainAdminUserSchema(many=True))
    @jwt_required()
    def get(self):
        try:
            adminUsers = AdminUserModel.query.all()
            return adminUsers
        except:
            abort(500, message='an occurred while saving user')


@blp.route('/admin-user/update-status/<string:userId>')
class UpdateAdminUserStatus(MethodView):

    @blp.response(201, PlainAdminUserSchema)
    @jwt_required()
    def patch(self, userId):
        try:
            user = AdminUserModel.find_by_id(userId)
            user.isActive = not user.isActive
            user.save_to_db()
            return user
        except:
            abort(404, message='can not find user')


@blp.route('/admin-user/<string:userId>')
class OneAdminUser(MethodView):

    @blp.response(201, PlainAdminUserSchema)
    @jwt_required()
    def get(self, userId):
        try:
            user = AdminUserModel.find_by_id(userId)
            return user
        except:
            abort(404, message='can not find user')

    @blp.arguments(PlainUpdateAdminUserSchema)
    @blp.response(201, PlainAdminUserSchema)
    @jwt_required()
    def patch(self, adminData, userId):
        try:
            user = AdminUserModel.find_by_id(userId)
            user.name = adminData.get('name', user.name)
            user.phone = adminData.get('phone', user.phone)
            user.profilePic = adminData.get('profilePic', user.profilePic)
            if adminData.get('password'):
                user.password = pbkdf2_sha256.hash(adminData['password'])
                print('password changed')
            user.save_to_db()
            return user
        except:
            abort(404, message='can not find user')
