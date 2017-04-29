import copy
from Model.dbModel import *


def db_to_str(cls, date_formate="%Y/%m/%d"):
    new_cls = copy.copy(cls)
    for key, val in new_cls.__dict__.items():
        if val is None:
            new_cls.__dict__[key] = ""

        if isinstance(val, datetime.datetime):
            new_cls.__dict__[key] = new_cls.__dict__[key].strftime(date_formate)

    return new_cls


def json_mapping(fn, arr):
    return list(map(fn, arr))


class BaseJSON:
    def __new__(cls, arg, date_formate="%Y/%m/%d", remove_dict=None):
        if remove_dict is None:
            remove_dict = [
                'CreateDate',
                "CreateBy",
                "ModifiedDate",
                "ModifiedBy",
                "SoftDelete",
            ]
        if arg is None:
            raise Exception("it's None")
        if isinstance(arg, list):
            raise Exception("it's list")

        new_cls = db_to_str(arg, date_formate)
        dict_output = new_cls.__dict__
        for remove in remove_dict:
            dict_output.pop(remove, None)
        for name in list(dict_output):
            cond1 = name.startswith("_")
            cond2 = name.endswith("_")
            if cond1 or cond2:
                dict_output.pop(name, None)

            elif isinstance(dict_output[name], db.Model):
                dict_output.pop(name, None)

        return dict_output


class TableJSON(BaseJSON):
    pass


class TopicJSON(BaseJSON):
    pass
