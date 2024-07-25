from db import db


class BusinessInvestmentModel(db.Model):
    __tablename__ = 'business_investment'

    id = db.Column(db.String(150), primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    ROI = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.Date, nullable=False)
    businessId = db.Column(db.String(150), db.ForeignKey('business_startup.id'), nullable=False)
    investorId = db.Column(db.String(150), db.ForeignKey('investor.id'), nullable=False)
    startCost = db.Column(db.Float, nullable=False)
    endCost = db.Column(db.Float, nullable=False)
    numberOfDays = db.Column(db.Integer, nullable=False)

    business_startup = db.relationship('BusinessStartUpModel', back_populates='business_investments')
    investor = db.relationship('InvestorModel', back_populates='investments')

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, investId: int) -> "BusinessInvestmentModel":
        return cls.query.get_or_404(investId)
