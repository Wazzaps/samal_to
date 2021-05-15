<template>
    <header id="header" class="mb-4" v-if="$route.name != 'OnboardingView'">
      <!-- Normal header -->
      <b-container
        v-if="$route.params.id == undefined"
        class="d-flex flex-row mb-3 align-items-center py-3 justify-content-between"
      >
        <img class="logo" alt="Samal to logo" src="../assets/logo.png">
        <b-nav pills>
          <b-nav-item :to="`/${roomID}/`" exact exact-active-class="active">Table</b-nav-item>
          <b-nav-item :to="`/${roomID}/tasks`" exact exact-active-class="active">Tasks</b-nav-item>
          <b-nav-item :to="`/${roomID}/people`" exact exact-active-class="active">People</b-nav-item>
        </b-nav>
        <b-button variant="link" v-b-modal.misc-modal><b-icon-three-dots-vertical/></b-button>
      </b-container>

      <!-- Item view header (person view) -->
      <b-container
        v-else-if="$route.name == 'PersonView'"
        class="d-flex flex-row mb-3 px-1 align-items-center justify-content-between"
      >
        <b-button class="py-3" variant="link" to=".." append><b-icon-arrow-left-circle-fill font-scale="2.125"/></b-button>
        <b-input
          class="name-tag text-body mx-3"
          :value="$store.state.people[$route.params.id].name"
          @change="updatePersonName"
          placeholder="Name..."
        />
        <b-button class="pad d-flex flex-row justify-content-center py-3" variant="link" @click="deleteThisPerson">
          <b-icon-trash-fill variant="danger" font-scale="1.5"/>
        </b-button>
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
          @change="updateTaskName"
          placeholder="Name..."
        />
        <b-button class="pad d-flex flex-row justify-content-center py-3" variant="link" @click="deleteThisTask">
          <b-icon-trash-fill variant="danger" font-scale="1.5"/>
        </b-button>
      </b-container>
    </header>
</template>

<script>
export default {
  name: 'HelloWorld',
  computed: {
    roomID() {
      return this.$router.currentRoute.params.room;
    },
  },
  props: {
  },
  components: {
  },
  methods: {
    updatePersonName(name) {
      this.$store.commit('personUpdateName', [this.$route.params.id, name]);
    },

    updateTaskName(name) {
      this.$store.commit('taskUpdateName', [this.$route.params.id, name]);
    },

    deleteThisPerson() {
      this.$store.commit('deletePerson', this.$route.params.id);
      this.$router.push(`/${this.roomID}/people`);
    },

    deleteThisTask() {
      this.$store.commit('deleteTask', this.$route.params.id);
      this.$router.push(`/${this.roomID}/tasks`);
    },
  },
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
  border-radius: 5px;
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
