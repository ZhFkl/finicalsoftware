<template>
  <div class="my-wrapper">
    <div class="my-title">
      基于深度学习的可解释性规则挖掘技术
      <!-- <i class="el-icon-back" v-if="!originFlag" @click="originFlag = true"
        >返回</i
      > -->
    </div>
    <div class="my-content">
      <el-row type="flex" align="middle">
        <el-col :span="4">请选择金融数据集：</el-col>
        <el-col :span="10">
          <el-select size="small" style="width: 100%" v-model="dataSource">
            <el-option
              v-for="item in sourceOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
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
          <el-select size="small" style="width: 100%" v-model="timeRange">
            <el-option
              v-for="item in timeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-col>
      </el-row>
      <el-row type="flex" align="middle">
        <el-col :span="4">请选择支持度程度：</el-col>
        <el-col :span="10">
          <el-select size="small" style="width: 100%" v-model="supportLevel">
            <el-option
              v-for="item in supportOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="5" :offset="1">
          <el-button type="primary" size="small" @click="showStatistic=dataSource?true:false"
            >查看统计信息</el-button
          >
          <el-button type="primary" size="small" @click="digData"
            >规则挖掘</el-button
          >
        </el-col>
      </el-row>


      <el-row class="panel-group" v-if="dataSource&&showStatistic">
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
      </el-row>
      <!-- <adminDashboard style="margin-top: 15px" v-if="dataSource&&showStatistic"
      :value1='dataSource=="before2015"?statisticInfo[0].nodeNum:statisticInfo[1].nodeNum' 
      :value2='dataSource=="before2015"?statisticInfo[0].edgeNum:statisticInfo[1].edgeNum'
      :label1='"节点数"' :label2='"边数"' ></adminDashboard> -->
    </div>
    <div class="my-content"  v-if="!originFlag">
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
                :graphData="graphDataList[(rulePage.curPage-1)*rulePage.pageSize].data"
                :hulls="graphDataList[(rulePage.curPage-1)*rulePage.pageSize].hulls"
                :ind="1"
                :picLabel="'规则' + parseInt((rulePage.curPage-1)*rulePage.pageSize+1)" 
                :isChange="changeRule"
                :isDestroy="changeRule"
              ></tmp-graph>
              </div>
              <el-button type="primary" size="mini"
              style="margin-top:10px"
              @click="showInstance(graphDataList[(rulePage.curPage-1)*rulePage.pageSize].id,(rulePage.curPage-1)*rulePage.pageSize+1)">
                查看规则{{parseInt((rulePage.curPage-1)*rulePage.pageSize+1)}}实例
              </el-button>
          </el-card>
        </el-col>
        <el-col :span="12" v-if="(rulePage.curPage-1)*rulePage.pageSize+1<graphDataList.length">
          <el-card style="width: 90%; height: 450px; margin-top: 10px;margin-left: 5%;text-align:center">
            <div style="height:350px">
              <tmp-graph
                :graphData="graphDataList[(rulePage.curPage-1)*rulePage.pageSize+1].data"
                :hulls="graphDataList[(rulePage.curPage-1)*rulePage.pageSize+1].hulls"
                :ind="2"
                :picLabel="'规则' + parseInt((rulePage.curPage-1)*rulePage.pageSize+2)" 
                :isChange="changeRule"
                :isDestroy="changeRule"
              ></tmp-graph>
              </div>
              <el-button type="primary" size="mini"
              style="margin-top:10px"
              @click="showInstance(graphDataList[(rulePage.curPage-1)*rulePage.pageSize+1].id,(rulePage.curPage-1)*rulePage.pageSize+2)">
                查看规则{{parseInt((rulePage.curPage-1)*rulePage.pageSize+2)}}实例
              </el-button>
          </el-card>
        </el-col>
        <!-- <div
          style="width: 90%; height: 450px; margin-top: 10px;margin-left: 5%;text-align:center"
          v-for="(item, index) in graphDataList"
          :key="index"
        >
          <div style="height:350px">
          <tmp-graph
            :graphData="item.data"
            :hulls="item.hulls"
            :ind="item.index"
            :picLabel="'规则' + item.index" 
          ></tmp-graph>
          </div>
          <el-button type="primary" size="mini"
          style="margin-top:10px"
          @click="showInstance(item.id,item.index)">
            查看规则{{item.index}}实例
          </el-button>
        </div> -->
      </el-row>
      
      <el-pagination
        background
        layout="prev, pager, next"
        :total="rulePage.total" 
        :current-page="rulePage.curPage"
        :page-size="rulePage.pageSize"
        @current-change="handlePageChange">
      </el-pagination>
    </div>
      <el-dialog
        :title="instanceTitle"
        :visible.sync="instanceVisible"
        width="60%"
        center>
        <div id='dialog-content'>
          <div v-if="instanceList&&instanceList[activeInd]"
          style="width: 90%; height: 350px;margin-left: 5%;margin-top: 10px"
          >
            <tmp-graph
              :graphData="instanceList[activeInd].data"
              :hulls="instanceList[activeInd].hulls"
              :ind="instanceList[activeInd].index"
              :picLabel="'实例' + (activeInd+1)" 
              :isChange="changeInstance"
              :isDestroy="changeInstance"
            ></tmp-graph>
            <el-button type="primary" @click="randomInstance" style="float:right">
              随机查看其他实例
            </el-button>
          </div>   
        </div>     
      </el-dialog>
  </div>
