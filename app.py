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
    nickname = session.get("nickname", "")
    return render_template("reg_requests.html", nickname=nickname)

@application.route("/submit_request_post", methods=['POST'])
def submit_request_post():
    data = request.form

    selected_item_name = data.get("selected_item", "")
    item_info = {}

    if selected_item_name:
        item_info = DB.get_item_by_name(selected_item_name) or {}
        item_info["name"] = selected_item_name

    request_info = {
        "search": data.get("search", ""),
        "nickname": data.get("nickname", ""),
        "title": data.get("title", ""),
        "content": data.get("content", ""),
        "item": item_info,
    }

    DB.insert_request(request_info)
    return render_template("submit_request_result.html", req=request_info)


@application.route("/request/<request_id>")
def request_detail(request_id):
    req_data = DB.get_request_by_id(request_id)
    if not req_data:
        return "해당 요청을 찾을 수 없습니다.", 404
    return render_template("submit_request_result.html", req=req_data)


@application.route("/api/items")
def api_items():
    # DB에서 전체 상품 리스트 가져오기
    items = DB.get_item_names()
    return {"items": items}

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

@application.route("/login_confirm", methods=['POST'])
def login_user():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if DB.find_user(username, password_hash):
        user = DB.get_user_by_username(username)
        session['id'] = username
        session['nickname'] = user['nickname']
        return redirect(url_for('home'))
    else: 
        flash("Wrong ID or PW!")
        return render_template("login.html")

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
