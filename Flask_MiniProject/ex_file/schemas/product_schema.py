# schemas/product_schema.py
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from models import Product
from schemas.cart_schema import CartSchema
from marshmallow import Schema, fields


# Product 모델에 대한 스키마 정의
class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        name = "ProductSchema"

    carts = Nested(CartSchema, many=True, exclude=("product",))


class AddProductSchema(Schema):
    name = fields.String(required=True)
    price = fields.Float(required=True)
    description = fields.String(required=False)
    # 필요한 다른 필드들 추가


class AddToCartSchema(Schema):
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(missing=1)





# 응답 메시지 스키마
class ResponseMessageSchema(Schema):
    msg = fields.String(required=True)


# 에러 응답 스키마
class ErrorResponseSchema(Schema):
    error = fields.String(required=True)
    message = fields.String(required=True)
