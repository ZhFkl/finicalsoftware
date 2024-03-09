<template>
  <div class="my-wrapper">
    <div class="my-title">{{modelType}}
      <!-- <i class="el-icon-back" v-if="showTripleStep||showMultiStep" 
      @click="(showTripleStep=true,showMultiStep = true)"
        >返回</i> -->
    </div>
    <div class="my-content" >
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
          <el-button type="primary" size="small" @click="getOriginData"
            >查看数据</el-button
          >
          <el-button type="primary" size="small" @click="getEditDistance"
            >编辑距离</el-button
          >
        </el-col>
      </el-row>
    </div>
    <div class="my-content">
        <el-row type="flex" align="middle"  style="margin-bottom:10px;margin-top:10px">
            <el-col :span="4">请选择预测的参数：</el-col>
            <el-col :span="5">
            λ：<el-input v-model="parameter.lambda" style="width:90%" size="small" />
            </el-col>
            <el-col :span="5" style="text-align:right">
            τ：<el-input v-model="parameter.tau"  style="width:90%"  size="small" />
            </el-col>
            <el-col :span="5" :offset="1">
            <el-button type="primary" size="small" @click="handlePredict"
                >超边预测</el-button
            >
            </el-col>
        </el-row>
        <div v-if="showOrigin">
            <el-row style="height:400px">
                <el-col :span="11" style="height:100%">
                <tmp-graph  :graphData="graphDataBefore" 
                            :hulls="hullsBefore" 
                            :ind="3" 
                            :isChange="changeBefore"
                            :isDestroy="destroyBefore"
                            @choosePoint="getChoosePoint">
                </tmp-graph>
                </el-col>
                <el-col :span="11" :offset="2" style="height:100%" v-if="showPredict">
                <tmp-graph :graphData="graphDataAfter" 
                            :hulls="hullsAfter" 
                            :ind="4" >
                            :isChange="changeAfter"
                            :isDestroy="destroyAfter"
                </tmp-graph>
                </el-col>
            </el-row>
        <el-row class="title" v-if="showDistance">{{editDistanceText}}</el-row>
        </div>
    </div>
  </div>
</template>

<script>

