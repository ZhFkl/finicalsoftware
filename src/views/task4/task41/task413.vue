<template>
  <iframe class="iframe-container" src="http://cn2.hxdcloud.com:53000/DataIntegration/PublicOpinion"></iframe>
</template>

<script>
export default {
  name: 'Task412',
  data() {
    return {
      user: {},
      activeTab: 'activity'
    }
  }
}
</script>
<style>
.iframe-container{
    width: 100%;
    height: 100%;
}
</style>