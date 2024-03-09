<template>
  <div class="dashboard-container" style="width:100%;height:100%">
    <component :is="currentRole" />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import adminDashboard from './admin'
import editorDashboard from './editor'
import HyperReasoning from './HyperReasoning.vue'

export default {
  name: 'Dashboard',
  components: { adminDashboard, editorDashboard, HyperReasoning},
  data() {
    return {
      currentRole: 'HyperReasoning'
    }
  },
  computed: {
    ...mapGetters([
      'roles'
    ])
  },
  created() {
  }
}
</script>
