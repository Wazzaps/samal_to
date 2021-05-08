<template>
  <div>
    <b-input-group class="mb-3">
      <template #prepend>
        <b-input-group-text><b-icon-card-text/></b-input-group-text>
      </template>
      <b-form-textarea
        :value="currentTask.description"
        @change="updateTaskDescription"
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
        @input="updateRequiredTags"
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

    <div class="d-flex flex-wrap mt-2 ml-5">
      <b-badge
        variant="primary"
        pill
        class="align-self-start mr-1 mb-1"
        v-for="[tag, tagId] in tagRecommendations"
        :key="tagId"
        href="#"
        @click="addRequiredTag(tagId)"
      >{{tag}}</b-badge>
    </div>

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
        @input="updateDisqualifyingTags"
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

    <div class="d-flex flex-wrap mt-2 ml-5">
      <b-badge
        variant="danger"
        pill
        class="align-self-start mr-1 mb-1"
        v-for="[tag, tagId] in tagRecommendations"
        :key="tagId"
        href="#"
        @click="addDisqualifyingTag(tagId)"
      >{{tag}}</b-badge>
    </div>

    <hr/>

    <h3>Shifts</h3>

    <em v-if="Object.keys(currentTask.shifts).length == 0">No shifts</em>

    <div v-for="(shifts, date) in groupedShifts" :key="date">
      <h5>– {{date}} –</h5>
      <b-list-group class="mb-3 mt-2">
      <b-list-group-item @click="openShiftEditModal(shift.shiftId)" v-b-modal.shift-modal v-for="shift in shifts" :key="shift.shiftId" class="pr-1">
        <div class="d-flex flex-row">
          <div class="d-flex flex-column mr-1 w-100">
            <span>
              <strong>{{formatShiftTime(shift.shift)}}</strong>
              {{formatShiftDuration(shift.shift)}}
            </span>
            <span class="description">{{formatShiftAssigned(shift.shift)}}</span>
          </div>
          <div class="pad d-flex flex-column justify-content-center py-2 px-3">
            <b-icon-pencil-fill variant="primary"/>
          </div>
        </div>
      </b-list-group-item>
    </b-list-group>
    </div>

    <b-button
      @click="addShift"
      variant="primary"
      class="float-right mb-3 pr-4 pl-3 py-2"
    ><b-icon-plus/> Add</b-button>

    <b-modal id="shift-modal" title="Edit Shift">
      <h5>Shift time:</h5>
      <center>
        <date-picker
          v-model="calValue"
          :attributes='calAttrs'
          :is24hr="true"
          mode="dateTime"
          is-range
        />
      </center>

      <h5 class="mt-4">Assigned:</h5>
      <b-form-select
        @change="updateShiftAssignment"
        :value="currentTask.shifts[0] ? currentTask.shifts[modalShiftId].assigned : null"
      >
        <b-form-select-option :value="null">Not assigned</b-form-select-option>
        <b-form-select-option
          :value="personId"
          v-for="([personId, person]) in Object.entries(this.$store.state.people)"
          :key="personId"
        >#{{person.num}}: {{person.name}}</b-form-select-option>
      </b-form-select>

      <template #modal-footer="{ ok }">
        <b-button variant="danger" @click="deleteShift()">
          Delete Shift
        </b-button>
        <b-button variant="primary" @click="ok()">
          OK
        </b-button>
      </template>
    </b-modal>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import DatePicker from 'v-calendar/lib/components/date-picker.umd'

function objectKeyByValue (obj, val) {
  return Object.entries(obj).find(i => i[1] === val)[0];
}

function setDifference(a, b) {
  return new Set([...a].filter(x => !b.has(x)));
}

