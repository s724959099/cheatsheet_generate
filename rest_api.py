from flask_restful_swagger_2 import Resource
from libs.flask_get import *
from Model.db_manager import *
from utli.mytool import *

# from libs.flask_get import *

"""

class SampleREST(Resource):
    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

    def post(self):
        pass

"""


class TableREST(Resource):
    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

    @return_transform()
    def post(self):
        table_data = json_get("table_data")
        return TableManager.add_table(table_data)


class TopicREST(Resource):
    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

    @return_transform("topic")
    def post(self):
        topic_data = json_get("topic_data")
        return TopicManager.add_topic(topic_data)
