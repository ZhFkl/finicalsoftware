<template>
  <div class="my-wrapper">
    <div class="my-title">
      基于置信度的风险评估
      <i class="el-icon-back" v-if="!originFlag" @click="originFlag = true"
        >返回</i
      >
    </div>

    <div class="my-content" v-if="originFlag">

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

      <el-row type="flex" align="middle"  style="margin-bottom:10px;margin-top:10px">
        <el-col :span="4">请选择评估的模型：</el-col>
        <el-col :span="10">
          <el-select size="small" style="width: 100%" v-model="modelType">
            <el-option
              v-for="item in modelOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="5" :offset="1">
          <el-button type="primary" size="small" @click="showStatistic=true"
            >查看评估信息</el-button
          >
        </el-col>
      </el-row>

      <el-row align="middle" v-if="showStatistic">
        <el-col :span="6"  class="panel-group">
          <el-row class="title">风险评估统计信息</el-row>
          
          <div class="card-panel">
            <el-image :src="img.path" fit="contain" style="height:110px"/>
          </div>
          
          <div class="card-panel">
            <div class="card-panel-icon-wrapper icon-people">
              <svg-icon icon-class="star" class-name="card-panel-icon" />
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">
                准确率ACC
              </div>
              <div class="card-panel-num">{{statisticInfo.acc}}</div>
            </div>
          </div>
          
          <!-- <div class="card-panel">
            <div class="card-panel-icon-wrapper icon-people">
              <svg-icon icon-class="star" class-name="card-panel-icon" />
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">
                低风险规则占比
              </div>
              <div class="card-panel-num">{{statisticInfo.low}}</div>
            </div>
          </div>
          
          <div class="card-panel">
            <div class="card-panel-icon-wrapper icon-people">
              <svg-icon icon-class="star" class-name="card-panel-icon" />
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">
                高风险规则占比
              </div>
              <div class="card-panel-num">{{statisticInfo.high}}</div>
            </div>
          </div> -->
          <pie-chart :id="'tmpPie'" :pieData="pieData" :isChange="pieChange"></pie-chart>
          
        </el-col>
        <el-col :span="18">
          <el-row class="title">典型风险规则可视化</el-row>
          <el-row>
            <el-col :span="12">
              <div style="width: 90%; height: 450px; margin-top: 10px;text-align:center">
                <tmp-graph
                  :graphData="highRule.data"
                  :hulls="highRule.hulls"
                  :ind="highRule.index"
                  :picLabel="highRule.risk"
                  :isChange="highRule.change"
                ></tmp-graph>
                
                <el-button type="primary" size="mini"
                style="margin-top:10px"
                @click="showInstance(highRule.id,highRule.index)">
                  高风险规则实例
                </el-button>
              </div>         
            </el-col>
            <el-col :span="12">
              <div style="width: 90%; height: 450px; margin-top: 10px;text-align:center">
                <tmp-graph
                  :graphData="lowRule.data"
                  :hulls="lowRule.hulls"
                  :ind="lowRule.index"
                  :picLabel="lowRule.risk"
                  :isChange="lowRule.change"
                ></tmp-graph>
                
                <el-button type="primary" size="mini"
                style="margin-top:10px"
                @click="showInstance(lowRule.id,lowRule.index)">
                  低风险规则实例
                </el-button>
              </div>
            </el-col>
          </el-row>
             
        </el-col>
      </el-row>
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
import pieChart from "@/components/Charts/pieChart.vue";
import adminDashboard from "./../task31/admin";
import * as apiTopic1 from "@/api/topic1";
export default {
  name: "task331",
  components: { TmpGraph, adminDashboard,pieChart },
  data() {
    return {
      img: {
        url: '',
        path:require('@/assets/topic1.2.jpg')
      },
      tableData: [],
      originFlag: true,
      graphData: {},
      hulls: [],
      statisticInfo:{
        model:'',
        acc:'',
        high:'',
        low:''        
      },
      pieData:[
      ],
      pieChange:false,
      graphMap:null,
      instanceVisible:false,
      instanceTitle:'',
      instanceList:[],
      activeInd:0,
      activeId:-1,
      changeInstance:false,
      highRule:{
        data:{},
        hulls:[],
        index:0,
        risk:'',
        id:0,
        change:false,
      },
      lowRule:{
        data:{},
        hulls:[],
        index:1,
        risk:'',
        change:false,
        id:0
      },
      highRiskList:[],
      lowRiskList:[],
      dataSource:'',
      sourceOptions: [
        {
          label: "DATA1 供应商持股关系 （十万级）",
          value: 1,
        },
      ],
      modelType:'',
      modelOptions: [
        {
          label: "GraphSage",
          value: 1,
        },
      ],
      showStatistic:false,
    };
  },

  created() {},
  mounted() {
    this.initData();
    this.getStatistic();
  },
  methods: {
    randomInstance(){
      if(!this.graphMap||!this.graphMap.has(this.activeId)){
        this.$notify('该规则没有实例');
        return;
      }
      let list=this.graphMap.get(this.activeId);
      this.activeInd = (this.activeInd+1)%list.length;
      this.changeInstance = !this.changeInstance;
    },
    randomRule(){
      let highInd = 0;
      let lowInd = 0;
      this.highRule={
        data:this.highRiskList[highInd].data,
        hulls:this.highRiskList[highInd].hulls,
        index:this.highRiskList[highInd].index,
        risk:this.highRiskList[highInd].risk,
        id:this.highRiskList[highInd].id,
        change:!this.highRule.change
      };
      this.lowRule={
        data:this.lowRiskList[lowInd].data,
        hulls:this.lowRiskList[lowInd].hulls,
        index:this.lowRiskList[lowInd].index,
        risk:this.lowRiskList[lowInd].risk,
        id:this.lowRiskList[lowInd].id,
        change:!this.lowRule.change
      };
    },
    getStatistic(){
      apiTopic1.getRiskInfo().then(res=>{
        console.log(res)
        this.statisticInfo.model = res.data['模型'];
        this.statisticInfo.acc = res.data['test acc'];
        this.statisticInfo.low = res.data['低风险规则比例'];
        this.statisticInfo.high = res.data['高风险规则比例'];
        this.pieData=[
          {name:'高风险规则',value:parseInt(this.statisticInfo.high.replace('%',''))},
          {name:'低风险规则',value:parseInt(this.statisticInfo.low.replace('%',''))},
        ],
        this.pieChange=!this.pieChange
      })
    },
    showInstance(id,index){
      console.log(id,index)
      this.activeId = id;
      if(!this.graphMap||!this.graphMap.has(id)){
        this.$notify('该规则没有实例');
        return;
      }
      this.activeInd = 0;
      this.instanceTitle = `${id === this.highRule.id ? '高风险':'低风险'}规则的实例`;
      this.instanceList=[];
      let list=this.graphMap.get(id);
      let ind = index*10;
      let counter = 1;
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
                      fill: k["risk"] == 1 ? "#ff4949": "#13ce1c" ,
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
    initData() {
      apiTopic1
        .getRiskExample()
        .then((res) => {
          console.log(res);
          let ind = 1;
          let counter = 1;
          let ruleList=[];
          this.graphMap = new Map();
          for (let i of res.data.patterns_list) {
            if(this.graphMap.has(i.id)){
              this.graphMap.get(i.id).concat(i.instances)
            }else{
              this.graphMap.set(i.id,i.instances)
            }
          
            let uniqueNodes = [];
            let tmpdata = {};
            tmpdata.data = {};
            tmpdata.data.nodes = [];
            tmpdata.data.edges = [];
            tmpdata.hulls = [];
            tmpdata.risk = i.risk===1?'高风险':'低风险';
            tmpdata.index = ind++;
            tmpdata.id=i.id;

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
                    risk:k['risk'],
                    style: {
                      fill: "#f2e394"//k["risk"] === 1 ? "#588c73" : "#f2e394",
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
            if(i.risk===1){
              this.highRiskList.push(tmpdata);
            }else{
              this.lowRiskList.push(tmpdata);
            }
          }
          this.randomRule();
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>


<style lang="scss" scoped>

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
}

.title{
  font-weight: bold;
  line-height: 20px;
  color: rgba(0, 0, 0, 0.6);
  font-size: 18px;
  text-align: center;
}

.panel-group {
  .card-panel:hover{
    box-shadow: 4px 4px 15px rgba(0, 0, 0, .25);
    border-color: rgba(0, 0, 0, .25);

  }
  .card-panel {
    margin-top: 18px;
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 15px rgba(0, 0, 0, .05);
    border-color: rgba(0, 0, 0, .05);

    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }

      .icon-people {
        background: #40c9c6;
      }
    }

    .icon-people {
      color: #40c9c6;
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
      float: left;
      font-weight: bold;
      line-height: 108px;
      height: 108px;
      margin-left: 10px;

      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        display: inline-block;
      }

      .card-panel-num {
        float:right;
        font-size: 20px;
        margin-left: 20px;
        display: inline-block;
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
