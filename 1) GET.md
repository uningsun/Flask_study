# 1. Simple Example - GET

https://blog.naver.com/wideeyed/221350669178 참조

## 필요한 모듈 설치
```cmd
pip install flask
pip install flask-restful
```

## 소스코드 작성
- api.py 파일
```Python
from flask import Flask
from flask_restful import reqparse, Api, reqparse, Resource

app = Flask(__name__)
api = Api(app)

class Plus(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('x', required=True, type=int, help='x cannot be blank')
            parser.add_argument('y', required=True, type=int, help='y cannot be blank')
            args = parser.parse_args()
            result = args['x']+args['y']
            return {'result' : result}
        except Exception as e:
            return {'error': str(e)}


api.add_resource(Plus, '/plus')

if __name__ == '__main__':
    app.run(debug=True)
```

## 소스코드 실행
```cmd
python api.py
```

## debug
- 새로운 커맨드 창에서 실행
```cmd
curl -d "x=3&y=10" http://localhost:5000/plus  -X GET
```
- 결과
```cmd
{
    "result": 13
}
```

(-d 옵션을 추가하면 -X POST는 제외 가능)

## 정리

### 1. reqparse
  
1. parser = reqparse.RequestParser()로 틀을 만든 후
```Python
parser = reqparse.RequestParser()
```
2. .add_argument로 key 형태 정의
```Python
parser.add_argument('x', required=True, type=int, help='x cannot be blank')
parser.add_argument('y', required=True, type=int, help='y cannot be blank')
```
3. .parse_args()로 최종 추가된 내용들 가져오기
```Python
args = parser.parse_args()
```
4. .add_argument에 작성했던 key 이름으로 내용 가져올 수 있음
```Python
result = args['x']+args['y']
```
cf. args 저장된 형태
```cmd
{
    "x": 3,
    "y": 10
}
```

---

### 2. curl
- curl : command line용 data transfer tool, HTTP/HTTPS/FTP/LDAP/SCP 등 주요한 프로토콜 지원

- d, --data : < data > send specified data in POST request.
- h, --header : < HEADER > Headers to supply with request.
- X, --request : The request method to use. ex)GET, POST

https://www.lesstif.com/pages/viewpage.action?pageId=14745703

https://blog.naver.com/wideeyed/221350638501
