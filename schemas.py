from marshmallow import fields, Schema


class PlainLoginSchema(Schema):
    email = fields.Email(required=True, load_only=True)
    password = fields.Str(required=True, load_only=True)


class PlainLoginResponseSchema(Schema):
    id = fields.UUID(required=True)
    token = fields.UUID(required=True)
    names = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    profilePic = fields.Str()


class AdminUserSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    phone = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    profilePic = fields.Str()


class PlainAdminUserSchema(AdminUserSchema):
    id = fields.UUID(required=True)
    isActive = fields.Bool(required=True)


class PlainUpdateAdminUserSchema(Schema):
    firstName = fields.Str()
    lastName = fields.Str()
    phone = fields.Str()
    password = fields.Str()
    profilePic = fields.Str()


class InvestorSchema(Schema):
    email = fields.Email(required=True)
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    phone = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    profilePic = fields.Str()


class PlainUpdateInvestorSchema(Schema):
    email = fields.Email()
    firstName = fields.Str()
    lastName = fields.Str()
    phone = fields.Str()
    password = fields.Str(load_only=True)
    profilePic = fields.Str()


class PlainInvestorSchema(InvestorSchema):
    id = fields.UUID(required=True)
    isActive = fields.Bool(required=True)


class StartUpSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    stage = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    profilePic = fields.Str()
    location = fields.Str()
    businessType = fields.Str()
    growthRate = fields.Float()
    cost = fields.Float()
    capital = fields.Float()


class PlainStartUpSchema(StartUpSchema):
    id = fields.UUID(required=True)
    isActive = fields.Bool(required=True)


class PlainUpdateStartUpSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    phone = fields.Str()
    stage = fields.Str()
    password = fields.Str(load_only=True)
    profilePic = fields.Str()


class PlainStartUpDocSchema(Schema):
    document = fields.Str()


class PlainUpdateStartUpDocSchema(Schema):
    document = fields.Str(required=True)


class PlainReturnOnInvestment(Schema):
    numberOfDays = fields.Int(required=True)
    amount = fields.Float(required=True)
    startUpId = fields.UUID(required=True)


class PlainReturnOnInvestmentResponse(PlainReturnOnInvestment):
    ROI = fields.Float(required=True)


class BusinessInvestmentSchema(Schema):
    investorId = fields.UUID(required=True)
    businessId = fields.UUID(required=True)
    amount = fields.Float(required=True)
    startCost = fields.Float(required=True)
    endCost = fields.Float(required=True)
    numberOfDays = fields.Int(required=True)
    ROI = fields.Float(required=True)


class PlainBusinessInvestmentSchema(BusinessInvestmentSchema):
    id = fields.UUID(required=True)
    created_at = fields.Date(required=True)


class PlainConversationSchema(Schema):
    id = fields.Int(dump_only=True)
    message = fields.Str(required=True)
    senderId = fields.UUID(required=True)
    receiverId = fields.UUID(required=True)
    isRead = fields.Bool(dump_only=True)
    createdAt = fields.DateTime(dump_only=True)


class UpdateStatusConversationSchema(Schema):
    isRead = fields.Bool(required=True)


class PlainInsightSchema(Schema):
    documentLink = fields.Str(required=True)


class RowInvestorSchema(Schema):
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    profilePic = fields.Str(required=True)


class RowBusinessSchema(Schema):
    name = fields.Str(required=True)
    profilePic = fields.Str(required=True)


class PlainInvestorBusinessSchema(Schema):
    amount = fields.Float(dump_only=True)
    created_at = fields.Date(dump_only=True)
    business_startup = fields.Nested(RowBusinessSchema,dump_only=True)
    investor = fields.Nested(RowInvestorSchema,dump_only=True)
