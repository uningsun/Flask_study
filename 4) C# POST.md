# 4. C#에서 Flask로 POST 하기

## 1. 3rd 예제 api.py 실행
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

## 2. C# 작성 및 실행
```C#
using System;
using System.IO;
using System.Text;
using System.Net;

namespace ConsoleApp11
{
    class Program
    {
        static void Main(string[] args)
        {
            string url = "http://localhost:5000/todos";
            string responseText = string.Empty;
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
            request.Method = "POST";
            request.Timeout = 3 * 1000; // 30초

            string data = "test";

            String postData = string.Format("task={0}", data);

            byte[] bytes = Encoding.UTF8.GetBytes(postData);
            request.ContentLength = bytes.Length; // 바이트수 지정
            request.ContentType = "application/x-www-form-urlencoded"; 

            using (Stream reqStream = request.GetRequestStream())
            {
                reqStream.Write(bytes, 0, bytes.Length);
            }

            try
            {
                using (HttpWebResponse resp = (HttpWebResponse)request.GetResponse())
                {
                    HttpStatusCode status = resp.StatusCode;
                    Stream respStream = resp.GetResponseStream();
                    using (StreamReader sr = new StreamReader(respStream))
                    {
                        responseText = sr.ReadToEnd();
                    }
                }

                Console.WriteLine(responseText);

            }
            
            catch
            {
            }
        }
    }
}
```

## 3. 정리
### 1. C#과 curl 비교
- curl : 커맨드창에 -d "task=데이터" 형태로 전달
- C# : 전송 + 수신 두 단계
```C#
string url = "http://localhost:5000/todos"; //URL
HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
request.Method = "POST"; // Method 방법 설정
request.Timeout = 3 * 1000; // 30초
```

 * 서버 전송    
    
① "task=data" postData 생성
```C#
string data = "test";
String postData = string.Format("task={0}", data); 
```
② postData -> byte 배열에 담음 + 인코딩(UTF8)
```C#
byte[] bytes = Encoding.UTF8.GetBytes(postData);
```
③ request에 byte 수 지정 + ContentType 설정
```C#
request.ContentLength = bytes.Length; // 바이트수 지정
request.ContentType = "application/x-www-form-urlencoded"; 
```
④ 서버 전송
```C#
using (Stream reqStream = request.GetRequestStream())
{
    reqStream.Write(bytes, 0, bytes.Length);
}
```

* 서버 수신

① responseText에 저장

```C#
try
{
    using (HttpWebResponse resp = (HttpWebResponse)request.GetResponse())
    {
        HttpStatusCode status = resp.StatusCode;
        Stream respStream = resp.GetResponseStream();
        using (StreamReader sr = new StreamReader(respStream))
        {
            responseText = sr.ReadToEnd();
        }
    }
...

```

