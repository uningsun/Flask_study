# 2. Resourceful Routing Example - PUT, GET 
https://flask-restful.readthedocs.io/en/latest/quickstart.html

## 1. .py파일 생성 후 실행
```Python
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
```

## 2. debug
```cmd
$ curl http://localhost:5000/todo1 -d "data=Remember the milk" -X PUT
{"todo1": "Remember the milk"}
$ curl http://localhost:5000/todo1
{"todo1": "Remember the milk"}
$ curl http://localhost:5000/todo2 -d "data=Change my brakepads" -X PUT
{"todo2": "Change my brakepads"}
$ curl http://localhost:5000/todo2
{"todo2": "Change my brakepads"}
```

## 3. 정리
### 1. HTTP METHOD
- GET : 서버에게 resource를 보내달라고 요청. 서버(혹은 DB)의 resource는 클라이언트로 전달만 될 뿐 변경되지 않음.
- PUT : 요청된 자원을 수정(UPDATE)한다. 내용 갱신을 위주로 Location : URI를 보내지 않아도 된다. 클라이언트측은 요청된 URI를 그대로 사용하는 것으로 간주함.
- POST : 서버에게 resource를 보내면서 생성(CREATE)해 달라고 요청. ex) 회원가입을 하면 DB에 새로운 회원정보가 등록되고, 사진을 업로드 하면 그 사진이 웹사이트에 등록됩니다.

https://javaplant.tistory.com/18

https://m.blog.naver.com/azure0777/220824614635

---

### 2. <string:todo_id>, request.form
1. <string:todo_id> - string 형태로 들어온 임의의 string 주소(todo_id)
2. request.form['data'] - 'data= '형태로 들어온 data
