<template>
  <iframe class="iframe-container" src="http://cn2.hxdcloud.com:51112/system"></iframe>
</template>

<script>
export default {
  name: 'Task21',
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