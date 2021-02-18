from flask import Flask
from flask_restful import Resource, Api, abort
from service import ServiceManager

app = Flask(__name__)
api = Api(app)
service_manager = ServiceManager()



class GetLink(Resource):

    def get(self, code):

        success, url = service_manager.decode(code)

        if success:
            return url
        else:
            return abort(404, message=f"The code {code} is not valid ")


class GetCode(Resource):

    def get(self, url):

        code = service_manager.encode(url)

        return code


api.add_resource(GetLink, '/find/<string:code>')
api.add_resource(GetCode, '/new/<string:url>')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=6000)
