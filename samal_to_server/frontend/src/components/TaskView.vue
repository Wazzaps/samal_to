<template>
  <div>
    <b-input-group class="mb-3">
      <template #prepend>
        <b-input-group-text><b-icon-card-text/></b-input-group-text>
      </template>
      <b-form-textarea
        :value="$store.state.tasks[$route.params.id].description"
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
        :value="$store.state.tasks[$route.params.id].mustHaveTags.map(i => $store.state.tags[i])"
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
        :value="$store.state.tasks[$route.params.id].mustNotHaveTags.map(i => $store.state.tags[i])"
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
  </div>
</template>

<script>
export default {
  name: 'TaskView',
  props: {
  },
  components: {
  }
}
</script>

<style scoped>
.description {
  overflow-y: auto !important;
}
</style>
