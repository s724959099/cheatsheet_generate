

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

Vue.component('topic_table', {
    template: '#topic_table'
    data: ->
        return {

        }
    methods: {
    }
})

#Vue.component("live-edit", {
#    name: '#live-edit',
#    props: {
#        value: {
#            type: String,
#            required: true,
#        },
#        editable: {
#            type: Boolean,
#            required: true,
#        },
#        multiline: {
#            type: Boolean,
#            default: false,
#        },
#        placeholder: {
#            type: String
#        }
#    }
#    data: {
#
#    }
#
#    watch: {
#        modelvalue: (val)->
#            this.$emit('input', val)
#    }
#})
$ ->
    get_topic = ->
        res = myAjax.getSync("/api/topic/#{url(2)}", null)
        return res.data


    vm = new Vue({
        el: '#app',
        data: {
            showModal: false
            topic: get_topic()
            title:null,
        }
        methods: {
            add_click: ->
                console.log("receive emit")
        }
    })