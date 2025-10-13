from flask import Flask, render_template, request
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

# 상품 등록 처리
@application.route("/submit_item")
def reg_item_submit():
    name=request.args.get("name")
    seller=request.args.get("seller")
    addr=request.args.get("addr")
    email=request.args.get("email")
    category=request.args.get("category")
    card=request.args.get("card")
    status=request.args.get("status")
    phone=request.args.get("phone")

    print(name, seller, addr, email, category, card, status, phone)
    #return render_template("reg_item.html")

# 이미지 업로드
@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    image_file=request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    data=request.form
    return render_template("submit_item_result.html", data=data, img_path="static/image/{}".format(image_file.filename))

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