export default {
  name: 'TaskView',
  data: () => ({
    modalShiftId: 0,
    tagUpdateAge: 0,
    calAttrs: [
      {
        key: 'today',
        highlight: {
          fillMode: 'outline',
        },
        dates: new Date(),
      },
    ],
    calValue: {}
  }),
  props: {
  },
  components: {
    DatePicker,
  },
  computed: {
    ...mapState({
      tagRecommendations(state) {
        this.tagUpdateAge; // Reactivity hack

        let allTags = Object.keys(state.tags);
        let myTags = state.tasks[this.$route.params.id].mustHaveTags + state.tasks[this.$route.params.id].mustNotHaveTags;
        return allTags.filter((tagId) => {
          return myTags.indexOf(tagId) === -1;
        }).map((tagId) => {
          return [state.tags[tagId], tagId];
        });
      },
      currentTask(state) {
        return state.tasks[this.$route.params.id];
      },
      groupedShifts(state) {
        this.tagUpdateAge; // Reactivity hack

        let shifts = [];
        for (const [shiftId, shift] of Object.entries(this.currentTask.shifts)) {
          shifts.push({shiftId, shift});
        }
        shifts.sort((shiftA, shiftB) => {
          return shiftA.shift.start > shiftB.shift.start ? 1 : -1;
        });

        if (shifts.length == 0) {
          return [];
        }

        let days = {};
        let curDate = null;
        for (const shift of shifts) {
          const nextDate = new Date(shift.shift.start * 1000).toLocaleString('sv', {timeZoneName: 'short'}).split(" ")[0];
          if (curDate != nextDate) {
            days[nextDate] = [];
          }
          days[nextDate].push(shift);
          curDate = nextDate;
        }
        return days;
      },
    }),

    currentTaskId() {
      return this.$route.params.id;
    }
  },
  watch: {
    calValue(newDate) {
      this.$store.commit('shiftSetTime', [this.$route.params.id, this.modalShiftId, newDate]);
    }
  },
  methods: {
    openShiftEditModal(shiftId) {
      const shift = this.currentTask.shifts[shiftId];
      this.calValue = {
        start: new Date(shift.start * 1000),
        end: new Date((shift.start + shift.duration) * 1000),
      };

      this.modalShiftId = shiftId;
    },

    updateShiftAssignment(personId) {
      this.$store.commit('taskAssignShift', [this.$route.params.id, this.modalShiftId, personId]);

      // Reactivity hack
      this.$forceUpdate();
      this.tagUpdateAge++;
    },

    formatShiftTime(shift) {
      let startTime = new Date(shift.start * 1000).toLocaleString('sv', {timeZoneName: 'short'}).split(" ")[1];
      startTime = startTime.substr(0, startTime.lastIndexOf(":"));
      let endTime = new Date((shift.start + shift.duration) * 1000).toLocaleString('sv', {timeZoneName: 'short'}).split(" ")[1];
      endTime = endTime.substr(0, endTime.lastIndexOf(":"));
      return `${startTime} - ${endTime}`;
    },

    formatShiftDuration(shift) {
      const durationHr = parseInt(shift.duration / (60 * 60));
      const durationMin = (shift.duration % (60 * 60));
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

    updateTaskDescription(description) {
      this.$store.commit('taskUpdateDescription', [this.$route.params.id, description.trim() + "\n"]);
    },

    addRequiredTag(tagId) {
      this.$store.commit('taskAddRequiredTag', [this.$route.params.id, tagId]);

      // Reactivity hack
      this.$forceUpdate();
      this.tagUpdateAge++;
    },

    removeRequiredTag(tagId) {
      this.$store.commit('taskRemoveRequiredTag', [this.$route.params.id, tagId]);

      // Reactivity hack
      this.$forceUpdate();
      this.tagUpdateAge++;
    },

    updateRequiredTags(nextTags) {
      // Create all new tags
      const newTags = setDifference(
        nextTags,
        new Set(Object.values(this.$store.state.tags)),
      );
      let maxTagId = Math.max(-1, ...Object.keys(this.$store.state.tags));
      for (const tagName of newTags) {
        this.$store.commit('createTag', [++maxTagId, tagName]);
      }

      // Update differences
      let prevTagIds = new Set(this.$store.state.tasks[this.$route.params.id].mustHaveTags);
      let nextTagIds = new Set(nextTags.map(tag => objectKeyByValue(this.$store.state.tags, tag)));

      // Add new tags
      let addedTagIds = setDifference(nextTagIds, prevTagIds);
      for (const tagId of addedTagIds) {
        this.addRequiredTag(tagId);
      }

      // Remove removed tags
      let removedTagIds = setDifference(prevTagIds, nextTagIds);
      for (const tagId of removedTagIds) {
        this.removeRequiredTag(tagId);
      }

      // Reactivity hack
      this.$forceUpdate();
      this.tagUpdateAge++;
    },

    addDisqualifyingTag(tagId) {
      this.$store.commit('taskAddDisqualifyingTag', [this.$route.params.id, tagId]);

      // Reactivity hack
      this.$forceUpdate();
      this.tagUpdateAge++;
    },

    removeDisqualifyingTag(tagId) {
      this.$store.commit('taskRemoveDisqualifyingTag', [this.$route.params.id, tagId]);

      // Reactivity hack
      this.$forceUpdate();
      this.tagUpdateAge++;
    },

    updateDisqualifyingTags(nextTags) {
      // Create all new tags
      const newTags = setDifference(
        nextTags,
        new Set(Object.values(this.$store.state.tags)),
      );
      let maxTagId = Math.max(-1, ...Object.keys(this.$store.state.tags));
      for (const tagName of newTags) {
        this.$store.commit('createTag', [++maxTagId, tagName]);
      }

      // Update differences
      let prevTagIds = new Set(this.$store.state.tasks[this.$route.params.id].mustNotHaveTags);
      let nextTagIds = new Set(nextTags.map(tag => objectKeyByValue(this.$store.state.tags, tag)));

      // Add new tags
      let addedTagIds = setDifference(nextTagIds, prevTagIds);
      for (const tagId of addedTagIds) {
        this.addDisqualifyingTag(tagId);
      }

      // Remove removed tags
      let removedTagIds = setDifference(prevTagIds, nextTagIds);
      for (const tagId of removedTagIds) {
        this.removeDisqualifyingTag(tagId);
      }

      // Reactivity hack
      this.$forceUpdate();
      this.tagUpdateAge++;
    },

    async addShift() {
      let newShiftId = await this.$store.dispatch('taskAddShift', this.currentTaskId);
      this.openShiftEditModal(newShiftId);

      // Reactivity hack
      this.$forceUpdate();
      this.tagUpdateAge++;

      // Show modal
      this.$bvModal.show('shift-modal');
    },

    deleteShift() {
      // Hide modal
      this.$bvModal.hide('shift-modal');
      const modalShiftId = this.modalShiftId;
      this.modalShiftId = 0;

      // Delete the shift
      this.$store.commit('taskDeleteShift', [this.currentTaskId, modalShiftId]);

      // Reactivity hack
      this.$forceUpdate();
      this.tagUpdateAge++;
    }
  }
}
</script>

<style scoped>
.description {
  overflow-y: auto !important;
}
</style>

<style>
.vc-date-time {
  /* margin: auto !important; */
  text-align: center;
  padding-left: 0.3rem;
  padding-right: 1rem;
}

.vc-time {
  justify-content: center;
}

.vc-date {
  display: inline-flex !important;
}

#shift-modal .modal-footer {
  justify-content: space-between;
}
</style>
