<template>
  <div>
    <b-list-group class="mb-3">
      <b-list-group-item :to="'/people/' + id" v-for="(person, id) in this.$store.state.people" :key="id">
        <div class="d-flex w-100 align-items-center">
          <person-bubble :person="person" class="mr-3"/>
          <div class="d-flex flex-column w-100">
            <div class="d-flex w-100 flex-wrap justify-content-between">
              <strong class="mr-1">{{person.name}}</strong>
              <a :href="'tel:' + person.phoneNum"><small>{{person.phoneNum}}</small></a>
            </div>
            <div class="d-flex flex-wrap">
              <b-badge
                variant="secondary"
                pill
                class="align-self-start mr-1 mb-1"
                v-for="tagId in person.tags"
                :key="tagId"
              >{{$store.state.tags[tagId]}}</b-badge>
            </div>
          </div>
        </div>
      </b-list-group-item>
    </b-list-group>
    <b-button
      @click="addPerson"
      variant="primary"
      class="float-right mb-3 pr-4 pl-3 py-2"
    ><b-icon-plus/> Add</b-button>
  </div>
</template>

<script>
import 'typeface-rubik';
import PersonBubble from './PersonBubble.vue';

export default {
  components: {
    PersonBubble,
  },
  methods: {
    async addPerson() {
      let newPersonId = await this.$store.dispatch('addPerson');
      this.$router.push('/people/' + newPersonId);
    }
  },
}
</script>

<style scoped>
</style>

<style>
</style>
