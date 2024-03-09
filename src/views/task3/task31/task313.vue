<template>
  <div class="my-wrapper">
    <div class="my-title">
      周期模式挖掘
      <!-- <i class="el-icon-back" v-if="!originFlag" @click="originFlag = true"
        >返回</i
      > -->
    </div>
    <div class="my-content">
      <el-row type="flex" align="middle">
        <el-col :span="4">请选择金融数据集：</el-col>
        <el-col :span="10">
          <el-select v-model="dataSource" size="small" style="width: 100%">
            <el-option
              v-for="item in sourceOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
      </el-row>
      <el-row type="flex" align="middle" style="margin-bottom:10px;margin-top:10px">
        <el-col :span="4">请选择时间的间隔：</el-col>
        <el-col :span="10">
          <!-- <el-date-picker
            v-model="timeRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期">
          </el-date-picker> -->
          <el-select v-model="timeRange" size="small" style="width: 100%">
            <el-option
              v-for="item in timeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
      </el-row>
      <el-row type="flex" align="middle">
        <el-col :span="4">请选择周期次数：</el-col>
        <el-col :span="10">
          <el-select v-model="supportLevel" size="small" style="width: 100%">
            <el-option
              v-for="item in supportOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="5" :offset="1">
          <!-- <el-button type="primary" size="small" @click="showStatistic=dataSource?true:false"
            >查看统计信息</el-button
          > -->
          <el-button
            type="primary"
            size="small"
            @click="digData"
          >规则挖掘</el-button>
        </el-col>
      </el-row>

      <!-- <el-row class="panel-group" v-if="dataSource&&showStatistic">
        <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
          <div class="card-panel">
            <div class="card-panel-icon-wrapper icon-people">
              <svg-icon icon-class="tree" class-name="card-panel-icon" />
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">
                边数
              </div>
              <count-to :start-val="0"
              :end-val='dataSource=="before2015"?statisticInfo[0].edgeNum:statisticInfo[1].edgeNum'
              :duration="2600" class="card-panel-num" />
            </div>
          </div>
        </el-col>
        <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
          <div class="card-panel">
            <div class="card-panel-icon-wrapper icon-people">
              <svg-icon icon-class="star" class-name="card-panel-icon" />
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">
                节点数
              </div>
              <count-to :start-val="0"
                        :end-val="dataSource=='before2015'?statisticInfo[0].nodeNum:statisticInfo[1].nodeNum"
                        :duration="2600" class="card-panel-num" />
            </div>
          </div>
        </el-col>
        <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col" style="text-align:center">
          <div class="card-panel">
           <el-image :src="img.path" fit="contain" style="height:110px"/>
          </div>
        </el-col>
      </el-row> -->
      <!-- <adminDashboard style="margin-top: 15px" v-if="dataSource&&showStatistic"
      :value1='dataSource=="before2015"?statisticInfo[0].nodeNum:statisticInfo[1].nodeNum'
      :value2='dataSource=="before2015"?statisticInfo[0].edgeNum:statisticInfo[1].edgeNum'
      :label1='"节点数"' :label2='"边数"' ></adminDashboard> -->
    </div>
    <div v-if="!originFlag" class="my-content">
      <!-- <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="label" label="统计项" width="230">
        </el-table-column>
        <el-table-column prop="value" label="统计结果"> </el-table-column>
      </el-table> -->
      <el-row class="rule-board">
        <el-col :span="12">
          <el-card style="width: 90%; height: 450px; margin-top: 10px;margin-left: 5%;text-align:center">
            <div style="height:350px">
              <tmp-graph
                :graph-data="graphDataList[(rulePage.curPage-1)*rulePage.pageSize].data"
                :hulls="graphDataList[(rulePage.curPage-1)*rulePage.pageSize].hulls"
                :ind="1"
                :pic-label="'实例' + parseInt((rulePage.curPage-1)*rulePage.pageSize+1)"
                :is-change="changeRule"
                :is-destroy="changeRule"
              />
            </div>
          </el-card>
        </el-col>
        <el-col v-if="(rulePage.curPage-1)*rulePage.pageSize+1<graphDataList.length" :span="12">
          <el-card style="width: 90%; height: 450px; margin-top: 10px;margin-left: 5%;text-align:center">
            <div style="height:350px">
              <tmp-graph
                :graph-data="graphDataList[(rulePage.curPage-1)*rulePage.pageSize+1].data"
                :hulls="graphDataList[(rulePage.curPage-1)*rulePage.pageSize+1].hulls"
                :ind="2"
                :pic-label="'实例' + parseInt((rulePage.curPage-1)*rulePage.pageSize+2)"
                :is-change="changeRule"
                :is-destroy="changeRule"
              />
            </div>
          </el-card>
        </el-col>

      </el-row>

      <el-pagination
        background
        layout="prev, pager, next"
        :total="rulePage.total"
        :current-page="rulePage.curPage"
        :page-size="rulePage.pageSize"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script>
