
###
    jquery set Cursor postion
###
$.fn.setCursorPosition = (pos) ->
  @each (index, elem) ->
    if elem.setSelectionRange
      elem.setSelectionRange pos, pos
    else if elem.createTextRange
      range = elem.createTextRange()
      range.collapse true
      range.moveEnd 'character', pos
      range.moveStart 'character', pos
      range.select()
    return
  this

Vue.component('modal', {
    template: '#modal-template'
})

Vue.component('table_add', {
    template: '#table_add'
    methods: {
        btn_fn: ->
            this.$emit("add_click")
    }
})

editable_click_fn=($el,fn)->
    $el.on("click", ->

        value = $el.text()
        console.log("click")
        input_el = "<input type='text' value='" + value + "' id='_editable' '>"
        $(this).html(input_el)
        $(this).off("click")
        $input = $("#_editable")
        $input.setCursorPosition(value.length);
        $input.focus()
        $input.on("keyup",(e)->
            if e.which==13
                console.log("click123")
                fn($input.val())
                $el=$($(this).parent()[0])
                $(this).parent().text($input.val())
                editable_click_fn($el,fn)
        )
    )



Vue.directive("editable", (el, binding,vnode)->
    $el = $(el)
    fn = binding.value
    editable_click_fn($el,fn)

)



Vue.component('topic_table', {
    template: '#topic_table'
    data: ->
        return {

        }
    methods: {
    }
})

$ ->
    get_topic = ->
        res = myAjax.getSync("/api/topic/#{url(2)}", null)
        return res.data


    vm = new Vue({
        el: '#app',
        data: {
            showModal: false
            topic: get_topic()
        }
        methods: {
            edit_callback:(el_data)->
                return (val)->
                    obj=
                        topic_data:
                            Name:val
                    myAjax.putSync("/api/topic/#{url(2)}",obj)

            add_click: ->
                console.log("receive emit")
        }
    })