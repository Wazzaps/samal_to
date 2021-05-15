import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import OnboardingView from './components/OnboardingView.vue'
import TimetableView from './components/TimetableView.vue'
import TaskView from './components/TaskView.vue'
import TasksView from './components/TasksView.vue'
import PeopleView from './components/PeopleView.vue'
import PersonView from './components/PersonView.vue'
import store from './store.js'

Vue.config.productionTip = false

const router = new VueRouter({
  routes: [
    { path: '/', component: OnboardingView, name: "OnboardingView" },
    { path: '/:room/', component: TimetableView },
    { path: '/:room/import/:data', component: TimetableView },
    { path: '/:room/tasks', component: TasksView },
    { path: '/:room/tasks/:id', component: TaskView, name: "TaskView" },
    { path: '/:room/people', component: PeopleView },
    { path: '/:room/people/:id', component: PersonView, name: "PersonView", },
  ]
});

// Load state if navigating to new room
let room = null;
router.beforeEach((to, _from, next) => {
  if (room != to.params.room) {
    room = to.params.room;
    if (room === "example") {
      // Fill with example data
      window.exampleData();
    } else if (to.params.data != null) {
      // Import data
      const decoded = to.params.data.replace(/-/g, "+").replace(/_/g, "/")
      const state = window.LZUTF8.decompress(decoded, {inputEncoding: "Base64"});

      localStorage.setItem(`state-${room}`, state);
      store.replaceState(JSON.parse(state));

      router.replace(`/${room}/`);
    } else {
      // Load data from storage
      let loadedState = JSON.parse(localStorage.getItem(`state-${room}`));
      if (!loadedState) {
        loadedState = {
          tags: {},
          people: {},
          tasks: {},
        };
      }
      store.replaceState(loadedState);
    }
  }
  next();
});

// Save state on change
store.subscribe((_mutation, state) => {
  localStorage.setItem(`state-${room}`, JSON.stringify(state));
});

new Vue({
  render: h => h(App),
  router,
  store,
}).$mount('#app')
