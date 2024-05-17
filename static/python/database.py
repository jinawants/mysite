# mysql 서버와의 연결 ~ query문 질의
# class 생성

import pymysql

class MyDB:
    # 생성자 함수
    def __init__(
            self, _host, _port, _user, _pw, _db      
    ):
        # 클래스 내부에서 사용되는 독립 변수 생성
        self.host = _host
        self.port = _port
        self.user = _user
        self.password = _pw
        self.db = _db
        
    # 매개변수 query문, data값을 이용해 질의를 보낸다
    # 결과 값을 받아오거나 DB Server에 동기화한 뒤 연결을 종료한다
    # 클래스 내부에 함수 생성
    def db_execute(self, query, *data):
        # 데이터베이스와 연결
        _db = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            db = self.db
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
