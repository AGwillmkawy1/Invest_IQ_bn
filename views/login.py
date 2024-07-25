from flask_smorest import Blueprint, abort
from flask.views import MethodView
from model import AdminUserModel, InvestorModel, BusinessStartUpModel
from schemas import PlainLoginSchema, PlainLoginResponseSchema
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta

blp = Blueprint('Login', __name__, description='Operations on User login')


@blp.route('/login/admin')
class LoginAdmin(MethodView):

    @blp.arguments(PlainLoginSchema)
    @blp.response(201, PlainLoginResponseSchema)
    def post(self, adminUserData):
        try:
            user = AdminUserModel.find_by_email(adminUserData['email'])
            if not pbkdf2_sha256.verify(adminUserData['password'], user.password) or not user.isActive:
                return abort(401, message='invalid user name or password')

            additional_claims = {'isAdmin': 'admin'}
            tkn = create_access_token(identity=user.email, expires_delta=timedelta(days=1),
                                      additional_claims=additional_claims)

            return {'token': tkn, 'names': user.name, 'email': user.email,
                    'phone': user.phone, 'profilePic': user.profilePic, 'id': user.id}
        except:
            abort(500, message='an error occurred while logging in')


@blp.route('/login/business-startup')
class LoginBusinessStartUp(MethodView):

    @blp.arguments(PlainLoginSchema)
    @blp.response(201, PlainLoginResponseSchema)
    def post(self, doctorData):
        try:
            user = BusinessStartUpModel.find_by_email(doctorData['email'])
            if not pbkdf2_sha256.verify(doctorData['password'], user.password) or not user.isActive:
                return abort(401, message='invalid user name or password')

            additional_claims = {'isAdmin': 'business-startup'}
            tkn = create_access_token(identity=user.email, expires_delta=timedelta(days=1),
                                      additional_claims=additional_claims)

            return {'token': tkn, 'names': user.name, 'email': user.email,
                    'phone': user.phone, 'profilePic': user.profilePic, 'id': user.id}
        except:
            abort(500, message='an error occurred while logging in')


@blp.route('/login/investor')
class LoginInvestor(MethodView):

    @blp.arguments(PlainLoginSchema)
    @blp.response(201, PlainLoginResponseSchema)
    def post(self, doctorData):
        try:
            user = InvestorModel.find_by_email(doctorData['email'])
            if not pbkdf2_sha256.verify(doctorData['password'], user.password) or not user.isActive:
                return abort(401, message='invalid user name or password')

            additional_claims = {'isAdmin': 'investor'}
            tkn = create_access_token(identity=user.email, expires_delta=timedelta(days=1),
                                      additional_claims=additional_claims)

            return {'token': tkn, 'names': f'{user.firstName} {user.lastName}', 'email': user.email,
                    'phone': user.phone, 'profilePic': user.profilePic, 'id': user.id}
        except:
            abort(500, message='an error occurred while logging in')

# @blp.route('/current-user')
# class GetCurrentUser(MethodView):
#
#     @blp.response(200, PlainCurrentUserSchema)
#     @jwt_required()
#     def get(self):
#         try:
#             return {"isAllowed": True}
#         except:
#             abort(500, message='an error occurred while getting currently logged in user')
