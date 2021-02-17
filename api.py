from flask import Flask
from flask_restful import Resource, Api, abort
from db import find_code, generate_code

app = Flask(__name__)
api = Api(app)


class GetLink(Resource):

    def get(self, code):

        found, url = find_code(code)

        if found:
            return url
        else:
            return abort(404, message=f"The code {code} is not valid ")


class GetCode(Resource):

    def get(self, url):

        code = generate_code(url)

        return code


api.add_resource(GetLink, '/find/<string:code>')
api.add_resource(GetCode, '/new/<string:url>')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=6000)
