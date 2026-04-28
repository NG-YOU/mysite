# 라이브러리(프레임워크) 로드
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
# 데이터베이스에 접속하는 커스텀 모듈
from db import MyDB
# sql 쿼리문이 저장되어 있는 커스텀 모듈
from querys import user

# Flask class 생성
# __name__ : 현재 파일의 이름을 나타냄
app = Flask(__name__)
# MyDB class 생성 -> Local DB 접속하기 때문에 생성자 함수 인자를 기본값으로 사용
db = MyDB()
# query문 모듈에서 create_query 실행
db.sql_query(user.create_query)
db.commit()

# 로그인 화면 보여주는 api 생성
@app.route('/')
def index():
    return render_template('login.html')

# 회원 가입 화면 보여주는 api 생성
@app.route('/signup')
def signup():
    return render_template('signup.html')

# 로그인 api 생성 -> DB server에 등록된 아이디와 비밀번호가 일치하는가
@app.route('/login', methods=['post'])
def login():
    # user 모듈 안에 login_query를 이용하여 유저가 입력한 데이터 확인
    # post 방식으로 유저가 보낸 데이터는 request 안에 form에 데이터가 dict 형태로 존재
    _id = request.form['input_id']
    _pass = request.form['input_pass']
    print('/login[post] input_data : ', _id, _pass)
    # 실제 데이터베이서 서버에 질의를 보내고 결과를 받는다
    sql_result = db.sql_query(user.login_query, _id, _pass)
    db.commit()
    # 로그인 성공 -> sql_result 존재
    if sql_result:
        # 로그인이 성공하는 경우 -> dashboard 주소로 이동
        return redirect('/dashboard')
    else:
        return redirect('/')
    
# 회원 가입 api 생성
@app.route('/signup2', methods=['post'])
def signup2():
    print('/signup2[post] input_data : ', request.form)
    # request.form -> {'input_id' : 'xxxx', 'input_pass' : 'xxxx', 'input_name' : 'xxxx' }
    # dict형 데이터를 언패킹하여 인자 사용 **
    db.sql_query(user.signup_query, **request.form)
    # 회원 가입 완료 되면 로그인 화면으로 돌아간다
    db.commit()
    return request('/')

# dashboard.html 연결하는 api 생성
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard2')
def dashboard2():
    return render_template('dashboard2.html')


# 웹 서버 실행 디버그 모드 on
app.run(debug=True)
