<template>
  <div>
    <b-input-group class="mb-3">
      <template #prepend>
        <b-input-group-text><b-icon-telephone/></b-input-group-text>
      </template>
      <b-form-input
        id="tel-input"
        :value="$store.state.people[$route.params.id].phoneNum"
        @change="updatePhoneNum"
        :state="telValid"
        type="tel"
        size="lg"
        placeholder="Phone number..."
        required
      ></b-form-input>
    </b-input-group>
    <hr/>

    <!-- Tag selector -->
    <b-input-group>
      <template #prepend>
        <b-input-group-text><b-icon-tags/></b-input-group-text>
      </template>
      <b-form-tags
        input-id="person-tags"
        :value="$store.state.people[$route.params.id].tags.map(i => $store.state.tags[i])"
        @input="updateTags"
        tag-variant="primary"
        tag-pills
        size="lg"
        separator=","
        placeholder="Add tags..."
        autocomplete="off"
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
        @click="addTag(tagId)"
      >{{tag}}</b-badge>
    </div>

    <hr/>

    <!-- Assignments -->
    <h3>Assigned shifts</h3>

    <em v-if="assignedShifts.length == 0">No shifts assigned</em>

    <b-list-group class="mb-3 mt-2">
      <b-list-group-item v-for="(shift, shiftId) in assignedShifts" :key="shiftId" class="pr-1">
        <div class="d-flex flex-row">
          <div class="d-flex flex-column mr-1 w-100">
            <strong>{{shift.task.name}}</strong>
            <span>{{formatShiftTime(shift.shift)}}</span>
          </div>
          <b-button class="pad d-flex flex-column justify-content-center py-2 px-3" variant="link" @click="unassignShift(shift.taskId, shift.shiftId)">
            <b-icon-x variant="danger" font-scale="1.5"/>
          </b-button>
        </div>
      </b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
import { mapState } from 'vuex'

function objectKeyByValue (obj, val) {
  return Object.entries(obj).find(i => i[1] === val)[0];
}

function setDifference(a, b) {
  return new Set([...a].filter(x => !b.has(x)));
}

export default {
  name: 'PersonView',
  data: () => ({
    telValid: null,
    tagUpdateAge: 0,
  }),
  props: {
  },
  components: {
  },
  computed: {
    ...mapState({
      tagRecommendations(state) {
        this.tagUpdateAge; // Reactivity hack

        let allTags = Object.keys(state.tags);
        let myTags = state.people[this.$route.params.id].tags;
        return allTags.filter((tagId) => {
          return myTags.indexOf(tagId) === -1;
        }).map((tagId) => {
          return [state.tags[tagId], tagId];
        });
      },
      assignedShifts(state) {
        let shifts = [];
        for (const [taskId, task] of Object.entries(state.tasks)) {
          for (const [shiftId, shift] of Object.entries(task.shifts)) {
            if (shift.assigned == this.$route.params.id) {
              shifts.push({taskId, task, shiftId, shift});
            }
          }
        }
        return shifts;
      }
    })
  },
  methods: {
    addTag(tagId) {
      this.$store.commit('personAddTag', [this.$route.params.id, tagId]);

      // Reactivity hack
      this.$forceUpdate();
      this.tagUpdateAge++;
    },

    removeTag(tagId) {
      this.$store.commit('personRemoveTag', [this.$route.params.id, tagId]);

      // Reactivity hack
      this.$forceUpdate();
      this.tagUpdateAge++;
    },

    updateTags(nextTags) {
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
      let prevTagIds = new Set(this.$store.state.people[this.$route.params.id].tags);
      let nextTagIds = new Set(nextTags.map(tag => objectKeyByValue(this.$store.state.tags, tag)));

      // Add new tags
      let addedTagIds = setDifference(nextTagIds, prevTagIds);
      for (const tagId of addedTagIds) {
        this.addTag(tagId);
      }

      // Remove removed tags
      let removedTagIds = setDifference(prevTagIds, nextTagIds);
      for (const tagId of removedTagIds) {
        this.removeTag(tagId);
      }

      // Reactivity hack
      this.$forceUpdate();
      this.tagUpdateAge++;
    },

    updatePhoneNum(phoneNum) {
      if (phoneNum.match(/[^0-9-]/) == null) {
        this.$store.commit('personUpdatePhoneNum', [this.$route.params.id, phoneNum]);
        this.telValid = null;
      } else {
        this.telValid = false;
      }
    },

    unassignShift(taskId, shiftId) {
      this.$store.commit('taskAssignShift', [taskId, shiftId, null]);

      // Reactivity hack
      this.$forceUpdate();
      this.tagUpdateAge++;
    },

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
  }
}
</script>

<style scoped>
</style>
