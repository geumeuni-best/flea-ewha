from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
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
    items = DB.get_items()
    latest_items = list(items.items())[:4]
    return render_template("index.html", latest_items=latest_items)

# 상품 조회
@application.route("/list")
def view_list():
    page = request.args.get("page",0,type=int)
    per_page=8  # 2 by 4로 수정
    per_row=4
    row_count = int(per_page/per_row)
    start_idx = per_page * page
    end_idx = per_page * (page+1)
    data = DB.get_items()
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    for i in range(row_count):
        if(i == row_count - 1) and (tot_count%per_row!=0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
    return render_template(
        "list.html",
        datas = data.items(),
        row1 = locals()['data_0'].items(),
        row2 = locals()['data_1'].items(),
        limit = per_page,
        page=page,
        page_count = int((item_counts/per_page)+1),
        total=item_counts)

# 리뷰 조회
@application.route("/review")
def view_review():
    return render_template("review.html")

# 상품 등록
@application.route("/reg_items")
def reg_items():
    username = session.get("id", "")
    return render_template("reg_items.html", username=username)

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
    data = request.form.to_dict()

    image_file = request.files["image"]
    image_path = f"static/image/{image_file.filename}"
    image_file.save(image_path)

    data["img_path"] = image_path

    DB.insert_item(data["name"], data, image_file.filename)
    return render_template("submit_item_result.html", data=data)

# 리뷰 등록
@application.route("/reg_reviews")
def reg_reviews():
    return render_template("reg_reviews.html")

# 리뷰 등록 처리
@application.route("/submit_review_post", methods=['POST'])
def submit_review_post():
    form = request.form.to_dict()

    reviewer_id = form.get("reviewer_id").strip()
    item_name = form.get("item_name").strip()   
    title = form.get("title").strip()
    content = form.get("content").strip()
    rating_raw = form.get("rating")

    if not title:
        flash("리뷰 제목 입력은 필수입니다.", "error")
        return redirect(url_for("reg_reviews"))
    if len(content)<20:
        flash("리뷰 내용은 20자 이상 입력해주세요.", "error")
        return redirect(url_for("reg_reviews"))
    if not rating_raw:
        flash("별점을 선택해주세요.", "error")
        return redirect(url_for("reg_reviews"))
    rating = int(rating_raw)
    
    img_path = None
    image_file = request.files.get("image")
    if image_file and image_file.filename:
        image_file.save(f"static/image/reviews/{image_file.filename}")
        img_path = f"static/image/reviews/{image_file.filename}"

    review = {
        "item_name": item_name,
        "reviewer_id": reviewer_id,
        "title": title,
        "content": content,
        "rating": rating,
        "img_path": img_path,
        "created_at": int(time.time())
    }


# 판매 요청
@application.route("/reg_requests")
def reg_requests():
    nickname = session.get("nickname", "")
    return render_template("reg_requests.html", nickname=nickname)

@application.route("/submit_request_post", methods=['POST'])
def submit_request_post():
    data = request.form
    print("🔍 selected_item_img:", data.get("selected_item_img")) 

    selected_item_name = data.get("selected_item")
    selected_item_img = data.get("selected_item_img", "")
    item_info = DB.get_item_by_name(selected_item_name) or {}

    if selected_item_name:
        item_info["name"] = selected_item_name
        if selected_item_img:
            item_info["img_path"] = selected_item_img
    if selected_item_img:
        item_info["img_path"] = selected_item_img

    request_info = {
        "search": data.get("search", ""),
        "nickname": data.get("nickname", ""),
        "title": data.get("title", ""),
        "content": data.get("content", ""),
        "item": item_info,
    }

    new_id = DB.insert_request(request_info)
    return redirect(url_for("request_detail", request_id=new_id))
    
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

# 품절 변경
@application.route("/item_soldout/<item_name>", methods=["POST"])
def update_item_soldout(item_name):
    is_soldout = request.form.get("is_soldout") == "true"
    DB.update_item_soldout(item_name, is_soldout)
    return jsonify({"message": f"{item_name}의 판매 상태가 {'품절' if is_soldout else '판매중'}으로 변경되었습니다."})

# 판매 요청 조회 페이지 (request.html)
@application.route("/request")
def request_page():
    page = request.args.get("page", 0, type=int)
    per_page = 8
    start_idx = per_page * page
    end_idx = per_page * (page + 1)

    data = DB.get_requests()

    count_map = {}
    for req in data:
        item = req.get("item", {})
        name = item.get("name", "상품명 미상")
        count_map[name] = count_map.get(name, 0) + 1

    for req in data:
        item = req.get("item", {})
        name = item.get("name", "상품명 미상")
        item["request_count"] = count_map.get(name, 1)
        req["item"] = item
    
    data.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    total_count = len(data)
    data = data[start_idx:end_idx]
    page_count = int((total_count / per_page) + 1)

    return render_template(
        "request.html",
        datas=data,
        total=total_count,
        page=page,
        page_count=page_count
    )

# 마이페이지
@application.route("/mypage")
def mypage():
    if "id" not in session:
        flash("로그인 후 이용 가능합니다.")
        return redirect(url_for("login"))

    user_id = session["id"]
    user = DB.get_user_by_username(user_id)
    purchases = DB.get_purchases(user_id)

    enriched_purchases = []
    for p in purchases:
        item = DB.get_item_by_name(p["item_name"])
        p["item"] = item or {}
        enriched_purchases.append(p)

    return render_template("mypage.html", user=user, purchases=enriched_purchases)

# 구매 처리
@application.route("/buy_item", methods=["POST"])
def buy_item():
    if "id" not in session:
        return jsonify({"error": "로그인이 필요합니다."}), 401

    user_id = session["id"]
    item_name = request.form.get("item_name")
    quantity = int(request.form.get("quantity", 1))
    created_at = time.strftime("%Y-%m-%d %H:%M")

    # DBhandler 내부에 purchase 저장용 메서드 추가
    DB.add_purchase(user_id, item_name, quantity, created_at)

    return jsonify({"message": "구매가 완료되었습니다!"})

# 상세상품 (프론트엔드 화면 설계 확인용)
# 수정X -> 백엔드에서 넘겨주는 화면은 submit_item_result.html 만들어져있음. -> 라우팅 따로 할 것
@application.route("/item_result_fe")
def item_result_fe_page():
    return render_template("submit_item_result_frontend.html")

# 상세리뷰 (프론트엔드 화면 설계 확인용)
# 수정X -> 백엔드에서 넘겨주는 화면은 submit_review_result.html 만들어져있음. -> 라우팅 따로 할 것
@application.route("/review_result_fe")
def review_result_fe_page():
    return render_template("submit_review_result_frontend.html")

# 로그인
@application.route("/login")
def login():
    return render_template("login.html")

# 로그인 처리
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

# 로그아웃 처리
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('home'))

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


@application.route("/view_detail/<name>/")
def view_item_detail(name):
    print("###name:", name)
    data = DB.get_item_byname(str(name))
    print("####data:", data)
    data["name"] = name
    return render_template("submit_item_result.html", name=name, data=data)

# ------------------------
# Flask 실행
# ------------------------

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, debug=True)