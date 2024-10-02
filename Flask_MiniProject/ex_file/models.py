from werkzeug.security import generate_password_hash, check_password_hash
from database import db


# Product 모델 정의
class Product(db.Model):
    __tablename__ = "product"

    # 상품 ID, 기본 키로 설정
    id = db.Column(db.Integer, primary_key=True)
    # 상품명
    name = db.Column(db.String(81), nullable=False)
    # 상품 가격
    price = db.Column(db.Float, nullable=False)
    # 상품 설명
    description = db.Column(db.String(200))

    # 관계 설정
    carts = db.relationship("Cart", back_populates="product", lazy="dynamic")
    order_details = db.relationship(
        "OrderDetail", back_populates="product", lazy="dynamic"
    )


# Cart 모델 정의
class Cart(db.Model):
    __tablename__ = "cart"

    # 장바구니 ID, 기본 키로 설정
    id = db.Column(db.Integer, primary_key=True)
    # 사용자 ID, 외래 키
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 상품 ID, 외래 키
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    # 수량
    quantity = db.Column(db.Integer, nullable=False)

    # 관계 설정
    user = db.relationship("User", back_populates="carts", lazy="select")
    product = db.relationship("Product", back_populates="carts", lazy="select")


# Order 모델 정의
class Order(db.Model):
    __tablename__ = "order"

    # 주문 ID, 기본 키로 설정
    id = db.Column(db.Integer, primary_key=True)
    # 사용자 ID, 외래 키
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 총 가격
    total_price = db.Column(db.Float, nullable=False)
    # 결제 여부, 기본값은 False
    is_paid = db.Column(db.Boolean, default=False, nullable=False)

    # 관계 설정
    user = db.relationship("User", back_populates="orders", lazy="select")
    order_details = db.relationship(
        "OrderDetail", back_populates="order", lazy="dynamic"
    )


# OrderDetail 모델 정의
class OrderDetail(db.Model):
    __tablename__ = "order_detail"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, nullable=False)

    # 관계 설정
    order = db.relationship("Order", back_populates="order_details", lazy="select")
    product = db.relationship("Product", back_populates="order_details", lazy="select")


# User 모델 정의
class User(db.Model):
    __tablename__ = "user"

    # 사용자 ID, 기본 키로 설정
    id = db.Column(db.Integer, primary_key=True)
    # 사용자 이름
    username = db.Column(db.String(80), unique=True, nullable=False)
    # 비밀번호 해시
    password_hash = db.Column(db.String(255), nullable=False)

    # 비밀번호 속성 (읽기 전용)
    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    # 비밀번호 설정자 (해시 생성)
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 비밀번호 검증 메서드
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 관계 설정
    carts = db.relationship("Cart", back_populates="user", lazy="dynamic")
    orders = db.relationship("Order", back_populates="user", lazy="dynamic")
