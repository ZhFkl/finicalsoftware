<template>
  <iframe class="iframe-container" src="http://cn2.hxdcloud.com:55773/video_sentiment/"></iframe>
</template>

<script>
export default {
  name: 'Task55',
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