from Model.db_lib import *


class SmartDB:
    def __init__(self):
        self.allSuc = True
        self.msg = None

    def commit(self, arg=None):
        if not self.allSuc:
            return self.allSuc, self.msg, None

        suc, msg = db_commit()
        if not suc:
            return self.allSuc, self.msg, None

        return self.allSuc, self.msg, arg

    def _do_error_thing(self, msg):
        self.allSuc = False
        self.msg = msg
        raise Exception(msg)

    def insert_list(self, clsName, d_arg, d_arg_other={}):
        suc, msg, new_obj = dict_insert_db_list(
            clsName,
            d_arg,
            d_arg_other,
            db_flush
        )
        if not suc:
            self._do_error_thing(msg)
        return new_obj

    def insert_single(self, clsName, d_arg, d_arg_other={}):
        suc, msg, new_obj = dict_insert_db(
            clsName,
            d_arg,
            d_arg_other,
            db_flush
        )
        if not suc:
            self._do_error_thing(msg)
        return new_obj

    def delete_list(self, arg):
        db_delete_list(arg)
        suc, msg = db_flush()
        if not suc:
            self._do_error_thing(msg)

    def delete_single(self, arg):
        args = [arg]
        return self.delete_list(arg)

    def update_single(self, db_obj, d_arg):
        suc, msg = dict_update_db(db_obj, d_arg, db_flush)
        if not suc:
            self._do_error_thing(msg)

    def update_list(self, list_db_obj, d_arg):
        for db_obj in list_db_obj:
            self.update_single(db_obj, d_arg)


class Relation:
    def __init__(self, model_view):
        self.__model_view = model_view
        self.__foreign_key = []
        self.__properties = []
        self.to_model_json = {}

    def get(self, output_name):
        def get_last_obj(data):
            if data is None:
                last_obj = None
            if isinstance(data, list):
                last_obj = data[-1]
            else:
                last_obj = data
            return last_obj

        temp_obj = {}
        first_loop = True
        for property in self.__properties:
            temp_obj[property] = None
        for models in self.__model_view:
            model_obj = {}
            for model in models:
                model_name = model.__class__.__name__
                model_obj[model_name] = model

            for d in self.__foreign_key:
                parent = d["parent"]
                child = d["child"]
                keys = d["keys"]
                data = temp_obj[parent]
                if data is None:
                    last_obj = None
                if isinstance(data, list):
                    last_obj = data[-1]
                else:
                    last_obj = data

                if last_obj is None:
                    setattr(model_obj[parent], child, model_obj[child])
                    temp_obj[parent] = model_obj[parent]
                else:
                    check_last_same = True
                    for key in keys:
                        data1 = getattr(model_obj[parent], key)
                        data2 = getattr(last_obj, key)
                        if data1 != data2:
                            check_last_same = False
                            break
                    if check_last_same:
                        last_obj_child = getattr(last_obj, child)
                        if isinstance(last_obj_child, list):
                            last_obj_child.append(model_obj[child])
                        else:
                            last_obj_child = [last_obj_child, model_obj[child]]

                        setattr(last_obj, child, last_obj_child)
                        temp_obj[parent] = last_obj

                    else:
                        setattr(model_obj[parent], child, model_obj[child])
                        if isinstance(temp_obj[parent], list):

                            temp_obj[parent].append(model_obj[parent])
                        else:
                            temp_obj[parent] = [temp_obj[parent], model_obj[parent]]

        return temp_obj[output_name]

    def set_name(self, name):

        parent = name.split(".")[0]
        child = name.split(".")[1]
        push_data = [parent, child]
        for data in push_data:
            if data not in self.__properties:
                self.__properties.append(data)

        parent_model = getattr(db_model, parent)
        keys = [key.name for key in inspect(parent_model).primary_key]

        self.__foreign_key.append({
            "parent": parent,
            "child": child,
            "keys": keys
        })

    def set_json(self, name, JsonModel):
        self.to_model_json[name] = JsonModel
        return self
