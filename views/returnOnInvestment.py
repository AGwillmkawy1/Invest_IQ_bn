from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from model import BusinessStartUpModel
from joblib import load
from schemas import PlainReturnOnInvestment, PlainReturnOnInvestmentResponse

roiModel = load('trainedModel/roiModel.joblib')


blp = Blueprint('ROI', __name__, description='Operations on ROI')


@blp.route('/calculate-roi')
class ReturnOnInvestment(MethodView):

    @blp.arguments(PlainReturnOnInvestment)
    @blp.response(201, PlainReturnOnInvestmentResponse)
    @jwt_required()
    def post(self, roiData):
        try:
            startup = BusinessStartUpModel.find_by_id(str(roiData['startUpId']))
            endCost = (startup.growthRate * roiData['amount']) + roiData['amount']
            labels = [[roiData['amount'], startup.growthRate, endCost, roiData['numberOfDays']]]
            predicted = roiModel.predict(labels)
            roiData['ROI'] = float(predicted[0])
            return roiData
        except:
            abort(500, message='an occurred while calculating ROI')
