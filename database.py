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
            "img_path": img_path             
        }
        self.db.child("item").child(name).set(item_info)
        print(data,img_path)
        return True

    def get_items(self):
        items = self.db.child("item").get().val()
        return items

    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value=""
        print("##########", name)
        for res in items.each():
            key_value = res.key()

            if key_value == name:
                target_value = res.val()
        return target_value

    # 아래 코드는 판매 요청 관련 함수들
    def insert_request(self, data):
        request_info = {
            "search": data["search"],
            "nickname": data["nickname"],
            "title": data["title"],
            "content": data["content"],
            "item": data.get("item", {}),
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self.db.child("request").push(request_info)
        return True

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
