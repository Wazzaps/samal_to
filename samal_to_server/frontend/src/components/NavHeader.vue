<template>
    <header id="header" class="mb-4">
      <!-- Normal header -->
      <b-container
        v-if="$route.params.id == undefined"
        class="d-flex flex-row mb-3 align-items-center py-3 justify-content-between"
      >
        <img class="logo" alt="Samal to logo" src="../assets/logo.png">
        <b-nav pills>
          <b-nav-item to="/" exact exact-active-class="active">Table</b-nav-item>
          <b-nav-item to="/tasks" exact exact-active-class="active">Tasks</b-nav-item>
          <b-nav-item to="/people" exact exact-active-class="active">People</b-nav-item>
        </b-nav>
        <b-button variant="link" v-b-modal.modal-1><b-icon-three-dots-vertical/></b-button>
      </b-container>

      <!-- Item view header (person view) -->
      <b-container
        v-else-if="$route.name == 'PersonView'"
        class="d-flex flex-row mb-3 px-1 align-items-center justify-content-between"
      >
        <b-button class="py-3" variant="link" to=".." append><b-icon-arrow-left-circle-fill font-scale="2.125"/></b-button>
        <!-- <b-button variant="outline-primary d-flex flex-row align-items-center">
          <span class="title mr-2">{{$store.state.people[$route.params.id].name}}</span>
          <b-icon-pencil-fill font-scale="0.8"/>
        </b-button> -->
        <b-input
          class="name-tag text-body mx-3"
          :value="$store.state.people[$route.params.id].name"
          placeholder="Name..."
        />
        <div class="pad d-flex flex-row justify-content-center">
          <person-bubble
            :person="$store.state.people[$route.params.id]"
            flat
          />
        </div>
      </b-container>

      <!-- Item view header (task view) -->
      <b-container
        v-else
        class="d-flex flex-row mb-3 px-1 align-items-center justify-content-between"
      >
        <b-button class="py-3" variant="link" to=".." append><b-icon-arrow-left-circle-fill font-scale="2.125"/></b-button>
        <b-input
          class="name-tag text-body mx-3"
          :value="$store.state.tasks[$route.params.id].name"
          placeholder="Name..."
        />
        <div class="pad"/>
      </b-container>
    </header>
</template>

<script>
import PersonBubble from "./PersonBubble.vue";
export default {
  name: 'HelloWorld',
  props: {
  },
  components: {
    PersonBubble,
  }
}
</script>

<style scoped>
.name-tag {
  text-align: center;
  font-size: 1.35rem;
  font-weight: bold;
}

.pad {
  /* padding: 0 30px; */
  width: 93px;
  padding-right: 0.75rem;
}

.title {
  font-size: 1.3rem;
  margin-bottom: 0;
  font-weight: bold;
}
</style>

<style>
.logo {
  height: 40px;
}

.nav-link.active, .logo {
  box-shadow: 0 4px 16px -2px #6594c7;
  border-radius: 4px;
}

.nav-link.active {
  background: linear-gradient(#1a89ff, #006cdf);
}

@media only screen and (max-width: 360px) {
  .nav-link {
    padding: 0.5rem 0.5rem;
  }
}

#header {
  background: #ffffff;
  box-shadow: 0 0 16px #c2c8ce;
}
</style>
