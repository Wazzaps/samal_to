<template>
  <div>
    <b-input-group class="mb-3">
      <template #prepend>
        <b-input-group-text><b-icon-telephone/></b-input-group-text>
      </template>
      <b-form-input
        id="input-1"
        :value="$store.state.people[$route.params.id].phoneNum"
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
  props: {
  },
  components: {
  },
  computed: {
    ...mapState({
      tagRecommendations: function (state) {
        let allTags = Object.keys(state.tags);
        let myTags = state.people[this.$route.params.id].tags;
        return allTags.filter((tagId) => {
          return myTags.indexOf(tagId) === -1;
        }).map((tagId) => {
          return [state.tags[tagId], tagId];
        });
      }
    })
  },
  methods: {
    addTag(tagId) {
      this.$store.commit('personAddTag', [this.$route.params.id, tagId]);
    },

    removeTag(tagId) {
      this.$store.commit('personRemoveTag', [this.$route.params.id, tagId]);
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
    }
  }
}
</script>

<style scoped>
</style>
