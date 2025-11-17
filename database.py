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

    def find_user(self, username_, password_):
        users = self.db.child("user").get()
        target_value = []
        for res in users.each():
            value = res.val()

            if value['username'] == username_ and value['password'] == password_:
                return True
        return False

    def insert_item(self, name, data, img_path):
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
        self.db.child("item").child(name).set(item_info)
        print(data,img_path)
        return True
    
    # 품절 여부 변경
    def update_item_soldout(self, item_name, is_soldout):
        self.db.child("item").child(item_name).update({"is_soldout": is_soldout})
        print(f"{item_name} 판매 상태 변경: {'품절' if is_soldout else '판매중'}")

    def get_items(self):
        items = self.db.child("item").get().val()
        if not items:
            return {}

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

    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value=""
        print("##########", name)
        for res in items.each():
            key_value = res.key()

            if key_value == name:
                target_value = res.val()
        return target_value

    # 구매 관련
    def add_purchase(self, user_id, item_name, quantity, created_at):
        purchase_data = {
            "item_name": item_name,
            "quantity": quantity,
            "created_at": created_at,
        }
        self.db.child("purchase").child(user_id).push(purchase_data)

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
    
    # 좋아요 관련
    def get_heart_byname(self, uid, name):
        hearts = self.db.child("heart").child(uid).get()
        target_value = {"interested": "N"}  # 기본값

        if hearts.val() is None:
            return target_value

        for res in hearts.each():
            if res.key() == name:
                return res.val()

        return target_value

    def update_heart(self, user_id, isHeart, item):
        heart_info = {
            "interested": isHeart
        }
        self.db.child("heart").child(user_id).child(item).set(heart_info)
        return True

    # 아래 코드는 판매 요청 관련 함수들
    def insert_request(self, data):
        item = data.get("item", {})
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

        new_ref = self.db.child("request").push(request_info)
        new_key = new_ref["name"]
        return new_key

    def get_item_names(self):
        items = self.db.child("item").get()
        result = []
        for item in items.each():
            val = item.val()
            result.append({
                "name": item.key(),
                "img_path": val.get("img_path", ""),
                "status": val.get("status", ""),
                "price": val.get("price", 0),
                "stars": val.get("stars", 5),
                "rating_count": val.get("rating_count", 0),
            })
        return result

    def get_item_by_name(self, name):
        item = self.db.child("item").child(name).get()
        return item.val() if item.val() else {}

    def get_request_by_id(self, request_id):
        req = self.db.child("request").child(request_id).get()
        return req.val() if req.val() else {}

    def get_user_by_username(self, username):
        users = self.db.child("user").get()
        for res in users.each():
            value = res.val()
            if value['username'] == username:
                return value
        return None
    
    # 판매요청등록 테이블에서 데이터 가져오기
    def get_requests(self):
        requests = self.db.child("request").get().val() or {}
        result = []
        for key, val in requests.items():
            val["id"] = key
            result.append(val)

        # created_at 기준 최신순 정렬
        result.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return result