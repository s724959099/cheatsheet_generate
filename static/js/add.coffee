
vm = new Vue({
    el: '#app',
    data: {
        name:null
    }
    methods: {
        add_table:->
            console.log(this.name)
            obj={
                Name:this.name
            }

            data=myAjax.postSync("/api/topic",obj)
            debugger
            if data.code==11
                window.location="/edit/#{}"
    }
})