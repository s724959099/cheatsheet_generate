
vm = new Vue({
    el: '#app',
    data: {
        name:null
    }
    methods: {
        add_table:->
            console.log(this.name)
            
    }
})