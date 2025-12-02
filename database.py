import pyrebase
import json
import datetime

class DBhandler:

    # Firebase 인증 정보 로드
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    # 회원 정보 삽입
    def insert_user(self, data, pw):
        """
        data: {username, nickname, email, phone, student_id}
        pw: hashing된 비밀번호 (sha256)
        """
        user_info = {
            "username": data['username'],
            "password": pw,
            "nickname": data['nickname'],
            "email": data['email'],
            "phone": data['phone'],
            "student_id": data['student_id']
        }

        # 중복 확인
        if self.user_duplicate_check(str(data['username'])):
            # 중복 없음 → user 등록
            self.db.child("user").push(user_info)
            print("회원 등록 성공: ", user_info)
            return True
        else:
            print("이미 회원가입이 되어있습니다: ", data['username'])
            return False
        
    # 사용자 ID 중복 여부 확인
    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()

        print("users###", users.val())
        if str(users.val()) == "None":
            return True
        else:
            for res in users.each():
                value = res.val()
                
                if value['username'] == id_string:
                    return False
            return True

    # 로그인 시 username + pw 존재 여부 확인
    def find_user(self, username_, password_):
        users = self.db.child("user").get()
        target_value = []

        # 전체 유저 순회
        for res in users.each():
            value = res.val()

            # username + 해싱된 password 둘 다 일치해야 로그인 성공
            if value['username'] == username_ and value['password'] == password_:
                return True
        return False

    # 상품 정보 DB 저장
    def insert_item(self, name, data, img_path):
        """
        name : 상품 이름 (key)
        data : form 데이터
        img_path : 실제 저장된 이미지 파일명
        """
        item_info = {
            "seller_id": data['seller_id'],
            "price": int(data['price']),          
            "region": data['region'],
            "status": data['status'],
            "description": data['description'],
            "img_path": img_path,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),

            # 품절 관리를 위해 추가
            "is_soldout": False,
        }
        # item/name 경로에 저장
        self.db.child("item").child(name).set(item_info)
        print(data,img_path)
        return True
    
    # 품절 여부 변경
    def update_item_soldout(self, item_name, is_soldout):
        self.db.child("item").child(item_name).update({"is_soldout": is_soldout})
        print(f"{item_name} 판매 상태 변경: {'품절' if is_soldout else '판매중'}")

    # 모든 상품 조회 + created_at 기준 최신순 정렬
    def get_items(self):
        items = self.db.child("item").get().val()
        if not items:
            return {}

        # created_at을 datetime으로 변환해 정렬
        def safe_timestamp(item):
            value = item[1].get("created_at", 0)
            try:
                # 문자열을 datetime으로 변환
                return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M")
            except Exception:
                return datetime.datetime.min

        sorted_items = dict(
            sorted(items.items(), key=safe_timestamp, reverse=True)
        )
        return sorted_items

    # 이름(key)로 특정 상품 조회
    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value=""
        print("##########", name)

        # item 아래의 모든 key 비교
        for res in items.each():
            key_value = res.key()

            if key_value == name:
                target_value = res.val()
        return target_value

    # 구매 데이터 추가 (user_id 기준 저장)
    def add_purchase(self, user_id, item_name, quantity, created_at):
        purchase_data = {
            "item_name": item_name,
            "quantity": quantity,
            "created_at": created_at,
        }
        self.db.child("purchase").child(user_id).push(purchase_data)

    # 특정 유저의 구매 목록 반환 (최신순 정렬)
    def get_purchases(self, user_id):
        data = self.db.child("purchase").child(user_id).get().val()
        if not data:
            return []

        sorted_purchases = sorted(
            data.values(),
            key=lambda x: x.get("created_at", ""),
            reverse=True
        )
        return sorted_purchases
    
    # 리뷰 저장
    def insert_review(self, review):
        """
        review: {
            item_name, reviewer_id, title, content, rating,
            img_path, created_at
        }
        """
        item_name = review.get("item_name")
        if not item_name:
            return None

        # push() 하면 자동으로 key 생성됨
        new_ref = self.db.child("review").child(item_name).push(review)
        # push 반환값 : {"name": "새로운키"}
        return new_ref["name"]
    
    # 특정 리뷰 상세 조회
    def get_review(self, item_name, review_id):
        res = self.db.child("review").child(item_name).child(review_id).get()
        return res.val() if res.val() else None
    
    # uid 기준으로 해당 상품 좋아요 여부 조회
    def get_heart_byname(self, uid, name):
        hearts = self.db.child("heart").child(uid).get()
        # 기본값: 좋아요 안 함
        target_value = {"interested": "N"}

        if hearts.val() is None:
            return target_value

        # heart/userId/itemName 구조
        for res in hearts.each():
            if res.key() == name:
                return res.val()

        return target_value

    # 좋아요 상태 업데이트
    def update_heart(self, user_id, isHeart, item):
        heart_info = {
            "interested": isHeart
        }
        self.db.child("heart").child(user_id).child(item).set(heart_info)
        return True

    # 판매 요청
    def insert_request(self, data):
        item = data.get("item", {})
        # item.name 값 없으면 검색어로 대체
        if "name" not in item or not item["name"]:
            item["name"] = data.get("search", "상품명 미상")

        request_info = {
            "search": data.get("search", ""),
            "nickname": data.get("nickname", ""),
            "title": data.get("title", ""),
            "content": data.get("content", ""),
            "item": item,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }

        # push 로 새로운 request 생성
        new_ref = self.db.child("request").push(request_info)
        new_key = new_ref["name"]
        return new_key

    # item 리스트(간략버전) (API용)
    def get_item_names(self):
        items = self.db.child("item").get()
        result = []

        for item in items.each():
            name = item.key()
            val = item.val()

            # 리뷰 계산
            reviews_raw = self.db.child("review").child(name).get().val()
            if reviews_raw:
                ratings = [r.get("rating", 0) for r in reviews_raw.values()]
                stars = round(sum(ratings) / len(ratings))
                rating_count = len(ratings)
            else:
                stars = 0
                rating_count = 0

            result.append({
                "name": name,
                "img_path": val.get("img_path", ""),
                "status": val.get("status", ""),
                "price": val.get("price", 0),
                "stars": stars,
                "rating_count": rating_count,
            })

        return result

    # item/name 으로 직접 조회하는 버전 (item == dict)
    def get_item_by_name(self, name):
        item = self.db.child("item").child(name).get()
        return item.val() if item.val() else {}

    def get_request_by_id(self, request_id):
        req = self.db.child("request").child(request_id).get()
        return req.val() if req.val() else {}

    # username으로 사용자 상세값 반환
    def get_user_by_username(self, username):
        users = self.db.child("user").get()
        
        for res in users.each():
            value = res.val()
            # username 일치하면 해당 유저를 리턴
            if value['username'] == username:
                return value
        return None
    
    # request/{id} 조회
    def get_requests(self):
        """
        return: [ {id, search, nickname, title, ...}, ... ]
        created_at 최신순 정렬
        """
        requests = self.db.child("request").get().val() or {}
        result = []
        for key, val in requests.items():
            val["id"] = key
            result.append(val)

        # created_at 기준 최신순 정렬
        result.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return result