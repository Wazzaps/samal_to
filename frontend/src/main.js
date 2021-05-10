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
    { path: '/', component: TimetableView },
    { path: '/tasks', component: TasksView },
    { path: '/tasks/:id', component: TaskView, name: "TaskView" },
    { path: '/people', component: PeopleView },
    { path: '/people/:id', component: PersonView, name: "PersonView", },
  ]
});

new Vue({
  render: h => h(App),
  router,
  store,
}).$mount('#app')
