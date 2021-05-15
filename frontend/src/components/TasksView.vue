<template>
  <div>
    <b-list-group class="mb-3">
      <b-list-group-item :to="`/${roomID}/tasks/${id}`" v-for="(task, id) in this.$store.state.tasks" :key="id">
        <div class="d-flex flex-column">
          <div class="d-flex align-items-center">
            <strong class="mr-2">{{task.name}}</strong>
            <div class="d-flex flex-wrap">
              <b-badge
                variant="primary"
                pill
                class="align-self-start mr-1 mb-1"
                v-for="tagId in task.mustHaveTags"
                :key="tagId"
              ><b-icon-check/> {{$store.state.tags[tagId]}}</b-badge>
              <b-badge
                variant="danger"
                pill
                class="align-self-start mr-1 mb-1"
                v-for="tagId in task.mustNotHaveTags"
                :key="tagId"
              ><b-icon-x/> {{$store.state.tags[tagId]}}</b-badge>
            </div>
          </div>
          <span class="description">{{task.description}}</span>
        </div>
      </b-list-group-item>
    </b-list-group>
    <div class="py-2">
      <b-button
        @click="addTask"
        variant="primary"
        class="mb-3 mr-2 pr-3 pl-1 py-2"
      ><b-icon-plus/> Add Task</b-button>
      <b-button
        @click="openRebaseModal"
        v-b-modal.rebase-modal
        class="mb-3 mr-2"
        variant="outline-primary"
      >
        <span class="h-1em">Move All Shifts</span>
      </b-button>
      <b-button
        v-b-modal.unassign-modal
        class="mb-3 mr-2"
        variant="danger"
      >
        <span class="h-1em">Unassign All Shifts</span>
      </b-button>
    </div>

    <!-- Rebase modal -->
    <b-modal
      @ok="applyRebase"
      ok-title="Apply"
      id="rebase-modal"
      title="Time Of First Shift:"
    >
      <center>
        <date-picker
          v-model="calValue"
          :is24hr="true"
          mode="dateTime"
        />
      </center>
    </b-modal>

    <!-- Unassign all modal -->
    <b-modal
      @ok="applyUnassign"
      ok-title="Unassign All Shifts"
      ok-variant="danger"
      id="unassign-modal"
      title="Are you sure?"
    >
      <strong>Would you like to remove all shift assignments?</strong>
    </b-modal>
  </div>
</template>

<script>
import DatePicker from 'v-calendar/lib/components/date-picker.umd'

export default {
  data: () => ({
    calValue: new Date(),
  }),
  computed: {
    roomID() {
      return this.$router.currentRoute.params.room;
    },
  },
  components: {
    DatePicker,
  },
  methods: {
    shiftMinStartTime() {
      let minStartTime = Infinity;
      for (const task of Object.values(this.$store.state.tasks)) {
        for (const shift of Object.values(task.shifts)) {
          if (shift.start < minStartTime) {
            minStartTime = shift.start;
          }
        }
      }

      return minStartTime;
    },
    openRebaseModal() {
      this.calValue = new Date(this.shiftMinStartTime() * 1000);
    },

    applyRebase() {
      const delta = (this.calValue.getTime() / 1000) - this.shiftMinStartTime();
      this.$store.commit('rebaseShifts', delta);
    },

    async addTask() {
      let newTaskId = await this.$store.dispatch('addTask');
      this.$router.push(`/${this.roomID}/tasks/${newTaskId}`);
    },

    applyUnassign() {
      this.$store.commit('unassignAllShifts');
    }
  },
}
</script>

<style scoped>
.description {
  white-space: pre-wrap;
}

.h-1em {
  line-height: 1.75rem;
}
</style>
