from datetime import datetime

from flask_smorest import Blueprint, abort
from flask.views import MethodView
from model import ConversationModel
from schemas import PlainConversationSchema, UpdateStatusConversationSchema
from flask_jwt_extended import jwt_required

from views.usersEvent import handle_add_message

blp = Blueprint("Conversations", __name__, description="Operations on Conversations")


@blp.route("/conversation")
class Conversation(MethodView):

    @blp.arguments(PlainConversationSchema)
    @blp.response(201, PlainConversationSchema)
    @jwt_required()
    def post(self, conversation_data):
        try:
            conversation_data['senderId'] = str(conversation_data['senderId'])
            conversation_data['receiverId'] = str(conversation_data['receiverId'])
            conversation = ConversationModel(**conversation_data)
            conversation.createdAt = datetime.now()
            conversation.save_to_db()
            handle_add_message(conversation.receiverId)
            return conversation
        except:
            abort(500, message="an occurred while saving conversation")

    @blp.response(200, PlainConversationSchema(many=True))
    @jwt_required()
    def get(self):
        try:
            conversations = ConversationModel.query.all()
            return conversations
        except:
            abort(500, message="an occurred while fetching conversation")


@blp.route("/conversation/<string:id>")
class OneConversation(MethodView):

    @blp.response(200, PlainConversationSchema)
    @jwt_required()
    def get(self, id):
        try:
            conversation = ConversationModel.find_by_id(id)
            return conversation
        except:
            abort(404, message="can not find conversation")

    @blp.arguments(UpdateStatusConversationSchema)
    @blp.response(201, PlainConversationSchema)
    @jwt_required()
    def patch(self, conversation_data, id):
        try:
            conversation = ConversationModel.find_by_id(id)
            conversation.isRead = conversation_data["isRead"]
            conversation.save_to_db()
            return conversation
        except:
            abort(500, message="an occurred while updating conversation")
