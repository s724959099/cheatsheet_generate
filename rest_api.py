from flask_restful_swagger_2 import Api, swagger, Resource
from libs.flask_get import *


class TableREST(Resource):
    def get(self):
        return {
            "UserId": session_get("UserId"),
            "UserType": session_get("UserType")
        }

    def put(self):
        session["UserId"] = json_get("UserId")
        session["UserType"] = json_get("UserType")
        return "ok"