</template>

<script>
import TmpGraph from "./../../../components/myGraph.vue";
import adminDashboard from "./admin";
import tmpData from "@/js/data";
import * as apiTopic1 from "@/api/topic1";
import CountTo from 'vue-count-to'
export default {
  name: "topic1-1",
  components: { TmpGraph, adminDashboard, CountTo },
  data() {
    return {
      img: {
        url: '',
        path:require('@/assets/topic1.1.jpg')
      },
      tableData: [],
      originFlag: true,
      graphData: {},
      hulls: [],
      graphDataList: [],
      supportOptions: [
        {
          label: "0.5",
          value: '0.5',
        },
        {
          label: "0.7",
          value: '0.7',
        },
      ],
      supportLevel: "",
      graphMap:null,
      instanceVisible:false,
      instanceTitle:'',
      instanceList:[],
      activeInd:0,
      activeId:-1,
      changeInstance:false,
      changeRule:false,
      statisticInfo:{
        nodeNum:40000,
        edgeNum:126482,
        ruleNum:1067,
        runtime:0,
      },
      dataSource:'',
      sourceOptions: [
        {
          label: "DATA1 供应商持股关系 （十万级）",
          value: 'after2015',
        },
        {
          label: "DATA1 供应商持股关系 （万级）",
          value: 'before2015',
        },
      ],
      showStatistic:false,
      timeRange:'',
      timeOptions: [
        {
          label: "一年",
          value: '1year',
        },
        {
          label: "两年",
          value: '2year',
        },
      ],
      rulePage:{
        total:3,
        curPage:1,
        pageSize:2
      }
    };
  },

  created() {
    apiTopic1.getMineInfo().then(res=>{
      console.log(res)
      this.statisticInfo=[{
        nodeNum:parseInt(res.data['data1_节点数'].split(',').join('')),
        edgeNum:parseInt(res.data['data1_边数'].split(',').join('')),
        // ruleNum:parseInt(res.data['稳定时序规则数'].split(',').join('')),
        // runtime:res.data['运行时间'],
        // runInterval:res.data['时间间隔'],
      },{
        nodeNum:parseInt(res.data['data2_节点数'].split(',').join('')),
        edgeNum:parseInt(res.data['data2_边数'].split(',').join('')),
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
        label: "xxx",
        value: 1,
      },
      {
        label: "xxxx",
        value: 2,
      },
    ];
  },
  methods: {
    handlePageChange(val) {
        console.log(`当前页: ${val}`);
        this.rulePage.curPage =  val;
        this.changeRule  = !this.changeRule;
        console.log((this.rulePage.curPage-1)*this.rulePage.pageSize+1,this.graphDataList.length,(this.rulePage.curPage-1)*this.rulePage.pageSize+1<this.graphDataList.length)
      },
    randomInstance(){
      if(!this.graphMap||!this.graphMap.has(this.activeId)){
        this.$notify('该规则没有实例');
        return;
      }
      let list=this.graphMap.get(this.activeId);
      this.activeInd = (this.activeInd+1)%list.length;
      this.changeInstance = !this.changeInstance;
    },
    showInstance(id,index){
      console.log(id,index)
      this.activeId = id;
      if(!this.graphMap||!this.graphMap.has(id)){
        this.$notify('该规则没有实例');
        return;
      }
      this.activeInd = 0;
      this.instanceTitle = '规则'+index+'的实例';
      this.instanceList=[];
      let list=this.graphMap.get(id);
      let ind = index*10;
      let counter = 1;
      console.log(list)
      for(let i of list){
        let uniqueNodes = [];
        let tmpdata = {};
        tmpdata.data = {};
        tmpdata.data.nodes = [];
        tmpdata.data.edges = [];
        tmpdata.hulls = [];
        tmpdata.id=i.id;
        tmpdata.index = ind++;

            for (let j of i["hyperedges"]) {
              // console.log(j);
              let member = [];
              //加入超边的描述节点，opacity0隐藏
              member.push(j["label"] + counter);
              tmpdata.data.nodes.push({
                id: j["label"] + counter,
                label: j["name"]+'-'+j["label"]+'\n'+j['beg_time']+'-'+j['end_time'],
                size: 30,
                style: {
                  stroke: "#ff0000",
                  fillOpacity: 0,
                  strokeOpacity: 0,
                },
              });

              //加入超边组成的点
              for (let k of j["ids"]) {
                // console.log(k);
                if (k === "beg_time" || k === "end_time") {
                  continue;
                }
                member.push(k["id"] + "");
                if (uniqueNodes.indexOf(k["id"]) < 0) {
                  uniqueNodes.push(k["id"]);
                  tmpdata.data.nodes.push({
                    id: k["id"] + "",
                    label: k["name"],
                    size: 30,
                    style: {
                      fill: "#f2e394"// k["risk"] === 1 ? "#588c73" : "#f2e394",
                    },
                  });
                }
                // console.log(k["id"] + "", j["label"] + counter);
                tmpdata.data.edges.push({
                  id:'edge'+tmpdata.data.edges.length,
                  source: k["id"] + "",
                  target: j["label"] + counter,
                  size: 3,
                  style: {
                    stroke: "#ff0000",
                    opacity: 0,
                    fillOpacity: 0,
                    strokeOpacity: 0,
                  },
                });
              }
              //绘制超边
              tmpdata.hulls.push({
                id: "hull" + counter++,
                padding: 10,
                members: member,
                style: {
                  fill: "#000",
                  stroke: "#fff",
                },
              });
            }
            this.instanceList.push(tmpdata);
      }
      this.changeInstance = !this.changeInstance;
      this.instanceVisible=true;
      console.log(this.instanceList,this.instanceVisible,this.instanceTitle)
    },
    fetchStatistic(){

    },
    digData() {
      if(!(this.timeRange&&this.dataSource&&this.supportLevel)){
         this.$message({
          message: '请选择完全！',
          type: 'warning'
        });
        return;
      }
      console.log(this.timeRange,this.dataSource,this.supportLevel);
      apiTopic1
        .digSubgraph({
          time:this.timeRange,
          data:this.dataSource,
          support:this.supportLevel
        })
        .then((res) => {
          this.changeRule  = !this.changeRule;
          console.log(res);
          this.graphDataList = [];
          this.graphMap=new Map();

          let ind = 1;
          let counter = 1;
          for (let i of res.data.patterns_list) {
            if(this.graphMap.has(i.id)){
              this.graphMap.get(i.id).concat(i.instances)
            }else{
              this.graphMap.set(i.id,i.instances)
            }
              
            let uniqueNodes = [];
            // console.log(i);
            let tmpdata = {};
            tmpdata.data = {};
            tmpdata.data.nodes = [];
            tmpdata.data.edges = [];
            tmpdata.hulls = [];
            tmpdata.id=i.id;

            // tmpdata.risk = i.risk===1?'高风险':'低风险';
            tmpdata.index = ind++;

            for (let j of i["pattern_edge"]) {
              // console.log(j);
              let member = [];
              //加入超边的描述节点，opacity0隐藏
              member.push(j["label"] + counter);
              tmpdata.data.nodes.push({
                id: j["label"] + counter,
                label: j["label"],
                size: 30,
                style: {
                  stroke: "#ff0000",
                  fillOpacity: 0,
                  strokeOpacity: 0,
                },
              });

              //加入超边组成的点
              for (let k of j["ids"]) {
                // console.log(k);
                if (k === "beg_time" || k === "end_time") {
                  continue;
                }
                member.push(k["id"] + "");
                if (uniqueNodes.indexOf(k["id"]) < 0) {
                  uniqueNodes.push(k["id"]);
                  tmpdata.data.nodes.push({
                    id: k["id"] + "",
                    label: k["name"],
                    size: 30,
                    style: {
                      fill: "#f2e394",
                    },
                  });
                }
                // console.log(k["id"] + "", j["label"] + counter);
                tmpdata.data.edges.push({
                  id:'edge'+tmpdata.data.edges.length,
                  source: k["id"] + "",
                  target: j["label"] + counter,
                  size: 3,
                  style: {
                    stroke: "#ff0000",
                    opacity: 0,
                    fillOpacity: 0,
                    strokeOpacity: 0,
                  },
                });
              }
              //绘制超边
              tmpdata.hulls.push({
                id: "hull" + counter++,
                padding: 10,
                members: member,
                style: {
                  fill: "#000",
                  stroke: "#fff",
                },
              });
            }
            this.graphDataList.push(tmpdata);
            // console.log(tmpdata);
          }
          this.rulePage.total = this.graphDataList.length;
          this.rulePage.curPage = 1;
          this.originFlag = false;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
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
