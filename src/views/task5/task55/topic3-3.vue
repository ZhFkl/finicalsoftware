<template>
  <div class="my-wrapper">
    <div class="my-title">基于动态聚类的规则归纳及可视化</div>
    <div class="my-content">
      <el-row type="flex" align="middle">
        <el-col :span="4">1. 请选择基准数据集：</el-col>
        <el-col :span="10">
          <el-select size="small" style="width: 100%" v-model="dataSource">
            <el-option v-for="item in dataSourceOptions" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="5" :offset="1">
          <el-button type="primary" size="small" @click="loadData">选定数据</el-button>
        </el-col>
        <!-- <el-col :span="5" :offset="1">
          <el-button type="primary" size="small" @click="loadRules">获取新规则</el-button>
        </el-col> -->
      </el-row>

      <el-row style="margin-top: 10px">
        <el-col :span="24" style="height:500px">
          <tmp-graph :graphData="graphData" :hulls="graphHulls" :ind="0" @choosePoint="clickGraph"
            :isChange="isChangeFlag"></tmp-graph>
        </el-col>
      </el-row>

      <el-dialog :title="'超图-聚类类别' + clusterClass" :visible.sync="superGraphVisible" width="50%">
        <div style="width:100%;height:350px">
          <tmp-graph :graphData="graphDataDialog" :hulls="graphHullsDialog" :ind="1" :isChange="dialogIsChangeFlag">
          </tmp-graph>
        </div>
      </el-dialog>

      <el-row type="flex" align="middle">
        <el-col :span="4">2. 选择动态聚类的新规则：</el-col>
        <el-col :span="10">
          <el-select size="small" style="width: 100%" v-model="ruleSource">
            <el-option v-for="item in ruleSourceOptions" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="9" :offset="1">
          <el-button type="primary" size="small" @click="checkRules">查看</el-button>
          <el-button type="primary" size="small" @click="addRules">添加</el-button>
          <el-button type="primary" size="small" @click="DBscanCluster">动态聚类</el-button>
        </el-col>
      </el-row>

      <el-row style="margin-top: 10px">
        <el-col :span="24" style="height:500px">
          <tmp-graph :picLabel="'规则'+ruleSource" :graphData="ruleGraphData" :hulls="ruleGraphHulls" :ind="2" :isChange="ruleIsChangeFlag">
          </tmp-graph>
        </el-col>
      </el-row>


      <!-- 待添加数据！！！！！！！！！！！！！！！！！ -->
      <el-row style="margin-top: 10px">
        <el-col :span="24" style="height:500px">
          <tmp-graph picLabel="动态聚类结果图" :graphData="resGraphData" :hulls="resGraphHulls" :ind="3" @choosePoint="clickResGraph"
            :isChange="resIsChangeFlag"></tmp-graph>
        </el-col>
      </el-row>

      <el-dialog :title="'超图'" :visible.sync="ressuperGraphVisible" width="50%">
        <div style="width:100%;height:350px">
          <tmp-graph :graphData="resGraphDataDialog" :hulls="resGraphHullsDialog" :ind="4"
            :isChange="resDialogIsChangeFlag"></tmp-graph>
        </div>
      </el-dialog>

      <!-- <el-row type="flex" align="middle" style="margin-top:10px">
        <el-col :span="4">2. 请添加聚类规则：</el-col>
        <el-col :span="10">
          <el-select size="small" style="width: 100%" v-model="ruleSource">
            <el-option v-for="item in ruleSourceOptions" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="5" :offset="1">
          <el-button type="primary" size="small" @click="DBscanCluster">确定</el-button>
        </el-col>
      </el-row> -->

    </div>
  </div>
</template>

<script>

import { dataList, dataList3_3, newRule, dbcluster } from "@/api/topic3";

