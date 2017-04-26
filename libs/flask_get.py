from flask import *
from libs.functools import *


def form_get(var, deafult=None):
    return request.form[var] if request.form.get(var) is not None else deafult


def args_get(var, deafult=None):
    return request.args[var] if request.args.get(var) is not None else deafult


def json_get(var, deafult=None):
    if request.json is None:
        return deafult
    return request.json[var] if request.json.get(var) is not None else deafult


def session_get(var, deafult=None):
    try:
        return session[var] if session.get(var) is not None else deafult
    except:
        return deafult
