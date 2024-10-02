from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request, jsonify
from database import db
from models import Order, OrderDetail, Cart
from flask_jwt_extended import jwt_required, get_jwt_identity

order_blp = Blueprint("orders", "orders", url_prefix="/orders/")


@order_blp.route("<int:order_id>", methods=["GET", "POST"])
class OrderList(MethodView):
    @jwt_required()
    def get(self, order_id):  # order_id를 메소드 인자로 추가
        user_id = get_jwt_identity()

        # 주어진 order_id에 해당하는 주문 조회
        order = Order.query.filter_by(id=order_id, user_id=user_id).first_or_404()
        order_details = order.order_details.all()  # 주문 내역 조회

        # 주문 내역 직렬화
        details = [
            {
                "id": detail.id,
                "product_id": detail.product_id,
                "quantity": detail.quantity,
            }
            for detail in order_details
        ]

        # 주문 정보와 주문 내역을 함께 반환
        data = {
            "total_price": order.total_price,
            "is_paid": order.is_paid,
            "order_details": details,  # 주문 내역 추가
        }

        return jsonify(data), 200

    @jwt_required()
    def post(self, order_id):
        user_id = get_jwt_identity()
        data = request.get_json()

        if not data or "order_success" not in data:
            return jsonify({"msg": "주문 데이터가 잘못되었습니다"}), 400

        order = Order.query.get(order_id)

        if data["order_success"]:
            # 주문 성공 로직
            if order and order.user_id == user_id:
                order.is_paid = True
                # 장바구니 비우기
                Cart.query.filter_by(user_id=user_id).delete()
                db.session.commit()
                return jsonify({"msg": "주문이 성공적으로 처리되었습니다"}), 201
            else:
                return jsonify({"msg": "주문을 찾을 수 없습니다"}), 404
        else:
            # 주문 실패 로직
            if order and order.user_id == user_id:
                # 주문 상세 및 주문 삭제
                OrderDetail.query.filter_by(order_id=order_id).delete()
                Order.query.filter_by(id=order_id).delete()
                db.session.commit()
                return jsonify({"msg": "주문 처리에 실패했습니다, 주문이 취소되었습니다"}), 400
            else:
                return jsonify({"msg": "주문을 찾을 수 없습니다"}), 404
