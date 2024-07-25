from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from sqlalchemy import func
import pandas as pd

from model import BusinessStartUpModel, BusinessInvestmentModel
from schemas import PlainInvestorBusinessSchema

blp = Blueprint('Trends', __name__, description='Operations on Trends')


@blp.route('/trends/location')
class LocationTrends(MethodView):

    @blp.response(200)
    @jwt_required()
    def get(self):
        try:
            results = BusinessStartUpModel.query.with_entities(
                BusinessStartUpModel.location,
                func.group_concat(BusinessStartUpModel.name).label('startup_names')
            ).group_by(BusinessStartUpModel.location).all()
            locations = [{'location': result.location, 'startup_names': result.startup_names.split(',')} for result in
                         results]
            return locations
        except:
            abort(500, message='an occurred while calculating ROI')


@blp.route('/trends/business-type')
class BusinessTypeTrends(MethodView):

    @blp.response(200)
    @jwt_required()
    def get(self):
        try:
            results = BusinessInvestmentModel.query.all()
            businessTypes = [{'businessType': result.business_startup.businessType, 'amount': result.amount} for result
                             in
                             results]
            df = pd.DataFrame(businessTypes)
            grouped_df = df.groupby('businessType')['amount'].sum().reset_index()
            return grouped_df.to_dict(orient='records')
        except:
            abort(500, message='an occurred while calculating ROI')


@blp.route('/trends/start-up')
class StartUpTrends(MethodView):

    @blp.response(200)
    @jwt_required()
    def get(self):
        try:
            results = BusinessInvestmentModel.query.all()
            businessNames = [{'businessName': result.business_startup.name, 'amount': result.amount} for result
                             in
                             results]
            df = pd.DataFrame(businessNames)
            grouped_df = df.groupby('businessName')['amount'].sum().reset_index()
            return grouped_df.to_dict(orient='records')
        except:
            abort(500, message='an occurred while calculating ROI')


@blp.route('/trends/investor-business')
class InvestorBusiness(MethodView):

    @blp.response(200, PlainInvestorBusinessSchema(many=True))
    @jwt_required()
    def get(self):
        try:
            results = BusinessInvestmentModel.query.all()
            return results
        except:
            abort(500, message='an occurred while calculating ROI')
