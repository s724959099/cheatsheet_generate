from Model.rest_model_view import *
from Model.rest_model_json import *
from Model.dbSmart import SmartDB,Relation


class TableManager:
    @staticmethod
    def add_table(table_data):
        pass


class TopicManager:
    @staticmethod
    def add_topic(topic_data):
        smart = SmartDB()
        topic = smart.insert_single(Topic, topic_data)
        return smart.commit(TopicJSON(topic))

    @staticmethod
    def view_single(TopicId):
        multidata = TopicView.single(TopicId)
        relation = Relation(multidata)
        relation.set_name("Topic.Table")
        relation.set_name("Table.TableColumn")
        topic = relation.get("Topic")
        print("done")

