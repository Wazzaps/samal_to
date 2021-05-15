import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import TimetableView from './components/TimetableView.vue'
import TaskView from './components/TaskView.vue'
import TasksView from './components/TasksView.vue'
import PeopleView from './components/PeopleView.vue'
import PersonView from './components/PersonView.vue'
import store from './store.js'

Vue.config.productionTip = false

const router = new VueRouter({
  routes: [
    { path: '/:room/', component: TimetableView },
    { path: '/:room/tasks', component: TasksView },
    { path: '/:room/tasks/:id', component: TaskView, name: "TaskView" },
    { path: '/:room/people', component: PeopleView },
    { path: '/:room/people/:id', component: PersonView, name: "PersonView", },
  ]
});

// Watch route for room id changes
function generateRandomID() {
  var idBytes = new Uint8Array([0, 0, 0, 0, 0, 0]);
  for (let i = 0; i < 6; i++) {
    idBytes[i] = Math.random() * 256;
  }
  return btoa(String.fromCharCode.apply(null, idBytes)).replace(/\+/g, "-").replace(/\//g, "_");
}

// Load state if navigating to new room
let lastRoom = null;
router.beforeEach((to, _from, next) => {
  if (lastRoom != to.params.room) {
    lastRoom = to.params.room;
    let loadedState = JSON.parse(localStorage.getItem(`state-${lastRoom}`));
    store.replaceState(loadedState);
  }
  next();
});

// Save state on change
store.subscribe((_mutation, state) => {
  localStorage.setItem(`state-${lastRoom}`, JSON.stringify(state));
});

new Vue({
  render: h => h(App),
  router,
  store,
}).$mount('#app')
