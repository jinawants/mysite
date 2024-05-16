import pymysql
import pymysql.cursors

_db = pymysql.connect(
    host = 'flowgo.mysql.pythonanywhere-services.com',
    port = 3306,
    user = 'flowgo',
    password = 'jina1104',
    db = 'flowgo$ubion'
)

# 가상공간 Cursor 생성
cursor = _db.cursor(pymysql.cursors.DictCursor)

# table 생성 쿼리문을 적어 보자
create_user = """
    create table user
    if not exists 
    user (
    id varchar(32) primary key,
    password varchar(64) not null,
    name varchar(32) not null
    )
"""

# 쿼리문 실행
cursor.execute(create_user)
# 동기화
_db.commit()
# 서버와의 연결 종료
_db.close()

print("테이블 생성 완료")