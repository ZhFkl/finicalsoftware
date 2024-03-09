<template>
  <div class="dashboard-editor-container">
    <panel-group @handleSetLineChartData="handleSetLineChartData" 
    :value1='value1' :value2='value2' :value3='value3' 
    :label1='label1' :label2='label2' :label3='label3' />
  </div>
</template>

<script>
import PanelGroup from './components/PanelGroup'

const lineChartData = {
  newVisitis: {
    expectedData: [100, 120, 161, 134, 105, 160, 165],
    actualData: [120, 82, 91, 154, 162, 140, 145]
  }
}

export default {
  name: 'DashboardAdmin',
  components: {
    PanelGroup
  },
  props:{
    label1:{
      type:String,
      default:'数'
    },
    label2:{
      type:String,
      default:'数'
    },
    label3:{
      type:String,
      default:'数'
    },
    value1:{
      type:Number,
      default:0
    },
    value2:{
      type:Number,
      default:0
    },
    value3:{
      type:Number,
      default:0
    }
  },
  data() {
    return {
      lineChartData: lineChartData.newVisitis
    }
  },
  methods: {
    handleSetLineChartData(type) {
      this.lineChartData = lineChartData[type]
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}
</style>