import TmpGraph from './../../../components/myGraph.vue'
import * as apiTopic1 from '@/api/topic1'
export default {
  name: 'Task313',
  components: { TmpGraph },
  data() {
    return {
      ind: 1,
      img: {
        url: '',
        path: require('@/assets/topic1.1.jpg')
      },
      tableData: [],
      originFlag: true,
      graphData: {},
      hulls: [],
      graphDataList: [],
      supportOptions: [
        {
          label: '4',
          value: '4time'
        }
      ],
      supportLevel: '',
      // graphMap:null,
      instanceVisible: false,
      instanceTitle: '',
      instanceList: [],
      activeInd: 0,
      activeId: -1,
      changeInstance: false,
      changeRule: false,
      statisticInfo: {
        nodeNum: 40000,
        edgeNum: 126482,
        ruleNum: 1067,
        runtime: 0
      },
      dataSource: '',
      sourceOptions: [
        // {
        //   label: "DATA1 供应商持股关系 （十万级）",
        //   value: 'after2015',
        // },
        {
          label: '供应商持股关系',
          value: 'customer'
        }
      ],
      showStatistic: false,
      timeRange: '',
      timeOptions: [
        {
          label: '一年',
          value: '3core'
        }
        // {
        //   label: "两年",
        //   value: '2year',
        // },
      ],
      rulePage: {
        total: 3,
        curPage: 1,
        pageSize: 2
      }
    }
  },

  created() {
    apiTopic1.getMineInfo().then(res => {
      console.log(res)
      this.statisticInfo = [{
        nodeNum: parseInt(res.data['data1_节点数'].split(',').join('')),
        edgeNum: parseInt(res.data['data1_边数'].split(',').join(''))
        // ruleNum:parseInt(res.data['稳定时序规则数'].split(',').join('')),
        // runtime:res.data['运行时间'],
        // runInterval:res.data['时间间隔'],
      }, {
        nodeNum: parseInt(res.data['data2_节点数'].split(',').join('')),
        edgeNum: parseInt(res.data['data2_边数'].split(',').join(''))
        // ruleNum:parseInt(res.data['稳定时序规则数'].split(',').join('')),
        // runtime:res.data['运行时间'],
        // runInterval:res.data['时间间隔'],
      }]
      // let support = res.data['支持度'];
      // this.supportOptions = Array.isArray(support)?
      //   support.map((val,ind)=>{return {label:val,value:ind}}):
      //   [{label:support,value:1}];
      // let timeRange = res.data['时间间隔'];
      // this.timeOptions = Array.isArray(timeRange)?
      //   timeRange.map((val,ind)=>{return {label:val,value:ind}}):
      //   [{label:timeRange,value:1}];
    })
  },
  mounted() {
    this.tableData = [
      {
        label: 'xxx',
        value: 1
      },
      {
        label: 'xxxx',
        value: 2
      }
    ]
  },
  methods: {
    handlePageChange(val) {
      console.log(`当前页: ${val}`)
      this.rulePage.curPage = val
      this.changeRule = !this.changeRule
      console.log((this.rulePage.curPage - 1) * this.rulePage.pageSize + 1, this.graphDataList.length, (this.rulePage.curPage - 1) * this.rulePage.pageSize + 1 < this.graphDataList.length)
    },

    fetchStatistic() {

    },
    digData() {
      if (!(this.timeRange && this.dataSource && this.supportLevel)) {
        this.$message({
          message: '请选择完全！',
          type: 'warning'
        })
        return
      }
      console.log(this.timeRange, this.dataSource, this.supportLevel)
      apiTopic1
        .digSubgraph({
          time: this.timeRange,
          data: this.dataSource,
          support: this.supportLevel
        })
        .then((res) => {
          this.changeRule = !this.changeRule
          console.log(res)
          this.graphDataList = []
          // this.graphMap=new Map();
          let counter = 1
          for (const i of res.data.patterns_list) {
            const tmpdata = {}
            tmpdata.data = {}
            tmpdata.data.nodes = []
            tmpdata.data.edges = []
            tmpdata.hulls = []

            const hyperedge = i.instances[0].hyperedges
            const uniqueNodes = []
            for (const j of hyperedge) {
              const members = []
              for (const k of j['ids']) {
                if (uniqueNodes.indexOf(k.name) < 0) {
                  uniqueNodes.push(k.name)
                  tmpdata.data.nodes.push({
                    id: k['name'],
                    label: k['name'],
                    size: 30,
                    style: {
                      fill: '#f2e394'
                    }
                  })
                }
                members.push(k.name)
              }
              tmpdata.hulls.push({
                id: 'hull' + counter++,
                padding: 10,
                members: members,
                style: {
                  fill: '#000',
                  stroke: '#fff'
                }
              })
            }
            this.graphDataList.push(tmpdata)
          }
          this.rulePage.total = this.graphDataList.length
          this.rulePage.curPage = 1
          this.originFlag = false
        })
        .catch((err) => {
          console.log(err)
        })
    }
  }
}
</script>
<style scoped>
.el-pagination{
  margin-top:20px;
}
.el-dialog__wrapper{
  height: 90vh;
}
.el-dialog__body{
  margin-top: 5vh;
}
#dialog-content{
  height: 400px;
  overflow: auto;
  margin-right:-10px;
  text-align: centers;
}
.el-date-editor--daterange.el-input, .el-date-editor--daterange.el-input__inner, .el-date-editor--timerange.el-input, .el-date-editor--timerange.el-input__inner {
    width: 535px;
}
</style>

