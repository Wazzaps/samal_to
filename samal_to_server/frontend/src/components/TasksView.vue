<template>
  <div>
    <b-list-group class="mb-3">
      <b-list-group-item :to="'/tasks/' + id" v-for="(task, id) in this.$store.state.tasks" :key="id">
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
    <b-button variant="primary" class="float-right mb-3 pr-4 pl-3 py-2"><b-icon-plus/> Add</b-button>
  </div>
</template>

<script>
export default {
}
</script>

<style scoped>
.description {
  white-space: pre-wrap;
}
</style>
