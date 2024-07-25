from model import BusinessInvestmentModel
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
import uuid_utils as uuid
from datetime import date

from schemas import BusinessInvestmentSchema,PlainBusinessInvestmentSchema

blp = Blueprint('Business-Investment', __name__, description='Operations on Business-Investment')


@blp.route('/business-investment')
class BusinessInvestment(MethodView):

    @blp.arguments(BusinessInvestmentSchema)
    @blp.response(201, PlainBusinessInvestmentSchema)
    @jwt_required()
    def post(self, biData):
        biData['businessId'] = str(biData['businessId'])
        biData['investorId'] = str(biData['investorId'])
        bi = BusinessInvestmentModel(id=f"{uuid.uuid4()}", **biData)
        bi.created_at = date.today()
        try:
            bi.save_to_db()
            return bi
        except:
            abort(500, message='an occurred while saving Business Investment')

    @blp.response(200, PlainBusinessInvestmentSchema(many=True))
    @jwt_required()
    def get(self):
        try:
            bi = BusinessInvestmentModel.query.all()
            return bi
        except:
            abort(500, message='an occurred while getting Business Investment')


@blp.route('/business-investment/<string:id>')
class OneBusinessInvestment(MethodView):

    @blp.response(201, PlainBusinessInvestmentSchema)
    @jwt_required()
    def get(self, id):
        try:
            bi = BusinessInvestmentModel.find_by_id(id)
            return bi
        except:
            abort(404, message='can not find item')
