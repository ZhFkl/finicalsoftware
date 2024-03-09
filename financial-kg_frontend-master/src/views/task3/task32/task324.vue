<template>
  <div class="my-wrapper">
    <div class="my-title">基于深度特征的逻辑规则知识推理技术
      <i v-if="!originFlag" class="el-icon-back" @click="originFlag = true;showMetricFlag=false">返回</i>
    </div>
    <div class="my-content" v-if="originFlag">
      <!-- <el-row type="flex" justify="center">
        <el-col :span="4">
          <el-button type="primary" size="small" @click="inferByFeature">基于HyperE的推理</el-button>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" size="small" @click="inferByProjection">基于TransE的推理</el-button>
        </el-col>
         <el-col :span="4">
          <el-button type="primary" size="small" @click="inferByStructure" disabled
            >基于语义结构的推理</el-button
          >
        </el-col> 
      </el-row> -->
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
        <el-col :span="5" :offset="1">
          <el-button type="primary" size="small" @click="getGraphData"
            >查看数据</el-button
          >
        </el-col>
      </el-row>

      <el-row type="flex" align="middle"  style="margin-bottom:10px;margin-top:10px">
        <el-col :span="4">请选择推理的模型：</el-col>
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
          <el-button type="primary" size="small" @click="showMetric"
            >查看指标描述</el-button
          >
          <el-button type="primary" size="small" @click="handleInfer"
            >推理</el-button
          >
        </el-col>
      </el-row>
      <el-row v-if="showOri" style=" height: 500px; margin-top: 10px">
        <el-col :span="18" style="height:100%">
          <tmp-graph :graphData="graphData" :hulls="hulls" :ind="-1" @choosePoint="getChoosePoint" :isChange="changeOriGraph"></tmp-graph>
        </el-col>
        <el-col :span="6" style="height:100%">
        <el-card style="height:100%">
          <div slot="header" class="clearfix">
            <span>节点信息</span>
          </div>
          <div v-for="(item, index) in nodeInfo" :key="index">
            <span class="highlight-span">{{item.label}}：</span>
            <span>{{item.value}}</span>
          </div>
        </el-card>
      </el-col>
      </el-row>
      <el-row :v-show="showMetricFlag">
          <el-descriptions title="指标描述" :column="2" border>
            <el-descriptions-item v-for="(item, index) in metricList" :key="index" :labelStyle="{'width':'200px'}">
              <template slot="label">
                <i class="el-icon-tickets"></i>
                {{ item.label }}
                <el-button v-if="item.label==='method'" type="text" @click="getMetricDetail">查看指标</el-button>
              </template>
              {{ item.value }}
            </el-descriptions-item>
          </el-descriptions>
        </el-row>

        <el-dialog
          title="指标含义描述"
          :visible.sync="metricDialogVisible"
          width="50%">
          <el-image :src="img.path" fit="contain" />
          <pre>{{metricDetailContent}}</pre>
        </el-dialog>
    </div>

    <div class="my-content" v-else>

      <!-- choosenPoint中保存了获取到的点 -->
      <div class="ans-line">
        <div class="ans-box" style="font-weight:bolder;font-size:1.1em;line-height: 360px;margin-left: 50px;">{{ choosenPointLabel }} 推导出的Top {{ansGraph.length}}超边</div>
        <div class="ans-box" v-for="(item, index) in ansGraph" :key="index">
          <tmp-graph :isChange="changeGraph" :graphData="item.data" :hulls="item.hulls" :ind="index"
                :width="400" :picLabel="'图'+(index+1)+'-score=' + item.score"></tmp-graph>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TmpGraph from "./../../../components/myGraph.vue";
