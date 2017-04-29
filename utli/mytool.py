from libs.functools import wraps
from utli import api_return


def return_transform(data_name="data"):
    def out_side_wrap(fn):
        @wraps(fn)
        def wrap(*args, **kwargs):
            suc, msg, db_arg = fn(*args, **kwargs)
            if suc:
                if db_arg is None:
                    return api_return.success()
                else:
                    return api_return.success({
                        data_name: db_arg
                    })


            else:
                return api_return.other_error(msg)

        return wrap

    return out_side_wrap
