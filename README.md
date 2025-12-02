# 🛍️ FLEA:Ewha — 이화여대 수제품 거래 플랫폼

## 👥 팀원
|[설영은](https://github.com/0euun)| [고예빈](https://github.com/KoYebin) |[김유리](https://github.com/uri-git23)|
|------|---|---|
|__[이현경](https://github.com/eluda315)__|__[최지민](https://github.com/izmin120)__||

## 📖 프로젝트 소개
FLEA:EWHA는 이화여대 학생들이 편리하게 직접 만든 수제 물품을 거래할 수 있도록 개발한 웹 기반 거래 플랫폼입니다.
기본적인 회원관리·상품 등록/조회·리뷰 기능뿐만 아니라 품절 상품을 다시 사고 싶은 사람들이 요청글을 올릴 수 있는 ‘판매 요청 기능’을 제공하여 거래 수요를 자연스럽게 연결해주는 것이 특징입니다.

## ✨ 주요 기능
🧑‍💻 회원 기능
- 회원가입 (아이디 중복 확인 포함)
- 로그인 / 로그아웃
- 마이페이지 조회(닉네임, 학번, 구매 내역)

🛒 상품 기능
- 상품 리스트 조회 (최근 등록순 노출)
- 상품 상세 페이지 (가격, 별점, 리뷰 수, 판매자 정보)
- 상품 등록 (로그인 정보 기반 seller 자동 등록)
- 좋은 상품을 저장할 수 있는 좋아요 기능

⭐ 리뷰 기능
- 구매한 상품에 대해 리뷰 작성 (별점/내용/사진 등록)
- 리뷰 전체 조회
- 리뷰 상세 조회

📌 차별화 기능 — 판매 요청 게시판
- 품절된 상품을 다시 구매하고 싶은 사용자가 요청 게시글을 등록할 수 있음
- 특정 상품에 대한 요청 수 자동 집계
- 등록한 요청글에 연결된 관련 상품 표시

## 📂 디렉터리 구조 설명
```
📦 project-root
│
├── static/                   # 정적 파일(Frontend 리소스)
│   ├── css/                  # 스타일(CSS)
│   ├── image/                # 이미지 파일
│   └── js/                   # JavaScript 파일
│
├── templates/                # 화면에 렌더링되는 HTML 파일들
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── item_list.html
│   ├── item_detail.html
│   ├── review_list.html
│   ├── request_list.html
│   └── ... (기타 페이지들)
│
├── app.py                    # Flask 메인 서버 파일(라우팅 + 화면 연결)
├── database.py               # Firebase CRUD(데이터 읽기/쓰기) 기능 모듈
│
├── README.md
└── LICENSE
```
- Flask는 HTML 파일을 templates 폴더에서 자동으로 찾아 렌더링함
- static 폴더의 CSS/JS는 HTML에서 불러와 UI/UX를 담당함
- database.py에서 Firebase 연결 및 데이터 관리를 처리함

## 🛠️ 설치 및 실행
- Python 버전: Python 3.12
- Anaconda 설치: https://www.anaconda.com/download/success
1. 가상환경 생성: `conda create -n <이름> python==<버전>`
2. 가상환경 활성화: `conda activate <이름>
3. Flask 설치: `conda install flask`
4. 웹서버 구동: `flask --debug run`
- 데이터베이스: Firebase realtime database
1. Pyrebase 설치: `pip install pyrebase4`
2. Firebase 프로젝트 및 realtime database 생성
3. Firebase auth 파일 생성

## 📝 기술 블로그
https://velog.io/@fleaewha/posts

<img width="1920" height="1080" alt="3" src="https://github.com/user-attachments/assets/cc6eada6-74ee-4320-93c8-5759bcd06a7b" />
<img width="1920" height="1080" alt="4" src="https://github.com/user-attachments/assets/4ab39e60-f230-429f-9309-dd13206014ce" />
<img width="1920" height="1080" alt="5" src="https://github.com/user-attachments/assets/b0e6cc5d-081e-4431-905c-21514bd65ef6" />
<img width="1920" height="1080" alt="6" src="https://github.com/user-attachments/assets/a3be53d6-f858-4075-888a-52a718ea7041" />
<img width="1920" height="1080" alt="7" src="https://github.com/user-attachments/assets/9a1c1a02-fc99-46c0-aaf9-d517351a119f" />
<img width="1920" height="1080" alt="8" src="https://github.com/user-attachments/assets/2989e6f1-80ef-48d2-a0d5-44cc110c73b3" />
<img width="1920" height="1080" alt="9" src="https://github.com/user-attachments/assets/b27d3e29-32f0-4306-b1c2-73644130af8d" />
<img width="1920" height="1080" alt="10" src="https://github.com/user-attachments/assets/41cef874-17c6-462a-a691-ba45c2c9777e" />
<img width="1920" height="1080" alt="11" src="https://github.com/user-attachments/assets/92700242-17bd-4840-96ba-178c13f3e514" />
<img width="1920" height="1080" alt="12" src="https://github.com/user-attachments/assets/eb163222-5920-4dea-8a03-7d2b94a68fca" />
<img width="1920" height="1080" alt="13" src="https://github.com/user-attachments/assets/45299c14-e385-4e4a-a52b-2bd8a7778132" />
<img width="1920" height="1080" alt="14" src="https://github.com/user-attachments/assets/67eae285-37ee-433a-82f8-20eb46eb8597" />
<img width="1920" height="1080" alt="15" src="https://github.com/user-attachments/assets/0144e31b-2d60-473d-90a0-36059f108502" />
<img width="1920" height="1080" alt="16" src="https://github.com/user-attachments/assets/6d4b0d68-b878-4c7b-91d5-42d25a727895" />
<img width="1920" height="1080" alt="17" src="https://github.com/user-attachments/assets/3ad634e8-1cb1-4808-9d8a-560c4e46b612" />
<img width="1920" height="1080" alt="18" src="https://github.com/user-attachments/assets/8a3c595f-c17e-474f-8223-8f730cafcadd" />
<img width="1920" height="1080" alt="19" src="https://github.com/user-attachments/assets/588498df-a3ea-422a-b74b-e5b914c70013" />
<img width="1920" height="1080" alt="20" src="https://github.com/user-attachments/assets/de0296e3-698d-4381-b531-d5d4e796005d" />
<img width="1920" height="1080" alt="21" src="https://github.com/user-attachments/assets/eae64981-5d26-4e9e-acb5-55cc9b59b04d" />

















