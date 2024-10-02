from flask_smorest import Blueprint
from flask.views import MethodView
from flask import jsonify, request
from database import db
from models import Order, Cart, OrderDetail
from flask_jwt_extended import jwt_required, get_jwt_identity

cart_blp = Blueprint("carts", "carts", url_prefix="/carts/", description="장바구니 관리")


@cart_blp.route("", methods=["GET", "POST"])
class CreateOrder(MethodView):
    @jwt_required()
    def get(self):
        carts = Cart.query.filter_by(user_id=get_jwt_identity()).all()
        # Cart 객체를 직렬화 가능한 형태로 변환하여 반환
        serialized_carts = [
            {
                "product_id": cart.product_id,
                "quantity": cart.quantity,
            }
            for cart in carts
        ]
        return jsonify(serialized_carts)

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        # 장바구니 아이템 조회
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        if not cart_items:
            return jsonify({"msg": "장바구니가 비어 있습니다"}), 400

        # 주문 객체 생성 및 총 가격 계산
        order = Order(
            user_id=user_id,
            total_price=0,
            is_paid=False,
        )
        db.session.add(order)
        db.session.flush()  # order 객체에 ID 할당

        # 주문 상세 생성
        for item in cart_items:
            order_detail = OrderDetail(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
            )
            db.session.add(order_detail)
            order.total_price += item.product.price * item.quantity

        db.session.commit()
        return jsonify({"msg": "주문이 성공적으로 처리되었습니다", "order_id": order.id}), 201


@cart_blp.route("<int:product_id>/", methods=["PUT", "DELETE"])
class CartManagement(MethodView):
    @jwt_required()
    def put(self, product_id):
        data = request.get_json()
        new_quantity = data.get("quantity")
        cart_item = Cart.query.filter_by(
            user_id=get_jwt_identity(), product_id=product_id
        ).first()
        if not cart_item:
            return jsonify({"msg": "해당 상품이 장바구니에 없습니다"}), 400
        cart_item.quantity = new_quantity
        db.session.commit()
        return jsonify({"msg": "장바구니가 업데이트되었습니다"}), 200

    @jwt_required()
    def delete(self, product_id):
        cart_item = Cart.query.filter_by(
            user_id=get_jwt_identity(), product_id=product_id
        ).first()
        if cart_item.user_id != get_jwt_identity():
            return jsonify({"msg": "권한이 없습니다"}), 403

        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"msg": "장바구니 아이템이 삭제되었습니다"}), 200
