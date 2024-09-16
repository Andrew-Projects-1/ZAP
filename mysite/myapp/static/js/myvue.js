$(document).foundation()

const QuestionList = {
    data() {
        return {
            questions: [],
            interval: null,
            author: "none",
        }
    },
    mounted() {
        axios.get('/question_json/')
            .then(function (response) {
                // handle success
                myapp.questions = response.data.questions
                myapp.author = response.data.current_user
                console.log(response);
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
        this.interval = setInterval(() => {
            axios.get('/question_json/')
                .then(function (response) {
                    // handle success
                    myapp.questions = response.data.questions
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
myapp = Vue.createApp(QuestionList).mount('#question-list')