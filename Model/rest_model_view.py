from Model.dbModel import *


class TopicView:
    @staticmethod
    def single(TopicId):
        return db.session.query(
            Topic
        ).filter(
            Topic.TopicId == TopicId,
            Topic.SoftDelete == False

        ).scalar()