import TmpGraph from "./../../../components/myGraph.vue";
import tabelData from '@/js/data_tuili.js'
import *  as api from "@/api/topic2";
export default {
  name: "task322",
  components: { TmpGraph },
  data() {
    return {
      tableData: [],
      graphDataBefore: {},
      graphDataAfter: {},
      hullsBefore: [],
      hullsAfter: [],
      changeBefore: false,
      destroyBefore:false,
      changeAfter:false,
      destroyAfter:false,
      showOrigin:false,
      showPredict:false,
      showDistance:false,
      editDistanceText:'暂无结果',
      showInferColumn:false,
      dataSource:'',
      counter:0,
      choosenPoints:[],
      parameter:{
        lambda:'',
        tau:''
      },
      sourceOptions: [
        {
          label: "全部数据",
          value: 1,
        },
      ],
      modelType:'基于编辑距离的多步推理',
      modelOptions: [
        {
          label: "基于规则的三步推理",
          value: 1,
        },
        {
          label: "基于编辑距离的多步推理",
          value: 2,
        },
      ],
      ruleType:null,
      ruleOptions: [
        {
          label: "规则1",
          value: 1,
        },
        {
          label: "规则2",
          value: 2,
        },
        {
          label: "规则3",
          value: 3,
        },
        {
          label: "规则4",
          value: 4,
        },
        {
          label: "规则5",
          value: 5,
        },
      ],
      showTripleStep:false,
      showMultiStep:false,
    }
  },
  mounted() {
  },
  methods: {
    getChoosePoint(val) {
      console.log(val);
      this.choosenPoints = val;
      // this.choosenPointLabel = val[0]._cfg.model.label
    },
    handlePredict(){
        api.getHyedgePredict({
          lambda:this.parameter.lambda,
          tau:this.parameter.tau
          }).then(res=>{
            console.log(res)
            let graphData = {};
            graphData.nodes = [];
            graphData.edges = [];
            let hulls = [];
            let uniqueNodes = [];
            this.showPredict = true;
            this.destroyAfter = !this.destroyAfter;
            this.changeAfter = !this.changeAfter;
            for (let i of res.data) {
              let member = [];
                let tmpstr = i["relation"]["relation_name"] + "-ID"+ i["hyper_edge_id"];
                graphData.nodes.push({
                  id: i["hyper_edge_id"]+"",
                  label: tmpstr,
                  size: 30,
                  style: {
                    stroke: "#ff0000",
                    fillOpacity: 0,
                    strokeOpacity: 0,
                  },
                });
                member.push(i["hyper_edge_id"]+"");

                for (let j = 0; j < i["entities"].length; j++) {
                  if (uniqueNodes.indexOf(i["entities"][j]["entity_id"]) < 0) {
                    uniqueNodes.push(i["entities"][j]["entity_id"]);
                    graphData.nodes.push({
                      id: i["entities"][j]["entity_id"]+"",
                      label: i["entities"][j]["entity_name"],
                      size: 30,
                      style: {
                        fill: i["entities"][j]["entity_type"] === 0 ? "#588c73" : "#f2e394"
                      },
                    });
                  }
                  member.push(i["entities"][j]["entity_id"]+"");

                  graphData.edges.push({
                    source: i["entities"][j]["entity_id"]+"",
                    target: i["hyper_edge_id"]+"",
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
              hulls.push({
                id: "hull" + this.counter++,
                padding: 10,
                members: ["1310925", "62740157","58068530", "19656542","53391742"],
                style: {
                  fill: "#f00",
                  stroke: "#00f",
                },
              })
          this.hullsAfter= hulls
          this.graphDataAfter = graphData
          console.log(this.graphDataAfter, this.hullsAfter)
          }).catch(e=>e)
    },
    getEditDistance(){
      if(this.choosenPoints.length<=1 || this.choosenPoints.length>=3){
         this.$message({
          message: '请选择两个节点！',
          type: 'warning'
        });
        return;
      }
        api.getEditDistance({
          fId:this.choosenPoints[1]._cfg.id,
          tId:this.choosenPoints[0]._cfg.id
        }).then(res=>{
          console.log(res);
          this.showDistance=true;
          this.editDistanceText=res.data;
        }).catch(e=>console.log(e))
    },
    getOriginData(){
      api.getHypergraph().then(res => {
        let graphData = {};
        graphData.nodes = [];
        graphData.edges = [];
        let hulls = [];
        let uniqueNodes = [];
        this.showOrigin = true;
        this.destroyBefore = !this.destroyBefore;
        this.changeBefore = !this.changeBefore;
          console.log(res)
        for (let i of res.data) {
          let member = [];
            let tmpstr = i["relation"]["relation_name"] + "-ID"+ i["hyper_edge_id"];
            graphData.nodes.push({
              id: i["hyper_edge_id"]+"",
              label: tmpstr,
              size: 30,
              style: {
                stroke: "#ff0000",
                fillOpacity: 0,
                strokeOpacity: 0,
              },
            });
            member.push(i["hyper_edge_id"]+"");

            for (let j = 0; j < i["entities"].length; j++) {
              if (uniqueNodes.indexOf(i["entities"][j]["entity_id"]) < 0) {
                uniqueNodes.push(i["entities"][j]["entity_id"]);
                graphData.nodes.push({
                  id: i["entities"][j]["entity_id"]+"",
                  label: i["entities"][j]["entity_name"],
                  size: 30,
                  style: {
                    fill: i["entities"][j]["entity_type"] === 0 ? "#588c73" : "#f2e394"
                  },
                });
              }
              member.push(i["entities"][j]["entity_id"]+"");

              graphData.edges.push({
                source: i["entities"][j]["entity_id"]+"",
                target: i["hyper_edge_id"]+"",
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
          this.hullsBefore= hulls
          this.graphDataBefore = graphData
          console.log(this.graphDataBefore, this.hullsBefore)
      }).catch(res => {
        console.log(res)
      })
      // console.log(tabelData)
    },
    handleTripleInfer(){
      if(this.ruleType===1){
        this.getDataInfer()
      }else{
        this.getDataInferNew(parseInt(this.ruleType)-1)
      }
    },
    loadData(){
      this.destroyBefore = !this.destroyBefore;
      this.tableData=[];
      this.showInferColumn = false;
      if(this.ruleType===1){
        this.getDataOrigin()
        this.getRulePath()
      }
      else{
        this.getDataOriginNew(parseInt(this.ruleType)-1)
        this.getRulePathNew(parseInt(this.ruleType)-1)
      }

    },
    changeModel(){
      if(this.modelType===1){
        this.showMultiStep = false;
        this.showTripleStep = true;
      }
      else if(this.modelType===2){
        this.showTripleStep = false;
        this.showMultiStep = true;
      }
    },
    objectSpanMethod({ row, column, rowIndex, columnIndex }) {
      if (this.ruleType===1&&(columnIndex === 0 || columnIndex === 2)) {
        if (this.ruleType===1&&rowIndex % 3 === 0) {
          return {
            rowspan: 3,
            colspan: 1
          };
        } else {
          return {
            rowspan: 0,
            colspan: 0
          };
        }
      }
      else{
        return{
            rowspan: 1,
            colspan: 1
        }
      }
    },
    getRulePath() {
      api.getRulePath().then(res => {
        console.log(res)
        for (let i of Object.keys(res.data)) {
          let tmp = {}
          tmp.title = i

          for (let j = 0; j < res.data[i].length - 1; j++) {
            tmp.before = {}
            tmp.before.key = Object.keys(res.data[i][j])[0]
            tmp.before.highlight = []
            tmp.before.ordinary = []
            for (let k of Object.keys(res.data[i][j][tmp.before.key])) {
              // console.log(k)
              if (res.data[i][j][tmp.before.key][k]["type"] === 0) {
                tmp.before.ordinary.push(k)
              } else {
                tmp.before.highlight.push(k)
              }
            }


            tmp.after = {}
            tmp.after.key = Object.keys(res.data[i][3])[0]
            tmp.after.value = []
            for (let k of Object.keys(res.data[i][3][tmp.after.key])) {
                tmp.after.value.push(k)
            }
            this.tableData.push(JSON.parse(JSON.stringify(tmp)))
          }

        }
        console.log(this.tableData)
      }).catch(res => {
        console.log(res)
      })
      // console.log(tabelData)
    },
    getDataInfer() {
      api.getDataInfer().then(res => {
        console.log(res)
        let hullsAfter = []
        let edgesAfter = []
        let counter = this.hullsBefore.length;
        // let res={}
        // res.data = dataOrigin

        for (let i in res.data) {
          let member = [];
          member.push(i+"super");

          for (let j in res.data[i]) {
            if (j === "start_time" || j === "end_time") {
              continue;
            }
            member.push(j);

            edgesAfter.push({
              source: i+"super",
              target: j,
              size: 3,
              style: {
                stroke: "#ff0000",
                opacity: 0,
                fillOpacity: 0,
                strokeOpacity: 0,
              },
            });
          }
          hullsAfter.push({
            id: "afterHull" + counter++,
            padding: 10,
            members: member,
            style: {
              fill: "#f00",
              stroke: "#00f",
            },
          });
        }
        this.graphDataBefore.edges = this.graphDataBefore.edges.concat(edgesAfter)
        this.hullsBefore = this.hullsBefore.map(cur => {
          cur.id = "afterHull" + counter++
          return cur
        }).concat(hullsAfter)
        this.changeBefore = !this.changeBefore
        this.showInferColumn = true
        console.log(this.graphDataBefore, this.hullsBefore)
      })
    },
    getDataOrigin() {
      api.getDataOrigin().then(res => {
        console.log(res)
        let graphDataBefore = {}
        let hullsBefore = []
        graphDataBefore.nodes = [];
        graphDataBefore.edges = [];
        let counter = 1;
        let uniqueNodes = [];
        // let res={}
        // res.data = dataOrigin

        for (let i in res.data) {
          let member = [];
          member.push(i+"super");
          // if (uniqueNodes.indexOf(i) < 0) {
          //   uniqueNodes.push(i);
            graphDataBefore.nodes.push({
              id: i+"super",
              label: i,
              size: 30,
              style: {
                stroke: "#ff0000",
                fillOpacity: 0,
                strokeOpacity: 0,
              },
            });
          // }
          for (let j in res.data[i]) {
            if (j === "start_time" || j === "end_time") {
              continue;
            }
            member.push(j);
            if (uniqueNodes.indexOf(j) < 0) {
              uniqueNodes.push(j);
              graphDataBefore.nodes.push({
                id: j,
                label: j,
                size: 30,
                style: {
                  fill:
                    res.data[i][j]["type"] === 0 ? "#588c73" : "#f2e394",
                },
              });
            }
            graphDataBefore.edges.push({
              source: i+"super",
              target: j,
              size: 3,
              style: {
                stroke: "#ff0000",
                opacity: 0,
                fillOpacity: 0,
                strokeOpacity: 0,
              },
            });
          }
          hullsBefore.push({
            id: "beforeHull" + counter++,
            padding: 10,
            members: member,
            style: {
              fill: "#000",
              stroke: "#fff",
            },
          });
        }
        this.graphDataBefore = graphDataBefore
        this.hullsBefore = hullsBefore
        this.changeBefore = !this.changeBefore
        console.log(this.graphDataBefore, this.hullsBefore);
      })
    },
    getRulePathNew(guize) {
      api.getRulePathNew(guize).then(res => {
        console.log(res)
        for (let i of Object.keys(res.data.reason)) {
          let tmp = {}
          tmp.title = i
          tmp.before = []

          for (let j in res.data.reason[i].path) {
            let tmpItem = {}
            tmpItem.key = j
            tmpItem.highlight = []
            tmpItem.ordinary = []
            for (let k of Object.keys(res.data.reason[i].path[j])) {
              // console.log(k)
              tmpItem.ordinary.push(k)
            }
            tmp.before.push(tmpItem)
          }
          tmp.after = {};
          tmp.after.key = '新超边';
          tmp.after.value = [];
          for (let j in res.data.reason[i].result){
            tmp.after.value.push(j)
          }
          this.tableData.push(JSON.parse(JSON.stringify(tmp)))
        }
        console.log(this.tableData)
      }).catch(res => {
        console.log(res)
      })
      // console.log(tabelData)
    },
    getDataInferNew(guize) {
      api.getDataInferNew(guize).then(res => {
        console.log(res)
        let hullsAfter = []
        let edgesAfter = []
        let nodesAfter = []
        let counter = this.hullsBefore.length;
        // let res={}
        // res.data = dataOrigin

        for (let i in res.data.result) {
          let member = [];
          member.push(i+"super");
          nodesAfter.push({
              id: i+"super",
              label: '新超边'+(nodesAfter.length+1),
              size: 30,
              style: {
                stroke: "#ff0000",
                fillOpacity: 0,
                strokeOpacity: 0,
              },
            });
          for (let j in res.data.result[i]) {
            if (j === "start_time" || j === "end_time") {
              continue;
            }
            member.push(j);

            edgesAfter.push({
              source: i+"super",
              target: j,
              size: 3,
              style: {
                stroke: "#ff0000",
                opacity: 0,
                fillOpacity: 0,
                strokeOpacity: 0,
              },
            });
          }
          hullsAfter.push({
            id: "afterHull" + counter++,
            padding: 10,
            members: member,
            style: {
              fill: "#f00",
              stroke: "#00f",
            },
          });
        }
        this.graphDataBefore.edges = this.graphDataBefore.edges.concat(edgesAfter)
        this.graphDataBefore.nodes = this.graphDataBefore.nodes.concat(nodesAfter)
        this.hullsBefore = this.hullsBefore.map(cur => {
          cur.id = "afterHull" + counter++
          return cur
        }).concat(hullsAfter)
        this.changeBefore = !this.changeBefore
        this.showInferColumn = true
        console.log(this.graphDataBefore, this.hullsBefore)
      })
    },
    getDataOriginNew(guize) {
      api.getDataOriginNew(guize).then(res => {
        console.log(res)
        let graphDataBefore = {}
        let hullsBefore = []
        graphDataBefore.nodes = [];
        graphDataBefore.edges = [];
        let counter = 1;
        let uniqueNodes = [];
        // let res={}
        // res.data = dataOrigin

        for (let i in res.data) {
          let member = [];
          member.push(i+"super");
          // if (uniqueNodes.indexOf(i) < 0) {
          //   uniqueNodes.push(i);
            graphDataBefore.nodes.push({
              id: i+"super",
              label: i,
              size: 30,
              style: {
                stroke: "#ff0000",
                fillOpacity: 0,
                strokeOpacity: 0,
              },
            });
          // }
          for (let j in res.data[i]) {
            if (j === "start_time" || j === "end_time") {
              continue;
            }
            member.push(j);
            if (uniqueNodes.indexOf(j) < 0) {
              uniqueNodes.push(j);
              graphDataBefore.nodes.push({
                id: j,
                label: j,
                size: 30,
                style: {
                  fill:
                    res.data[i][j]["type"] === 0 ? "#588c73" : "#f2e394",
                },
              });
            }
            graphDataBefore.edges.push({
              source: i+"super",
              target: j,
              size: 3,
              style: {
                stroke: "#ff0000",
                opacity: 0,
                fillOpacity: 0,
                strokeOpacity: 0,
              },
            });
          }
          hullsBefore.push({
            id: "beforeHull" + counter++,
            padding: 10,
            members: member,
            style: {
              fill: "#000",
              stroke: "#fff",
            },
          });
        }
        this.graphDataBefore = graphDataBefore
        this.hullsBefore = hullsBefore
        this.changeBefore = !this.changeBefore
        console.log(this.graphDataBefore, this.hullsBefore);
      })
    }
  }
}
</script>


<style lang="scss" scoped>
.title{
  font-weight: 800;
  line-height: 20px;
  color: rgba(169, 45, 45, 0.6);
  font-size: 20px;
  text-align: left;
}
</style>