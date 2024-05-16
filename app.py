# 필요한 라이브러리 로드
from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import pymysql.cursors
from datetime import timedelta

# Flask의 인자는 파일 이름
app = Flask(__name__)
# secret_key 설정
app.secret_key = 'ABC'
# session의 지속 시간을 설정해 보자
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=10)

# session 초기화 : 데이터가 있을 때만 돌아가더라;;
# session.clear()

# DB Server와 연결하고 가상공간 Cursor를 생성한다
# 매개변수 query문, data값을 이용해 질의를 보낸다
# 결과 값을 받아오거나 DB Server에 동기화한 뒤 연결을 종료한다
def db_execute(query, *data):
    # 데이터베이스와 연결
    _db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='1234',
        database='ubion1'
    )
    # 가상공간 Cursor 생성
    cursor = _db.cursor(pymysql.cursors.DictCursor)
    # 매개변수 query, data를 이용하여 질의
    cursor.execute(query, data)
    # query가 select라면 결과값을 변수(result)에 저장
    if query.lower().strip().startswith('select'):
        result = cursor.fetchall()
    # query가 select가 아니라면 DB Server와 동기화하고 변수는 Query OK 문자 대입
    else:
        _db.commit()
        result = "Query OK"
    # 데이터베이스 서버와 연결 종료
    _db.close()
    # 결과를 되돌려준다
    return result


# 메인페이지 api 생성
# 로그인 화면
@app.route("/")
def index():
    # 세션에 데이터가 존재한다면?
    if 'user_id' in session:
        return redirect('/index')
    else:
    # 요청이 들어왔을 때 state 데이터가 존재하면
        try:
            _state = request.args['state']
        except:
            # 처음 로그인 화면을 로드한 경우
            _state = 1
        # login.html을 반환한다
        return render_template('login.html', state = _state)

# 로그인 화면에서 id와 password 데이터를 보내는 api
@app.route("/main", methods=['post'])
def main():
    # 유저가 보낸 두 데이터 (id, password)
    # 유저가 보낸 id값의 key를 미리 정해주자(input_id)
    # 유저가 보낸 password의 key도 정해주자(input_pw)
    _id = request.form['input_id']
    _pw = request.form['input_pw']
    # 잘 받아와졌는지 확인하도록 하자
    print(f"/main[post] 아이디 : {_id}, /main[post] 비밀번호 : {_pw}")
    # 유저가 보낸 데이터를 DB Server의 table data와 비교해 보자
    login_query = """
        select
        *
        from
        user
        where
        id = %s
        and
        password = %s
    """

    # 함수 호출
    db_result = db_execute(login_query, _id, _pw)
    if db_result:
        # session에 데이터를 저장한다
        session['user_id'] = _id
        session['user_pw'] = _pw
        # 로그인이 성공하는 경우 main.html을 반환한다
        # return render_template('main.html')
        return redirect('/index')
        # return "login"
    else:
        # 로그인 실패 -> 로그인 화면으로 돌아간다
        return redirect('/?state=2')
        # return "login failed"

# /index 주소 api 생성
@app.route('/index')
def index2():
    # session에 데이터가 존재하면 main.html을 반환한다
    if "user_id" in session:
        return render_template('main.html')
    # session에 데이터가 존재하지 않으면 로그인 화면으로 되돌아간다
    else:
        return redirect ('/')

# 회원 가입 화면을 보여 주는 api
@app.route("/signup")
def signup():
    return render_template('signup.html')

# id 사용 유무를 판단하는 api
@app.route('/check_id', methods=['post'])
def check_id():
    # 프론트에서 비동기통신으로 보내는 id값을 변수에 저장하자
    _id = request.form['input_id']
    # 유저에게 받은 데이터를 확인해 보자
    print(f"'check_id['post']에서 받은 id : {_id}")
    # 유저가 보낸 id값이 사용이 가능한지 확인해 보자
    check_id_query = """
        select * from `user`
        where id = %s
    """
    # 함수 호출
    db_result = db_execute(check_id_query, _id)
    # id가 사용 가능한 경우는 db_result가 존재하지 않는 경우
    if db_result :
        result = "0"
    else:
        result = "1"
    return result

# 회원 정보를 받아와서 데이터베이스에 삽입하는 api
@app.route("/signup2", methods=['post'])
def signup2():
    # 유저가 보낸 데이터를 변수에 저장
    _id = request.form['input_id']
    _pw = request.form['input_pw']
    _name = request.form['input_name']
    # 잘 받아와졌는지 확인해준다
    print(f"/signup2[post]에서 받은 ID : {_id} \n /signup2[post]에서 받은 password : {_pw} \n /signup[post]에서 받은 name : {_name}")
    # 쿼리문 작성
    insert_user_query = """
        insert into `user`
        values(%s, %s, %s)
    """
    # 함수 호출 (에러가 발생하는 경우도 처리해 주자)
    try:
        db_result = db_execute(insert_user_query, _id, _pw, _name)
        print(db_result)
    except:
        db_result = 3
    # 로그인 화면으로 되돌아간다
    if db_result == 3:
        return redirect(f'/?state={db_result}')
    else:
        return redirect('/')

# logout === session 데이터를 제거한다
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



# 웹 서버 실행
app.run(debug = True)