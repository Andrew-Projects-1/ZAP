$(document).foundation()

/*
document.querySelector('h1').addEventListener('click', function(){
  alert("You poked an h1 header!");
});

document.querySelector('p').addEventListener('click', function(){
  alert("You poked a paragraph!");
});

document.querySelector('ol').addEventListener('click', function(){
  alert("You poked an ordered list!");
});

document.querySelector('ul').addEventListener('click', function(){
  alert("You poked an unordered list!");
});
*/


let h1 = document.querySelectorAll('h1');
for (i of h1) {
  i.addEventListener('click', function() {
    alert("You poked an h1 header!");
  });
}

let p = document.querySelectorAll('p');
for (i of p) {
  i.addEventListener('click', function() {
    alert("You poked a paragraph!");
  });
}

let ol = document.querySelectorAll('ol');
for (i of ol) {
  i.addEventListener('click', function() {
    alert("You poked an ordered list!");
  });
}

let ul = document.querySelectorAll('ul');
for (i of ul) {
  i.addEventListener('click', function() {
    alert("You poked an unordered list!");
  });
}

const VueExamples = {
  data() {
      return {
          count: 0,
          welcome: true,
          big: true
      }
  }
}
myvueexamples = Vue.createApp(VueExamples).mount('#vue-examples')


const ListExample = {
  data() {
      return {
          items: [
              { message: 'CINS 465' },
              { message: 'Fall 2022' },
              { message: 'Hello World' }
          ]
      }
  }
}
mylistexamples = Vue.createApp(ListExample).mount('#list-example')