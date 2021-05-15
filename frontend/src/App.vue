<template>
  <div>
    <nav-header/>
    <b-container id="app" class="pb-4">
      <router-view></router-view>

      <b-modal id="misc-modal" title="Credits">
        <p class="my-2">
          Created with ♥ by <a href="https://github.com/Wazzaps">@Wazzaps</a> and <a href="https://github.com/Itay2805">@Itay2805</a>
          <br>
          <br>
          Help us pay the server costs:
          <br>
          <br>
          <center>
            <b-button
              id="bmc"
              variant="primary"
              href="https://www.buymeacoffee.com/wazzaps"
            >Buy us a coffee</b-button>
          </center>
        </p>

        <template #modal-footer="{ ok }">
          <b-button variant="secondary" @click="ok()">
            Dismiss
          </b-button>
        </template>
      </b-modal>
    </b-container>
  </div>
</template>

<script>
import Vue from 'vue'
import VueRouter from 'vue-router'
import Vuex from 'vuex'

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import NavHeader from './components/NavHeader.vue'

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)
Vue.use(VueRouter)
Vue.use(Vuex)

export default {
  name: 'App',
  components: {
    NavHeader,
  }
}
</script>

<style>
button.btn-primary {
  background: linear-gradient(#1a89ff, #006cdf);
  box-shadow: 0 4px 16px -2px #6594c7;
  border-radius: 4px;
}

button.btn-danger {
  background: linear-gradient(#D23C40, #B93438);
  box-shadow: 0 4px 16px -2px #db6264;
  border-radius: 4px;
}

#bmc {
  background: linear-gradient(#1a89ff, #006cdf);
  box-shadow: 0 4px 16px -2px #6594c7;
  padding: 0.4rem 1rem;
  font-size: 1.3rem;
  border-radius: 0.3rem;
}
</style>
