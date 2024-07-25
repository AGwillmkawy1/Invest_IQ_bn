from db import db


class AdminUserModel(db.Model):
    __tablename__ = 'administration_user'

    id = db.Column(db.String(150), primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    profilePic = db.Column(db.String(100), nullable=True)
    isActive = db.Column(db.Boolean, default=True)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, adminId: int) -> "AdminUserModel":
        return cls.query.get_or_404(adminId)

    @classmethod
    def find_by_email(cls, email: str) -> "AdminUserModel":
        applicant = cls.query.filter_by(email=email).first()
        if applicant:
            return applicant
        raise Exception(f"admin with email {email} not found")
