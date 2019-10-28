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
            return args
        except Exception as e:
            return {'error': str(e)}


api.add_resource(Plus, '/plus')

if __name__ == '__main__':
        app.run(debug=True)
