from Model.rest_model_view import *
from Model.rest_model_json import *
from Model.dbSmart import SmartDB, Relation


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
        topic = TopicView.single(TopicId)
        return TopicJSON(topic)

    @staticmethod
    def update_single(topic_data, TopicId):
        topic = TopicView.single(TopicId)
        smart = SmartDB()
        smart.update_single(topic, topic_data)
        return smart.commit(TopicJSON(topic))
