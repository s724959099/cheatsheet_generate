# from Model.rest_model_view import *
from Model.rest_model_json import *
from Model.dbSmart import SmartDB


class TableManager:

    @staticmethod
    def add_table(table_data):
        smart = SmartDB()
        table = smart.insert_single(Table, table_data)
        return smart.commit(TableJson(table))