import TmpGraph from "@/components/myGraph.vue";
export default {

  name: 'topic3-3',
  components: { TmpGraph },
  data() {

    return {
      ressuperGraphVisible:false,
      colorList: ['#36b5e6','#ff5219','#ffa806','#57b728','#f6ec46',
    '#ff39a0','#ff9f9f','#bc371d','#9032ba'],
      //["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff", "#00ffff", "#ffffff", "#999999", "#2e3c45", "#ef5612"],
      resDialogIsChangeFlag: false,
      resIsChangeFlag: false,
      resGraphData: {},
      resGraphHulls: [],
      resAllSuperGraphData: {},
      resGraphDataDialog: {},
      resGraphHullsDialog: [],
      ruleIsChangeFlag: false,
      ruleGraphData: {},
      ruleGraphHulls: [],
      selectRules: [],
      allruleGraphData: {},
      counter: 0,
      isChangeFlag: false,
      dialogIsChangeFlag: false,
      ruleSource: "",
      dataSource: "",
      ruleSourceOptions: [],
      dataSourceOptions: [],
      graphData: {},
      graphHulls: [],
      superGraphVisible: false,
      graphDataDialog: {},
      graphHullsDialog: [],
      clusterClass: -1,
    }
  },
  mounted() {
    dataList()
      .then((res) => {
        console.log(res);
        this.dataSourceOptions = res.data.map((val) => {
          if(val==='rules_1')
            return {
              value:val,
              label:'rules_2(千级别的规则)'
            }
          else if(val === 'rules_2')
            return {
              value:val,
              label:'rules_1(百级别的规则)'
            }
          else if(val === 'rules_3')
            return {
              value:val,
              label:'rules_3(十万级别的规则)'
            }
          return { value: val, label: val }
        }).sort((a,b)=>{
          return a.label.localeCompare(b.label)
        })
      })
      .catch((e) => console.log(e.message));
  },
  methods: {
    checkRules() {
      let ruleGraphData = {
        nodes: [],
        edges: []
      }
      let ruleGraphHulls = []

      // allruleGraphData
      let uniqueNodes = [];
      let BeforeData = this.allruleGraphData[this.ruleSource]
      for (let i = 0; i < BeforeData.edges.length; i++) {
        let member = [];
        member.push("超边" + i)
        ruleGraphData.nodes.push({
          id: "超边" + i,
          label: "超边" + i + "-类别" + BeforeData.edges[i]["relation"],
          size: 30,
          style: {
            stroke: "#ff0000",
            fillOpacity: 0,
            strokeOpacity: 0,
          },
        });
        for (let j of BeforeData.edges[i]["entities"]) {
          if (uniqueNodes.indexOf(j) < 0) {
            uniqueNodes.push(j)
            ruleGraphData.nodes.push({
              id: "node" + j,
              label: j + "",
              size: 30,
              style: {
                fill: "#588c73",
              },
            });
          }
          member.push("node" + j)
          ruleGraphData.edges.push({
            id: ruleGraphData.edges.length,
            source: "node" + j,
            target: "超边" + i,
            size: 3,
            style: {
              stroke: "#ff0000",
              opacity: 0,
              fillOpacity: 0,
              strokeOpacity: 0,
            },
          });
        }
        ruleGraphHulls.push({
          id: "hull" + this.counter++,
          padding: 10,
          members: member,
          style: {
            fill: "#000",
            stroke: "#fff",
          },
        });
      }
      this.ruleGraphData = ruleGraphData
      this.ruleGraphHulls = ruleGraphHulls
      this.ruleIsChangeFlag = !this.ruleIsChangeFlag
    },
    addRules() {
      this.selectRules.push(parseInt(this.ruleSource))
      // this.resAllSuperGraphData[nodeIndex].edges
      // console.log(this.allruleGraphData[this.ruleSource],this.superGraphData)
      this.resAllSuperGraphData[this.ruleSource] = JSON.parse(JSON.stringify(this.allruleGraphData[this.ruleSource]))
      this.resAllSuperGraphData = Object.assign(this.superGraphData,this.resAllSuperGraphData)
      this.$message({
        message: '添加成功',
        type: 'success'
      })
      console.log(this.resAllSuperGraphData)
    },
    loadRules() {
      this.ruleSourceOptions=[]
      newRule(this.dataSource).then(res => {
        console.log(res)
        for (let i of Object.keys(res.data.cases)) {
          this.ruleSourceOptions.push({
            label: "规则" + i,
            value: i
          })
        }
        this.allruleGraphData = res.data.cases
        this.resAllSuperGraphData = JSON.parse(JSON.stringify(this.allruleGraphData))
      }).catch(res => {
        console.log(res)
      })
    },
    clickGraph(arr) {
      if (arr.length < 1) return;
      // superGraphData 
      // graphDataDialog: {},
      // graphHullsDialog: [],
      let nodeIndex = arr[0]._cfg.id
      let graphDataDialog = {
        nodes: [],
        edges: []
      }
      let graphHullsDialog = []
      console.log(this.superGraphData[nodeIndex].edges)
      this.clusterClass = this.superGraphData[nodeIndex].label
      let uniqueNodes = [];
      for (let i = 0; i < this.superGraphData[nodeIndex].edges.length; i++) {
        let member = [];
        member.push("超边" + i)
        graphDataDialog.nodes.push({
          id: "超边" + i,
          label: "超边" + i + "-类别" + this.superGraphData[nodeIndex].edges[i]["relation"],
          size: 30,
          style: {
            stroke: "#ff0000",
            fillOpacity: 0,
            strokeOpacity: 0,
          },
        });
        for (let j of this.superGraphData[nodeIndex].edges[i]["entities"]) {
          if (uniqueNodes.indexOf(j) < 0) {
            uniqueNodes.push(j)
            graphDataDialog.nodes.push({
              id: "node" + j,
              label: j + "",
              size: 30,
              style: {
                fill: "#588c73",
              },
            });
          }
          member.push("node" + j)
          graphDataDialog.edges.push({
            id: graphDataDialog.edges.length,
            source: "node" + j,
            target: "超边" + i,
            size: 3,
            style: {
              stroke: "#ff0000",
              opacity: 0,
              fillOpacity: 0,
              strokeOpacity: 0,
            },
          });
        }
        graphHullsDialog.push({
          id: "hull" + this.counter++,
          padding: 10,
          members: member,
          style: {
            fill: "#000",
            stroke: "#fff",
          },
        });
      }

      this.graphDataDialog = graphDataDialog
      this.graphHullsDialog = graphHullsDialog
      this.dialogIsChangeFlag = !this.dialogIsChangeFlag
      console.log(this.graphDataDialog, this.graphHullsDialog)
      this.superGraphVisible = true
    },
    clickResGraph(arr) {
      if (arr.length < 1) return;
      
        // let resGraphDataDialog = 
        // this.resGraphDataDialog = resGraphDataDialog
        // resGraphHullsDialog:[],
        // resDialogIsChangeFlag:false,
      let nodeIndex = arr[0]._cfg.id
      let resGraphDataDialog = {
        nodes: [],
        edges: []
      }
      let resGraphHullsDialog = []
      console.log(this.resAllSuperGraphData[nodeIndex].edges)
      this.clusterClass = this.resAllSuperGraphData[nodeIndex].label
      let uniqueNodes = [];
      for (let i = 0; i < this.resAllSuperGraphData[nodeIndex].edges.length; i++) {
        let member = [];
        member.push("超边" + i)
        resGraphDataDialog.nodes.push({
          id: "超边" + i,
          label: "超边" + i + "-类别" + this.resAllSuperGraphData[nodeIndex].edges[i]["relation"],
          size: 30,
          style: {
            stroke: "#ff0000",
            fillOpacity: 0,
            strokeOpacity: 0,
          },
        });
        for (let j of this.resAllSuperGraphData[nodeIndex].edges[i]["entities"]) {
          if (uniqueNodes.indexOf(j) < 0) {
            uniqueNodes.push(j)
            resGraphDataDialog.nodes.push({
              id: "node" + j,
              label: j + "",
              size: 30,
              style: {
                fill: "#588c73",
              },
            });
          }
          member.push("node" + j)
          resGraphDataDialog.edges.push({
            id: resGraphDataDialog.edges.length,
            source: "node" + j,
            target: "超边" + i,
            size: 3,
            style: {
              stroke: "#ff0000",
              opacity: 0,
              fillOpacity: 0,
              strokeOpacity: 0,
            },
          });
        }
        resGraphHullsDialog.push({
          id: "hull" + this.counter++,
          padding: 10,
          members: member,
          style: {
            fill: "#000",
            stroke: "#fff",
          },
        });
      }

      this.resGraphDataDialog = resGraphDataDialog
      this.resGraphHullsDialog = resGraphHullsDialog
      this.resDialogIsChangeFlag = !this.resDialogIsChangeFlag
      // console.log(this.graphDataDialog, this.graphHullsDialog)
      this.ressuperGraphVisible = true
    },
    DBscanCluster() {
      console.log(this.dataSource, this.ruleSource)
      console.log(this.selectRules)
      if (this.dataSource==='rules_3') {
        this.$message.error('该数据集过大不便展示，请选择其他数据集！')
        return
      }
      dbcluster(this.dataSource, "[" + this.selectRules.join(",") + "]").then(res => {
        console.log(res)
        let resGraphData = JSON.parse(JSON.stringify(this.graphData))
        for (let i of Object.keys(res.data.embedding)) {
          let type = res.data.label[i]
          resGraphData.nodes.push({
            id: i + "",
            label: i + "",
            size: 80,
            fx: res.data.embedding[i][0] * 5+350,
            fy: res.data.embedding[i][1] * 5+250,
            style: {
              fill: this.colorList[type],
            },
          })
        }
        console.log(resGraphData)
        this.resGraphData = resGraphData
        this.resIsChangeFlag = !this.resIsChangeFlag
        this.selectRules = []
      }).catch(res => {
        console.log(res)
      })
    },
    loadData() {
      if (this.dataSource==='rules_3') {
        this.$message.error('该数据集过大不便展示，请选择其他数据集！')
        return
      }
      dataList3_3(this.dataSource).then(res => {
        console.log(res)

        let graphData = {
          nodes: [],
          edges: []
        }
        for (let i of Object.keys(res.data.embedding)) {
          let type = res.data.cases[i]["label"]
          graphData.nodes.push({
            id: i + "",
            label: i + "",
            fx: res.data.embedding[i][0] * 5+350,
            fy: res.data.embedding[i][1] * 5+250,
            style: {
              fill: this.colorList[type],
            },
          })
        }
        this.graphData = graphData
        console.log(this.graphData)
        this.isChangeFlag = !this.isChangeFlag
        this.superGraphData = res.data.cases//////////////
        // this.resAllSuperGraphData = JSON.parse(JSON.stringify(res.data.cases))
        // console.log(this.resAllSuperGraphData, this.superGraphData)
      }).then(res => {
        this.loadRules()
      }).catch(res => {
        console.log(res)
      })
    }
  }
}
</script>


