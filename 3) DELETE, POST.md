# 3. Full Example - GET+PUT+DELETE+POST 
https://flask-restful.readthedocs.io/en/latest/quickstart.html

## 1. api.py 생성 후 실행
```python
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')


if __name__ == '__main__':
    app.run(debug=True)
```

## 2. debug
### 1. GET the list
```cmd
$ curl http://localhost:5000/todos
{
    "todo2": {
        "task": "?????"
    },
    "todo3": {
        "task": "profit!"
    },
    "todo1": {
        "task": "build an API"
    }
}
```

### 2. GET a single task
```cmd
$ curl http://localhost:5000/todos/todo2
{
    "task": "?????"
}
```

### 3. DELETE a task
```cmd
$ curl http://localhost:5000/todos/todo2 -X DELETE -v
*   Trying ::1...
* TCP_NODELAY set
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> DELETE /todos/todo2 HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.55.1
> Accept: */*
>
* HTTP 1.0, assume close after body
< HTTP/1.0 204 NO CONTENT
< Content-Type: application/json
< Content-Length: 0
< Server: Werkzeug/0.11.11 Python/3.5.6
< Date: Mon, 28 Oct 2019 05:50:34 GMT
```

### 4. Add a new task - POST
```cmd
$ curl http://localhost:5000/todos -d "task=something new" -X POST -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying ::1...
* TCP_NODELAY set
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /todos HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.55.1
> Accept: */*
> Content-Length: 18
> Content-Type: application/x-www-form-urlencoded
>
* upload completely sent off: 18 out of 18 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 201 CREATED
< Content-Type: application/json
< Content-Length: 32
< Server: Werkzeug/0.11.11 Python/3.5.6
< Date: Mon, 28 Oct 2019 05:50:58 GMT
<
{
    "task": "something new"
}
```

```cmd
$ curl http://localhost:5000/todos -d "task=testing" -X POST -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying ::1...
* TCP_NODELAY set
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /todos HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.55.1
> Accept: */*
> Content-Length: 12
> Content-Type: application/x-www-form-urlencoded
>
* upload completely sent off: 12 out of 12 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 201 CREATED
< Content-Type: application/json
< Content-Length: 26
< Server: Werkzeug/0.11.11 Python/3.5.6
< Date: Mon, 28 Oct 2019 06:18:02 GMT
<
{
    "task": "testing"
}
```

### 5. Update a task - PUT
```cmd
$ curl http://localhost:5000/todos/todo3 -d "task=something different" -X PUT -v
*   Trying ::1...
* TCP_NODELAY set
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> PUT /todos/todo3 HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.55.1
> Accept: */*
> Content-Length: 24
> Content-Type: application/x-www-form-urlencoded
>
* upload completely sent off: 24 out of 24 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 201 CREATED
< Content-Type: application/json
< Content-Length: 38
< Server: Werkzeug/0.11.11 Python/3.5.6
< Date: Mon, 28 Oct 2019 06:23:11 GMT
<
{
    "task": "something different"
}
* Closing connection 0
```

### 6. check all tasks
```cmd
$ curl http://localhost:5000/todos
{
    "todo5": {
        "task": "testing"
    },
    "todo3": {
        "task": "something different"
    },
    "todo4": {
        "task": "something new"
    },
    "todo1": {
        "task": "build an API"
    }
}
```

---

## 3. 정리

### 1. HTTP 상태 코드
- 200 OK : HTTP 요청에 대한 성공 
- 201 Created : 새로운 자원에 대한 생성, POST 관련
- 204 No content : 요청 성공했으나 리턴되는 콘텐츠가 없음, DELETE 관련
- 400 Bad Request : 잘못된 요청으로 인한 실패
- 404 Not Found : 요청한 자원을 찾을 수 없음. 존재하지 않는 페이지 접근 시

https://mygumi.tistory.com/230

---