<style lang="scss" scoped>
.panel-group {
  margin-top: 18px;
  padding: 32px;
  background-color: #f6f7f7;
  position: relative;

  .card-panel-col {
    margin-right:20px;
  }

  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
    border-color: rgba(0, 0, 0, .05);

    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }

      .icon-people {
        background: #40c9c6;
      }

      .icon-message {
        background: #36a3f7;
      }

      .icon-money {
        background: #f4516c;
      }

      .icon-shopping {
        background: #34bfa3
      }
    }

    .icon-people {
      color: #40c9c6;
    }

    .icon-message {
      color: #36a3f7;
    }

    .icon-money {
      color: #f4516c;
    }

    .icon-shopping {
      color: #34bfa3
    }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }

    .card-panel-icon {
      float: left;
      font-size: 48px;
    }

    .card-panel-description {
      float: right;
      font-weight: bold;
      margin: 26px;
      margin-left: 0px;

      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }

      .card-panel-num {
        font-size: 20px;
      }
    }
  }
}

@media (max-width:550px) {
  .card-panel-description {
    display: none;
  }

  .card-panel-icon-wrapper {
    float: none !important;
    width: 100%;
    height: 100%;
    margin: 0 !important;

    .svg-icon {
      display: block;
      margin: 14px auto !important;
      float: none !important;
    }
  }
}
</style>
