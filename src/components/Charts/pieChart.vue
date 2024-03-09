<template>
  <div :id="id" :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
import resize from './mixins/resize'

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    id: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '200%'
    },
    pieData: {
      type: Array,
      default: []
    },
    isChange:{
      type:Boolean,
      default:false,
    }
  },
  data() {
    return {
      chart: null
    }
  },
  watch:{
    isChange:{
      handler() {
        this.chart.setOption({
          tooltip: {
            trigger: 'item',
            formatter: '{b0}占比: <br />{d0}%'
          },
          grid: {
            left: '5%',
            right: '5%',
            borderWidth: 0,
            top: 150,
            bottom: 95,
            textStyle: {
              color: '#fff'
            }
          },
          legend: {
            x: '5%',
            top: '10%',
            textStyle: {
              color: '#90979c'
            },
          },
          series: [{
            name: 'Rule Percentage',
            type: 'pie',
            radius: '50%',
            data: this.pieData,
            emphasis: {
                  itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                  }
            }
          }]
        });
      },
      deep:true,
    }
  },
  mounted() {
    this.initChart()
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(document.getElementById(this.id))
      
      this.chart.setOption({
        tooltip: {
          trigger: 'item',
          formatter: '{b0}占比: <br />{d0}%'
        },
        grid: {
          left: '5%',
          right: '5%',
          borderWidth: 0,
          top: 150,
          bottom: 95,
          textStyle: {
            color: '#fff'
          }
        },
        legend: {
          x: '5%',
          top: '10%',
          textStyle: {
            color: '#90979c'
          },
        },
        series: [{
          name: 'Rule Percentage',
          type: 'pie',
          radius: '50%',
          data: this.pieData,
          emphasis: {
                itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        },
        ]
      })
    }
  }
}
</script>
