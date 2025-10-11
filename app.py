from flask import Flask, render_template
import sys

application = Flask(__name__)

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