# 5. C#에서 binary 형태의 data 서버로 POST하기
## 0. binary data 저장
```test1.dat``` : BCCD Dataset(https://github.com/Shenggan/BCCD_Dataset/tree/master/BCCD/JPEGImages) ```BloodImage_00000.jpg``` 파일을 binary file 형태로 저장

## 1. 예시 3) 4)의 api.py 파일에 추가 및 수정
```python
# 이전 파일 초반에 모듈 추가
import base64 

...

# TodoList class의 post 함수 수정

class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = args['task'].replace(' ', '+') # 수정
        return TODOS[todo_id], 201
        
...

```

## 2. C#에서 코드 추가 및 수정
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
            // Binary data 읽어오기 추가
            BinaryReader br = new BinaryReader(new FileStream("test1.dat", FileMode.Open));
            byte[] file = br.ReadBytes((int)br.BaseStream.Length);
            br.Close();
            
            // base64 인코딩 : Binary data -> ASCII 인코딩 코드 추가
            string file_s = Convert.ToBase64String(file);

            string url = "http://localhost:5000/todos";
            string responseText = string.Empty;
            
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
            request.Method = "POST";
            request.Timeout = 3 * 1000; 
            
            // 코드 수정 - task = file_s 형태로 서버에 보내기 
            String postData = string.Format("task={0}", file_s);

            byte[] bytes = Encoding.UTF8.GetBytes(postData);
            request.ContentLength = bytes.Length; 
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

## 3. 결과
binary data -> 문자열  (base64 인코딩)
```cmd
{
    "todo4": "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
    ...
```

## 4. 정리

### 1. Base64
https://ko.wikipedia.org/wiki/%EB%B2%A0%EC%9D%B4%EC%8A%A464

- 이진 데이터를 ASCII 영역의 문자들로만 이루어진 일련의 문자열로 바꾸는 인코딩 방식
- 이진 데이터 전송 등에 많이 쓰임

### 2. Python에서 args['task'] 값 (3. 결과)을 가져와 base64 decoding 한 값과 / test1.dat 파일을 불러온 값이 다름
- 이유 : test1.dat을 불러와 base64 encoding한 값과 args['task']를 비교해보니 전자의 '+'가 후자에서는 ' '로 대체됨. 
- 이유의 원인 : C#에서 urlencoded로 서버에 보낼 때 '+' 값이 ' '로 대체되어 가는 것 같다. (이후 JSON형태로 전달 시 문제 발생 X)