import tmpData from "@/js/data";
import *  as api from "@/api/topic2";
export default {
  name: "task324",
  components: { TmpGraph },
  data() {
    return {
      changeOriGraph:true,
      nodeInfo:[],
      showOri: false,
      originFlag: true,
      ansGraph: [],
      hulls: [],
      choosenPoint: '',
      ansList: [
        {
          title: "123",
        },
      ],
      methodList: [],
      changeGraph: false,
      metricList: [],
      dataSource:'',
      sourceOptions: [
        {
          label: "全部数据",
          value: 1,
        },
      ],
      modelType:'',
      modelOptions: [
        {
          label: "HyperE",
          value: 1,
        },
        {
          label: "TransE",
          value: 2,
        },
      ],
      choosenPointLabel:'',
      showMetricFlag:false,
      choosenPointType:'',
      metricDialogVisible:false,
      img: {
        url: process.env.VUE_APP_BASE_API,
        path:''
      },
      metricDetailContent:'',
      counter:0
    };
  },
  created() {
    // this.graphData = {};
    // this.graphData.nodes = [];
    // this.graphData.edges = [];
  },
  mounted() {
    //该参数表示是2-1还是2-2的数据集
    api.fetchMethodList(1).then(
      res => {
        console.log(res)
        this.modelOptions = res.data.available_method.map(cur =>{
          return {label:cur, value:cur}
        })
        this.sourceOptions = res.data.available_dataset.map(cur =>{
          return {label:cur, value:cur}
        })
      }
    ).catch(e => { console.log(e.message) })
    // this.getGraphData();
  },
  methods: {
    getMetricDetail(){
      api.getMetricDetail(this.modelType).then(res =>{
        console.log(res)
        this.img.path = this.img.url + res.data.graph
        this.metricDetailContent = res.data.info
        this.metricDialogVisible=true
      }).catch(err =>{
        console.log(err)
      })
    },
    getGraphData() {
      api
        .getTopic2Data({dataset:this.dataSource})
        .then((res) => {
          console.log(res);
          let graphData = {};
          graphData.nodes = [];
          graphData.edges = [];
          let hulls = [];
          let uniqueNodes = [];

          for (let i = 0; i < res.data.length; i++) {
            let member = [];
            let tmpstr = res.data[i]["relation"]["relation_name"] + "-ID"+res.data[i]["hyper_edge_id"];
            graphData.nodes.push({
              id: res.data[i]["hyper_edge_id"]+"",
              label: tmpstr,
              size: 30,
              style: {
                stroke: "#ff0000",
                fillOpacity: 0,
                strokeOpacity: 0,
              },
            });
            member.push(res.data[i]["hyper_edge_id"]+"");

            for (let j = 0; j < res.data[i]["entities"].length; j++) {
              if (uniqueNodes.indexOf(res.data[i]["entities"][j]["entity_id"]) < 0) {
                uniqueNodes.push(res.data[i]["entities"][j]["entity_id"]);
                graphData.nodes.push({
                  id: res.data[i]["entities"][j]["entity_id"]+"",
                  label: res.data[i]["entities"][j]["entity_name"],
                  size: 30,
                  style: {
                    fill: res.data[i]["entities"][j]["entity_type"] === 0 ? "#588c73" : "#f2e394"
                  },
                });
              }
              member.push(res.data[i]["entities"][j]["entity_id"]+"");

              graphData.edges.push({
                source: res.data[i]["entities"][j]["entity_id"]+"",
                target: res.data[i]["hyper_edge_id"]+"",
                size: 3,
                style: {
                  stroke: "#ff0000",
                  opacity: 0,
                  fillOpacity: 0,
                  strokeOpacity: 0,
                },
              });
            }
            hulls.push({
              id: "hull" + this.counter++,
              padding: 10,
              members: member,
              style: {
                fill: "#000",
                stroke: "#fff",
              },
            });
          }
          this.hulls = hulls
          this.graphData = graphData
          // console.log(this.graphData, this.hulls)
          this.changeOriGraph = !this.changeOriGraph
          this.showOri = true
        })
        .catch((res) => {
          console.log(res);
        });
    },

    getChoosePoint(val) {
      console.log(val);
      this.choosenPoint = val[0]._cfg.id;
      this.choosenPointLabel = val[0]._cfg.model.label
      this.choosenPointType = val[0]._cfg.model.style.fill==="#f2e394"?'company':'people'

      api.getNodeInfo({entity_id:val[0]._cfg.id, dataset:this.dataSource}).then(res =>{
        console.log(res)
        this.nodeInfo=[]
        for(let i of Object.keys(res.data)){
          if(i==='embedding'){
            let tmp={}
            let length = res.data[i]['before'].length
            tmp.before = "["+res.data[i]['before'][0] + ', ..., '+res.data[i]['before'][length - 1]+"]"
            length = res.data[i]['after'].length
            tmp.after = "["+res.data[i]['after'][0] + ', ..., '+res.data[i]['after'][length - 1]+"]"
            this.nodeInfo.push({
            label:'embedding',
            value:tmp
          })
          continue;
          }
          this.nodeInfo.push({
            label:i,
            value:res.data[i]
          })
        }
      }).catch(res=>{
        console.log(res)
      })
    },
    showMetric(){
        api.fetchInferMetric({
          dataset: this.dataSource
        }).then(res2 => {
          console.log(res2)
          this.metricListAll=[]
          for (let i = 0; i < res2.data.length; i++) {
            let tmp = []
            for (let j in res2.data[i]) {
              tmp.push({
                label: j,
                value: res2.data[i][j]
              })
            }
            this.metricListAll.push(tmp)
            this.metricList=this.modelType==="HyperE"?this.metricListAll[1]:this.metricListAll[2]////////
          }
          this.showMetricFlag=true
        }).catch(e =>{
          this.$message.error('网络错误！');
          console.log(e.message)
        })
    },
    handleInfer(){
      if(this.choosenPointType==='company'){
        this.$message.error('请勿选择“公司”持股人做推理结点！');
        return;
      }
      if(this.modelType==="HyperE"){
        this.inferByFeature();
      }else if(this.modelType === "TransE"){
        this.inferByProjection();
      }
    },
    inferByFeature() {
      if (!this.choosenPoint) {
        this.$message.error('请先选择节点！');
        return;
      }
      this.ansGraph = [];
      api.fetchInferResult({
        method: this.modelType,
        entity: this.choosenPoint,
        dataset:this.dataSource
      }).then(res => {
        console.log(res);
        // let ansGraph=[]
        for (let i = 0; i < res.data.length; i++) {
          let graphData = {};
          graphData.nodes = [];
          graphData.edges = [];
          let hulls = [];
          let uniqueNodes = [];
          let member = [];
          graphData.nodes.push({
            id: res.data[i]["relation"]["relation_id"]+"",
            label: res.data[i]["relation"]["relation_name"],
            size: 30,
            style: {
              stroke: "#ff0000",
              fillOpacity: 0,
              strokeOpacity: 0,
            },
          });
          member.push(res.data[i]["relation"]["relation_id"]+"");
          // graphData.nodes.push({
          //   id: this.choosenPoint,
          //   label: this.choosenPoint,
          //   size: 30,
          //   style: {
          //     fill: "#588c73",
          //   },
          // });
          // member.push(this.choosenPoint);
          for (let j = 0; j < res.data[i]["entity"].length; j++) {
            if (uniqueNodes.indexOf(res.data[i]["entity"][j]["entity_id"]) < 0) {
              uniqueNodes.push(res.data[i]["entity"][j]["entity_id"]);
              graphData.nodes.push({
                id: res.data[i]["entity"][j]["entity_id"]+"",
                label: res.data[i]["entity"][j]["entity_name"],
                size: 30,
                style: {
                  fill: res.data[i]["entity"][j]["entity_type"] === 0 ? "#588c73" : "#f2e394"
                },
              });
            }
            member.push(res.data[i]["entity"][j]["entity_id"]+"");
            graphData.edges.push({
              id: graphData.edges.length,
              source: res.data[i]["entity"][j]["entity_id"]+"",
              target: res.data[i]["relation"]["relation_id"]+"",
              size: 3,
              style: {
                stroke: "#ff0000",
                opacity: 0,
                fillOpacity: 0,
                strokeOpacity: 0,
              },
            });
          }
          hulls.push({
            id: "hull",
            padding: 10,
            members: member,
            style: {
              fill: "#000",
              stroke: "#fff",
            },
          });
          this.ansGraph.push({
            data: graphData,
            hulls: hulls,
            score: res.data[i].score.toString()
          });
        }
        // console.log(ansGraph)
        this.changeGraph = !this.changeGraph;
        // this.ansGraph = ansGraph
        this.originFlag = false
      })
      .catch(e => {
        this.$message.error('推理失败');
        console.log(e)
      })
    },
    inferByProjection() {
      if (!this.choosenPoint) {
        this.$message.error('请先选择节点！');
        return;
      }
      this.ansGraph = [];
      api.fetchInferResult({
        method: this.modelType,
        entity: this.choosenPoint,
        dataset:this.dataSource
      }).then(res => {
        console.log(res);
        let ansGraph=[]
        for (let i = 0; i < res.data.length; i++) {
          let graphData = {};
          graphData.nodes = [];
          graphData.edges = [];
          let hulls = [];
          let uniqueNodes = [];
          let member = [];
          graphData.nodes.push({
            id: res.data[i]["relation"]["relation_id"]+"",
            label: res.data[i]["relation"]["relation_name"],
            size: 30,
            style: {
              stroke: "#ff0000",
              fillOpacity: 0,
              strokeOpacity: 0,
            },
          });
          member.push(res.data[i]["relation"]["relation_id"]+"");
          // graphData.nodes.push({
          //   id: this.choosenPoint,
          //   label: this.choosenPoint,
          //   size: 30,
          //   style: {
          //     fill: "#588c73",
          //   },
          // });
          // member.push(this.choosenPoint);
          for (let j = 0; j < res.data[i]["entity"].length; j++) {
            if (uniqueNodes.indexOf(res.data[i]["entity"][j]["entity_id"]) < 0) {
              uniqueNodes.push(res.data[i]["entity"][j]["entity_id"]);
              graphData.nodes.push({
                id: res.data[i]["entity"][j]["entity_id"]+"",
                label: res.data[i]["entity"][j]["entity_name"],
                size: 30,
                style: {
                  fill: "#588c73",
                },
              });
            }
            member.push(res.data[i]["entity"][j]["entity_id"]+"");
            graphData.edges.push({
              id: graphData.edges.length,
              source: res.data[i]["entity"][j]["entity_id"]+"",
              target: res.data[i]["relation"]["relation_id"]+"",
              size: 3,
              style: {
                stroke: "#ff0000",
                opacity: 0,
                fillOpacity: 0,
                strokeOpacity: 0,
              },
            });
          }
          hulls.push({
            id: "hull",
            padding: 10,
            members: member,
            style: {
              fill: "#000",
              stroke: "#fff",
            },
          });
          this.ansGraph.push({
            data: graphData,
            hulls: hulls,
            score: res.data[i].score.toString()
          });
        }
        console.log(this.ansGraph)
        this.changeGraph = !this.changeGraph;
        this.originFlag = false
      }).catch(e => {
        this.$message.error('推理失败');
        console.log(e.message)
      })
    },
    inferByStructure() {
      if (!this.choosenPoint) {
        this.$message.error('请先选择节点！');
        return;
      }
      api.fetchInferResult({
        method: this.methodList[1],
        entity: this.choosenPoint
      }).then(res => {
        console.log(res);
        for (let i = 0; i < res.data.length; i++) {
          let graphData = {};
          graphData.nodes = [];
          graphData.edges = [];
          let hulls = [];
          let uniqueNodes = [];
          let member = [];
          graphData.nodes.push({
            id: res.data[i]["relation"],
            label: res.data[i]["relation"],
            size: 30,
            style: {
              stroke: "#ff0000",
              fillOpacity: 0,
              strokeOpacity: 0,
            },
          });
          member.push(res.data[i]["relation"]);
          graphData.nodes.push({
            id: this.choosenPoint,
            label: this.choosenPoint,
            size: 30,
            style: {
              fill: "#588c73",
            },
          });
          member.push(this.choosenPoint);
          for (let j = 0; j < res.data[i]["entity"].length; j++) {
            if (uniqueNodes.indexOf(res.data[i]["entity"][j]) < 0) {
              uniqueNodes.push(res.data[i]["entity"][j]);
              graphData.nodes.push({
                id: res.data[i]["entity"][j],
                label: res.data[i]["entity"][j],
                size: 30,
                style: {
                  fill: "#588c73",
                },
              });
            }
            member.push(res.data[i]["entity"][j]);
            graphData.edges.push({
              id: graphData.edges.length,
              source: res.data[i]["entity"][j],
              target: res.data[i]["relation"],
              size: 3,
              style: {
                stroke: "#ff0000",
                opacity: 0,
                fillOpacity: 0,
                strokeOpacity: 0,
              },
            });
          }
          hulls.push({
            id: "hull",
            padding: 10,
            members: member,
            style: {
              fill: "#000",
              stroke: "#fff",
            },
          });
          this.ansGraph.push({
            data: graphData,
            hulls: hulls,
            score: res.data[i].score.toString()
          });
        }
        this.changeGraph = !this.changeGraph;
        this.originFlag = false;
        console.log(this.ansGraph)
      }).catch(e => {
        this.$message.error('推理失败');
        console.log(e.message)
      })
    },
  },
};
</script>

<style lang="scss" scoped>
.ans-line{
  display:flex;
  width:100%;
  flex-direction:row;
  flex-wrap: wrap;
  
  .ans-box{
    // flex:1;
    width:300px;
    height:300px;
  }
}

.highlight-span{
  font-weight:bold;
}
</style>
