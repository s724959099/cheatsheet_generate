
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
            console.log("btn_click")
            this.$emit("add_click")
    }
})



Vue.directive("editable", (el, binding)->
    $el = $(el)
    fn = binding.value
    value = $el.text()
    console.log("value=#{value}")
    $el.on("click", ->
        console.log("Test")
        input_el = "<input type='text' value='" + value + "' id='_editable' '>"
        $(this).html(input_el)
        $(this).off("click")
        $input = $("#_editable")
        $input.setCursorPosition(value.length);
        $input.focus()
        $input.on("click",->
            console.log("click")
            $(this).remove()
        )
    )
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
            title: null,
        }
        methods: {
            add_click: ->
                console.log("receive emit")
        }
    })