from db import db


class BusinessStartUpModel(db.Model):
    __tablename__ = 'business_startup'

    id = db.Column(db.String(150), primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    profilePic = db.Column(db.String(100), nullable=True)
    stage = db.Column(db.String(150), nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    location = db.Column(db.String(150), nullable=True)
    businessType = db.Column(db.String(150), nullable=True)
    growthRate = db.Column(db.Float, nullable=True)
    cost = db.Column(db.Float, nullable=True)
    capital = db.Column(db.Float, nullable=True)
    document = db.Column(db.String(150), nullable=True)

    business_investments = db.relationship('BusinessInvestmentModel', back_populates='business_startup', lazy="dynamic")

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, businessId: str) -> "BusinessStartUpModel":
        return cls.query.get_or_404(businessId)

    @classmethod
    def find_by_email(cls, email: str) -> "BusinessStartUpModel":
        applicant = cls.query.filter_by(email=email).first()
        if applicant:
            return applicant
        raise Exception(f"startup with email {email} not found")
