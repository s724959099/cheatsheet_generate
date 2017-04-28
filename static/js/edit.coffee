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
    data:{
        
    }
    methods: {
    }
})



new Vue({
    el: '#app',
    data: {
        showModal: false
    }
    methods:{
        add_click:->
            console.log("receive emit")
    }
})