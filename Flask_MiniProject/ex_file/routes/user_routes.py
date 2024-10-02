from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request, jsonify
from werkzeug.security import generate_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt,
    get_jwt_identity,
)
from models import User, db
from blocklist import BLOCKLIST
from schemas import user_schema

# 사용자 관련 라우트를 정의하는 블루프린트 생성
user_blp = Blueprint("users", "users", url_prefix="/users/", description="사용자 관리")


# 회원가입을 처리하는 클래스
@user_blp.route("/register/", methods=["POST"])
class Register(MethodView):
    @user_blp.arguments(user_schema.RegisterSchema)
    def post(self, args):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        # 유저네임 또는 비밀번호가 누락된 경우
        if not username or not password:
            return jsonify({"msg": "Missing username or password"}), 400

        # 이미 존재하는 유저네임인 경우
        if User.query.filter_by(username=username).first():
            return jsonify({"msg": "Username already exists"}), 409

        # 비밀번호 해싱 및 유저 생성
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # 회원가입 성공 메시지 반환
        return jsonify({"msg": "유저가 생성되었습니다."}), 201


# 로그인을 처리하는 클래스
@user_blp.route("/login/", methods=["POST"])
class Login(MethodView):
    @user_blp.arguments(user_schema.LoginSchema)
    def post(self, args):
        # 파싱된 데이터 사용
        username = args.get("username")
        password = args.get("password")

        # 유저네임 또는 비밀번호가 누락된 경우
        if not username or not password:
            return jsonify({"msg": "Missing username or password"}), 400

        # 유저 검증 및 토큰 생성
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            access_token = create_access_token(identity=user.id, fresh=False)
            return jsonify(access_token=access_token), 200
        else:
            # 잘못된 로그인 정보
            return jsonify({"msg": "아이디나 비밀번호가 틀렸습니다."}), 401


# 로그아웃을 처리하는 클래스
@user_blp.route("/logout/", methods=["POST"])
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return jsonify({"msg": "로그아웃 되었습니다."}), 200


# 회원 탈퇴를 처리하는 클래스
@user_blp.route("/delete-account/", methods=["DELETE"])
class DeleteAccount(MethodView):
    @jwt_required()
    def delete(self):
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(id=current_user_id).first()

        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"msg": "계정 삭제가 완료 되었습니다."}), 200
        else:
            return jsonify({"msg": "유저를 찾을수 없습니다"}), 404


# 마이페이지 정보를 보여주는 클래스
@user_blp.route("/my-page/", methods=["GET"])
class MyPage(MethodView):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(id=current_user_id).first()

        if user:
            return jsonify(username=user.username), 200
        else:
            return jsonify({"msg": "유저를 찾을수 없습니다."}), 404
