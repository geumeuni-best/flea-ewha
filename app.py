from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"
DB = DBhandler()

# 홈 
@application.route("/")
def home():
    return render_template("index.html")

# 상품 조회
@application.route("/list")
def view_list():
    return render_template("list.html")

# 리뷰 조회
@application.route("/review")
def view_review():
    return render_template("review.html")

# 상품 등록
@application.route("/reg_items")
def reg_items():
    return render_template("reg_items.html")

# 상품 등록 처리
@application.route("/submit_item")
def reg_item_submit():
    seller_id = request.args.get("seller_id")
    name = request.args.get("name")
    price = request.args.get("price")
    region = request.args.get("region")
    description = request.args.get("description")

    print(seller_id, name, price, region, description)
    return render_template("submit_item_result.html")

# 이미지 업로드
@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    image_file = request.files["image"]
    image_file.save("static/image/{}".format(image_file.filename))
    data = request.form
    DB.insert_item(data['name'], data, image_file.filename)
    return render_template("submit_item_result.html", data = data, img_path = "static/image/{}".format(image_file.filename))

# 리뷰 등록
@application.route("/reg_reviews")
def reg_reviews():
    return render_template("reg_reviews.html")

# 판매 요청
@application.route("/reg_requests")
def reg_requests():
    return render_template("reg_requests.html")

# 마이페이지
@application.route("/mypage")
def mypage():
    return render_template("mypage.html")

# 판매 요청 조회 페이지 (request.html)
@application.route("/request")
def request_page():
    return render_template("request.html")

# 로그인
@application.route("/login")
def login():
    return render_template("login.html")

# 회원가입
@application.route("/signup")
def signup():
    return render_template("signup.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0')
