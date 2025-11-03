import pyrebase
import json

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
