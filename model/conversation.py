from db import db


class ConversationModel(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    senderId = db.Column(db.String(90), nullable=False)
    receiverId = db.Column(db.String(90), nullable=False)
    isRead = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime, nullable=False)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, conversationId: int) -> "ConversationModel":
        return cls.query.get_or_404(conversationId)
