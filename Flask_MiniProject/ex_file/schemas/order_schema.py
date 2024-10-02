from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from models import Order
from schemas.user_schema import UserSchema


# Order 모델에 대한 스키마 정의
class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        name = "OrderSchema"

    user = Nested(
        UserSchema,
        exclude=(
            "orders",
            "carts",
        ),
    )
