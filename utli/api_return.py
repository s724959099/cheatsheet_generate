def other_error(msg=None):
    return {
        'code': 44,
        'msg': 'other error' if None else msg
    }


def success(update=None):
    data = {
        'code': 11,
        'msg': 'success'
    }
    if update is not None:
        data.update(update)
    return data
