from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys
import time

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

# 리뷰 등록 처리 (DB에 저장 후 결과 페이지로 이동)
@application.route("/submit_review_post", methods=['POST'])
def submit_review_post():
    form = request.form.to_dict()

    reviewer_id = form.get("reviewer_id", "").strip()
    item_name = form.get("item_name", "").strip()
    title = form.get("title", "").strip()
    content = form.get("content", "").strip()
    rating_raw = form.get("rating", "").strip()

    # 간단한 유효성 검사 
    if not title:
        flash("리뷰 제목 입력은 필수입니다.", "error")
        return redirect(url_for("reg_reviews"))
    if len(content) < 20:
        flash("리뷰 내용은 20자 이상 입력해주세요.", "error")
        return redirect(url_for("reg_reviews"))
    if not rating_raw:
        flash("별점을 선택해주세요.", "error")
        return redirect(url_for("reg_reviews"))

    try:
        rating = int(rating_raw)
    except ValueError:
        flash("별점 값이 올바르지 않습니다.", "error")
        return redirect(url_for("reg_reviews"))

    # 이미지 처리
    img_path = None
    image_file = request.files.get("image")
    if image_file and image_file.filename:
        save_path = f"static/image/{image_file.filename}"
        image_file.save(save_path)
        img_path = save_path

    # 리뷰 객체 생성 (DBhandler.insert_review과 호환되게)
    review = {
        "item_name": item_name,
        "reviewer_id": reviewer_id,
        "title": title,
        "content": content,
        "rating": rating,
        "img_path": img_path,
        "created_at": int(time.time())
    }

    # DB에 저장 (database.DBhandler.insert_review 사용)
    review_id = DB.insert_review(review)

    # 저장된 리뷰의 ID로 결과 페이지로 이동 (네가 만들어둔 review_result 라우트 사용)
    return redirect(url_for("review_result", review_id=review_id))


# 리뷰 등록 결과
@application.route("/review_result/<review_id>")
def review_result(review_id):
    review = DB.db.child("review").child(review_id).get().val()
    if not review:
        return "리뷰를 찾을 수 없습니다.", 404
    return render_template("submit_review_result.html", review=review)


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

# 회원가입 처리
@application.route("/signup_post", methods = ['POST'])
def register_user():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    nickname = data.get('nickname')
    email = data.get('email')
    phone = data.get('phone')
    student_id = data.get('student_id')

    if not username or not password or not nickname or not email or not phone or not student_id:
        flash("아이디/비밀번호/닉네임은 필수입니다.")
        return redirect(url_for("signup"))

    pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    normalized = {
        "username": username,
        "nickname": nickname,
        "email": email,
        "phone": phone,
        "student_id": student_id,
    }
    
    if DB.insert_user(normalized, pw_hash):
        flash("success! now log in")
        return render_template("login.html")
    else:
        flash("user id already exist!")
        return render_template("signup.html")

# ------------------------
# Flask 실행
# ------------------------

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, debug=True)
