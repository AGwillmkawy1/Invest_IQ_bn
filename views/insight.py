from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from docquery import document, pipeline

from schemas import PlainInsightSchema

nlp = pipeline('document-question-answering')

blp = Blueprint('Insight', __name__, description='Operations on Insight')


@blp.route('/insight')
class Insight(MethodView):

    @blp.arguments(PlainInsightSchema)
    @blp.response(200)
    @jwt_required()
    def get(self, insightData):
        try:
            doc = document.load_document(insightData['documentLink'])
            result = nlp(question="What is the total amount?", **doc.context)
            return result[0]['answer']
        except:
            abort(500, message='an occurred while searching for insight')
