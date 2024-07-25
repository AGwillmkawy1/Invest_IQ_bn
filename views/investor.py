from flask_smorest import Blueprint, abort
from flask.views import MethodView
from model import InvestorModel
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import jwt_required
import uuid_utils as uuid

from schemas import InvestorSchema, PlainInvestorSchema, PlainUpdateInvestorSchema

blp = Blueprint('Investor', __name__, description='Operations on Investor')


@blp.route('/investor')
class Investor(MethodView):

    @blp.arguments(InvestorSchema)
    @blp.response(201, PlainInvestorSchema)
    @jwt_required()
    def post(self, investorData):
        investorData['password'] = pbkdf2_sha256.hash(investorData['password'])
        user = InvestorModel(id=f"{uuid.uuid4()}", **investorData)
        try:
            user.save_to_db()
            return user
        except:
            abort(500, message='an occurred while saving user')

    @blp.response(200, PlainInvestorSchema(many=True))
    @jwt_required()
    def get(self):
        try:
            investor = InvestorModel.query.all()
            return investor
        except:
            abort(500, message='an occurred while saving user')


@blp.route('/investor/update-status/<string:userId>')
class UpdateBusinessStartUpStatus(MethodView):

    @blp.response(201, PlainInvestorSchema)
    @jwt_required()
    def patch(self, userId):
        try:
            user = InvestorModel.find_by_id(userId)
            user.isActive = not user.isActive
            user.save_to_db()
            return user
        except:
            abort(404, message='can not find user')


@blp.route('/investor/<string:userId>')
class OneBusinessStartUp(MethodView):

    @blp.response(201, PlainInvestorSchema)
    @jwt_required()
    def get(self, userId):
        try:
            user = InvestorModel.find_by_id(userId)
            return user
        except:
            abort(404, message='can not find user')

    @blp.arguments(PlainUpdateInvestorSchema)
    @blp.response(201, PlainInvestorSchema)
    @jwt_required()
    def patch(self, investorData, userId):
        try:
            user = InvestorModel.find_by_id(userId)
            user.phone = investorData.get('phone', user.phone)
            user.stage = investorData.get('stage', user.stage)
            user.firstName = investorData.get('firstName', user.firstName)
            user.lastName = investorData.get('lastName', user.lastName)
            user.profilePic = investorData.get('profilePic', user.profilePic)
            if investorData.get('password'):
                user.password = pbkdf2_sha256.hash(investorData['password'])
                print('password changed')
            user.save_to_db()
            return user
        except:
            abort(404, message='can not find user')
