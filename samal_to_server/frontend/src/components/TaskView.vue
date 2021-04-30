<template>
  <div>
    <b-input-group class="mb-3">
      <template #prepend>
        <b-input-group-text><b-icon-card-text/></b-input-group-text>
      </template>
      <b-form-textarea
        :value="currentTask.description"
        class="description"
        size="lg"
        rows="3"
        max-rows="8"
        placeholder="Task description..."
        required
      ></b-form-textarea>
    </b-input-group>
    <hr/>
    <b-input-group>
      <template #prepend>
        <b-input-group-text class="d-flex flex-column justify-content-center">
          <b-icon-tags/>
          <b-icon-check/>
        </b-input-group-text>
      </template>
      <b-form-tags
        :value="currentTask.mustHaveTags.map(i => $store.state.tags[i])"
        tag-variant="primary"
        tag-pills
        size="lg"
        separator=","
        placeholder="Add required tags..."
        remove-on-delete
      ></b-form-tags>
    </b-input-group>
    <b-form-text id="tags-remove-on-delete-help" class="mt-2 ml-5">
      Press the <kbd class="bg-light text-body border">,</kbd> key to add the tag
    </b-form-text>
    <hr/>
    <b-input-group>
      <template #prepend>
        <b-input-group-text class="d-flex flex-column justify-content-center">
          <b-icon-tags/>
          <b-icon-x/>
        </b-input-group-text>
      </template>
      <b-form-tags
        :value="currentTask.mustNotHaveTags.map(i => $store.state.tags[i])"
        tag-variant="danger"
        tag-pills
        size="lg"
        separator=","
        placeholder="Add disqualifying tags..."
        remove-on-delete
      ></b-form-tags>
    </b-input-group>
    <b-form-text id="tags-remove-on-delete-help" class="mt-2 ml-5">
      Press the <kbd class="bg-light text-body border">,</kbd> key to add the tag
    </b-form-text>

    <hr/>

    <h3>Shifts</h3>

    <b-list-group class="mb-3">
      <b-list-group-item :to="'/tasks/' + currentTaskId + '/shifts/' + shiftId" v-for="(shift, shiftId) in currentTask.shifts" :key="shiftId">
        <div class="d-flex flex-column">
          <span>
            <strong>{{formatShiftTime(shift)}}</strong>
            {{formatShiftDuration(shift)}}
          </span>
          <span class="description">{{formatShiftAssigned(shift)}}</span>
        </div>
      </b-list-group-item>
    </b-list-group>
    <b-button variant="primary" class="float-right mb-3 pr-4 pl-3 py-2"><b-icon-plus/> Add</b-button>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'TaskView',
  props: {
  },
  components: {
  },
  computed: {
    ...mapState({
      currentTask(state) {
        return state.tasks[this.$route.params.id];
      },
    }),

    currentTaskId() {
      return this.$route.params.id;
    }
  },
  methods: {
    formatShiftTime(shift) {
      const startHr = parseInt(shift.start);
      const startMin = parseInt((shift.start * 60) % 60);
      const endHr = parseInt(shift.start + shift.duration);
      const endMin = parseInt(((shift.start + shift.duration) * 60) % 60);
      return `${startHr}:${startMin.toString().padStart(2, '0')} - ${endHr}:${endMin.toString().padStart(2, '0')}`;
    },
    formatShiftDuration(shift) {
      const durationHr = parseInt(shift.duration / 4);
      const durationMin = (shift.duration % 4) * 15;
      return `(${durationHr}:${durationMin.toString().padStart(2, '0')} hour${shift.duration == 4 ? '' : 's'})`;
    },
    formatShiftAssigned(shift) {
      if (shift.assigned === null) {
        return 'Not assigned';
      } else {
        const assigned = this.$store.state.people[shift.assigned];
        return `Assigned #${assigned.num}: ${assigned.name}`;
      }
    },
  }
}
</script>

<style scoped>
.description {
  overflow-y: auto !important;
}
</style>
