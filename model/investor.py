from db import db


class InvestorModel(db.Model):
    __tablename__ = 'investor'

    id = db.Column(db.String(150), primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    firstName = db.Column(db.String(30), nullable=False)
    lastName = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    profilePic = db.Column(db.String(100), nullable=True)
    isActive = db.Column(db.Boolean, default=True)

    investments = db.relationship('BusinessInvestmentModel', back_populates='investor', lazy="dynamic")

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, investorId: int) -> "InvestorModel":
        return cls.query.get_or_404(investorId)

    @classmethod
    def find_by_email(cls, email: str) -> "InvestorModel":
        applicant = cls.query.filter_by(email=email).first()
        if applicant:
            return applicant
        raise Exception(f"investor with email {email} not found")
