# flask 웹 프레임워크 로드
from flask import Flask, render_template, redirect, request
from dotenv import load_dotenv
import os

load_dotenv()

# database 안 MyDB class 로드
from static.python.database import MyDB

# Flask class 생성
app = Flask(__name__)

# MyDB class 생성
mydb = MyDB(
    os.getenv('host'),
    os.getenv('port'),
    os.getenv('user'),
    os.getenv('password'),
    os.getenv('db_name')
)

# mydb = MyDB(
#     '127.0.0.1',
#     3306,
#     'root',
#     '1234',
#     'ubion1'
# )

# 'localhost:5000/' api 생성 -> carousel.html 반환
@app.route('/')
def carousel():
    # DB Server에 있는 company_list table의 정보 로드
    select_query = """
        select * from company_list
    """
    # class 생성한 mydb 안에 내장된 함수를 불러오자
    db_data = mydb.db_execute(select_query)
    # db_data의 type은 list 안 dict 형태 [{name : xx}, {link_url : xxxx}, {img_url : xxxx}]
    # db_data에서 img_url만 추출해 보자
    imgs = []
    links = []
    for data in db_data:
        imgs.append(data['img_url'])
        links.append(data['link_url'])
    print(imgs)
    print(links)
    return render_template('carousel.html', imgs = imgs, links = links, cnt = len(imgs))


# 웹 서버 실행
app.run(port = 5000, debug = True)