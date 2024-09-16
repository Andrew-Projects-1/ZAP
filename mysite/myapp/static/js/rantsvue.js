$(document).foundation()

const RantsList = {
    data() {
        return {
            rants: [],
            interval: null,
            author: "none",
        }
    },
    mounted() {
        axios.get('/rants_json/')
            .then(function (response) {
                // handle success
                myapp.rants = response.data.rants
                myapp.author = response.data.current_user
                console.log(response);
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
        this.interval = setInterval(() => {
            axios.get('/rants_json/')
                .then(function (response) {
                    // handle success
                    myapp.rants = response.data.rants
                    myapp.author = response.data.current_user
                    console.log(response);
                })
                .catch(function (error) {
                    // handle error
                    console.log(error);
                })
        }, 10000); // 1000 per second
    },
    unmounted() {
        clearInterval(this.interval);
    }
}
myapp = Vue.createApp(RantsList).mount('#rants-list')