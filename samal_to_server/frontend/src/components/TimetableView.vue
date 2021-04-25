<template>
  <div>
    <!-- <center>
      <b-button variant="outline-secondary" v-b-modal.timerange-picker>
        <b>2021-05-22</b> 10:00 – <b>2021-05-22</b> 13:00
      </b-button>
    </center> -->

    <!-- Highlight ID toggle -->
    <!-- <b-button @click="increment()">{{this.$store.state.count}}</b-button> -->

    <h3>TODO: Shifts x People</h3>

    <b-modal id="timerange-picker" title="Select date &amp; time range">
      <h5>Start date:</h5>
      <b-row>
        <b-col class="pr-1"><b-datepicker/></b-col>
        <b-col class="pl-1"><b-timepicker/></b-col>
      </b-row>
      <h5 class="mt-4">End date:</h5>
      <b-row>
        <b-col class="pr-1"><b-datepicker/></b-col>
        <b-col class="pl-1"><b-timepicker/></b-col>
      </b-row>
      <template #modal-footer="{ ok }">
        <b-button variant="primary" @click="ok()">
          Save
        </b-button>
      </template>
    </b-modal>
  </div>
</template>

<script>
export default {
  methods: {
    increment () {
      this.$store.commit('increment')
    },
  },
}
</script>

<style scoped>
</style>
