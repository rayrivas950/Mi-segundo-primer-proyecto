from extensions import ma
from marshmallow import fields, validate

class UserRegisterSchema(ma.Schema):
    username = fields.String(required=True, validate=validate.Length(min=4, max=80))
    password = fields.String(required=True, validate=validate.Length(min=8, max=255))
    # Add more complex password validation if needed, e.g., regex for special chars

class UserLoginSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()
