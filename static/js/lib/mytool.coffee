window.myAjax =
    _base: (type, urlStr, obj, callback)->
        ###
         base ajax function
        ###
        option =
            url: urlStr,
            type: type,
            dataType: "json",
            success: (data, textStatus, jqXHR)->
                data["xhr"] = jqXHR
                callback(data)
            error: (jqXHR, textStatus)->
                data =
                    xhr: jqXHR

                callback(data)
        if type != "GET"
            option["contentType"] = "application/json"

        if obj != null
            data = if type == "GET" then obj else JSON.stringify(obj)
            option["data"] = data
        $.ajax(option)

    _baseSync: (type, urlStr, obj)->
        ###
         base ajax function
        ###
        response = {}
        option =
            url: urlStr,
            type: type,
            async: false
            dataType: "json",
            success: (data, textStatus, jqXHR)->
                response = data
                response["xhr"] = jqXHR
            error: (jqXHR, textStatus)->
                response["xhr"] = jqXHR

        if type != "GET"
            option["contentType"] = "application/json"
        if obj != null
            data = if type == "GET" then obj else JSON.stringify(obj)
            option["data"] = data
        $.ajax(option)
        return response

    get: (urlStr, obj, callback)->
        @_base("GET", urlStr, obj, callback)
    post: (urlStr, obj, callback)->
        @_base("POST", urlStr, obj, callback)
    put: (urlStr, obj, callback)->
        @_base("PUT", urlStr, obj, callback)
    delete: (urlStr, obj, callback)->
        @_base("DELETE", urlStr, obj, callback)

    getSync: (urlStr, obj)->
        @_baseSync("GET", urlStr, obj)
    postSync: (urlStr, obj)->
        @_baseSync("POST", urlStr, obj)
    putSync: (urlStr, obj)->
        @_baseSync("PUT", urlStr, obj)
    deleteSync: (urlStr, obj)->
        @_baseSync("DELETE", urlStr, obj)


event = # an object
    clientList: [] #init
    triggerArgs: [] #init
    listen: (key, fn) ->
# if key not exist  then create an array
        if !@clientList[key]
            @clientList[key] = []

        # input to listen
        @clientList[key].push fn

        # if trigger before listen then still trigger
        if @triggerArgs[key]
            for args in @triggerArgs[key]
                fn.apply(@, args)

        return
    trigger: ->
# get key
        key = Array::shift.call(arguments)
        #get all fns in key
        fns = @clientList[key]

        # init triggerArgs in key
        if !@triggerArgs[key]
            @triggerArgs[key] = []
        @triggerArgs[key].push(arguments)

        #if not found fns
        if !fns or fns.length == 0
            return false

        # do fn which all in key
        i = 0
        fn = undefined
        while fn = fns[i++]
            fn.apply @, arguments
        return

installEvent = (obj) ->
# get new obj and set all key from event
    for key of event
        obj[key] = event[key]
    return obj


Vue.options.delimiters = ['${', '}']