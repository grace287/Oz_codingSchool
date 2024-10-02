from flask_smorest import Blueprint
from flask.views import MethodView
from schemas.product_schema import (
    ProductSchema,
    AddToCartSchema,
    AddProductSchema,
    ResponseMessageSchema,
)
from flask import request, jsonify
from models import Product
from models import Cart, db
from flask_jwt_extended import jwt_required, get_jwt_identity


product_blp = Blueprint(
    "products", "products", url_prefix="/products/", description="상품 관리"
)


@product_blp.route("list/", methods=["GET"])
class ProductList(MethodView):
    def get(self, *args):
        page = request.args.get("page", 1, type=int)
        per_page = 20
        paginated_products = Product.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False,
        )
        products = paginated_products.items

        # Product 객체들을 JSON 형식으로 직렬화
        product_schema = ProductSchema(many=True)
        products_json = product_schema.dump(products)

        # 페이징 정보 포함
        pagination_info = {
            "total": paginated_products.total,
            "pages": paginated_products.pages,
            "page": page,
            "per_page": per_page
        }

        return {"products": products_json, "pagination": pagination_info}, 200



@product_blp.route("list/<int:product_id>/", methods=["GET"])
class ProductDetail(MethodView):
    @product_blp.response(200, ProductSchema())
    def get(self, product_id):
        product = Product.query.get_or_404(product_id)
        return product


@product_blp.route("add/", methods=["POST"])
class AddProduct(MethodView):
    @product_blp.arguments(AddProductSchema)
    @product_blp.response(201, ResponseMessageSchema)
    def post(self, args):
        name = args.get("name")
        price = args.get("price")
        description = args.get("description")

        # 새 상품 객체 생성
        new_product = Product(
            name=name,
            price=price,
            description=description,
        )
        db.session.add(new_product)
        db.session.commit()

        return (
            jsonify(
                {
                    "msg": "성공적으로 추가되었습니다",
                    "product_id": new_product.id,
                }
            ),
            201,
        )


@product_blp.route("add-to-cart/", methods=["POST"])
class AddToCart(MethodView):
    @jwt_required()
    @product_blp.arguments(AddToCartSchema)
    @product_blp.response(200, ResponseMessageSchema)
    def post(self, args):
        user_id = get_jwt_identity()
        product_id = args.get("product_id")
        quantity = args.get("quantity")

        # 장바구니에서 동일한 product_id의 상품 찾기
        existing_cart_item = Cart.query.filter_by(
            user_id=user_id,
            product_id=product_id,
        ).first()

        if existing_cart_item:
            # 이미 상품이 장바구니에 있으면 수량 업데이트
            existing_cart_item.quantity += quantity
        else:
            # 새 상품을 장바구니에 추가
            new_cart_item = Cart(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity,
            )
            db.session.add(new_cart_item)

        db.session.commit()

        return jsonify({"msg": "장바구니에 상품이 추가되었습니다"}), 200
