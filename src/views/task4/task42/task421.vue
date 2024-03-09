<template>
  <iframe class="iframe-container" src="http://cn2.hxdcloud.com:53000/VisualAnalysis/StructureGraph"></iframe>
</template>

<script>
export default {
  name: 'Task421',
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