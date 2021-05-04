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

function objectKeyByValue (obj, val) {
  return Object.entries(obj).find(i => i[1] === val)[0];
}

function setDifference(a, b) {
  return new Set([...a].filter(x => !b.has(x)));
}

export default {
  name: 'TaskView',
  data: () => ({
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
  }
}
</script>

<style scoped>
.description {
  overflow-y: auto !important;
}
</style>
