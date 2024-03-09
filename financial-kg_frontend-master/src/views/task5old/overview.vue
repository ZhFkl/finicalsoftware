<template>
  <div class="my-wrapper">
    <div class="my-title">子任务三-总览</div>
    <div class="my-content">
      <el-row type="flex" align="middle">
        <el-col :span="4">1. 请选择数据源：</el-col>
        <el-col :span="10">
          <el-select size="small" style="width: 100%" v-model="dataSource">
            <el-option v-for="item in dataSourceOptions" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="5" :offset="1">
          <el-button type="primary" size="small" @click="loadData">加载数据</el-button>
        </el-col>
      </el-row>

      <adminDashboard style="margin-top: 10px" v-for="item in statisticData" :key="item.label[0]"
        :value1="item.value[0]" :value2="item.value[1]" :value3="item.value[2]" :label1="'节点数'" :label2="'边数'"
        :label3="'规则数'">
      </adminDashboard>
      <el-row style="margin-top: 10px">
        <el-col :span="4">2. filtration处理：</el-col>
        <el-col :span="10">
          <el-form ref="filtrationForm" :model="filtrationForm" label-width="100px" label-position="left">
            <el-form-item label="Layer层数">
              <el-select v-model="filtrationForm.layer" size="small">
                <el-option :key="index" v-for="(item, index) in layerList" :label="item" :value="item"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="filtration参数">
              <el-radio-group v-model="filtrationForm.fullness">
                <el-radio label="full">full</el-radio>
                <el-radio label="partial">partial</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-form>
        </el-col>
        <el-col :span="5" :offset="1">
          <el-button type="primary" size="small" @click="filtrationData">确定</el-button>
        </el-col>
      </el-row>

      <el-row style="margin-top: 10px">
        <el-col :span="4">3. 请输入想要查看对比的节点编号
          <span v-if="filtrationLength === -1">(请先进行filtration操作)</span>
          <span v-else>(0-{{ filtrationLength - 1 }})</span>
        </el-col>
        <el-col :span="10">
          <el-input size="small" v-model="filtrationIndex"></el-input>
        </el-col>
        <el-col :span="5" :offset="1">
          <el-button type="primary" size="small" @click="setFiltrationGraph">确定</el-button>
          <!-- @click="filtrationData" -->
        </el-col>
      </el-row>

      <el-row style="height:400px">
        <el-col :span="12" style="height:100%">
          <tmp-graph :graphData="graphDataBefore" :hulls="graphHullsBefore" :isChange="isChangeBefore" :ind="0"
            :picLabel="'filtration前'"></tmp-graph>
        </el-col>
        <el-col :span="12" style="height:100%">
          <tmp-graph :graphData="graphDataAfter" :hulls="graphHullsAfter" :isChange="isChangeAfter" :ind="1"
            :picLabel="'filtration后'"></tmp-graph>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import TmpGraph from "./../../components/myGraph.vue";
import adminDashboard from "../topic1/admin";
import { dataList, datainfo, filtration, dataFiltrationinfo } from "@/api/topic3";
export default {
  name: "overview",

  components: { TmpGraph, adminDashboard },
  data() {
    return {
      counter: 0,
      graphDataBefore: {},
      graphDataAfter: {},
      graphHullsBefore: [],
      graphHullsAfter: [],
      isChangeBefore: false,
      isChangeAfter: false,
      filtrationLength: -1,
      filtrationBefore: [],
      filtrationAfter: [],
      filtrationIndex: "",
      dataSource: "",
      dataSourceOptions: [],
      statisticData: [],
      layerList: [2, 3, 4, 5],
      filtrationForm: {
        layer: "",
        fullness: "",
      },
      showResult: false,
    };
  },
  mounted() {
    dataList()
      .then((res) => {
        console.log(res);
        this.dataSourceOptions = res.data.map((val) => {
          return { value: val, label: val };
        });
      })
      .catch((e) => console.log(e.message));
  },
  methods: {
    loadData() {
      if (this.dataSource === "") {
        this.$message.error("请选择数据源！");
        return;
      }
      datainfo(this.dataSource)
        .then((res) => {
          //   this.showData = true;
          console.log(res);
          this.statisticData = [];
          let keys = Object.keys(res.data);
          let obj = Object.create({ label: [], value: [] });
          for (let i = 0; i < keys.length; i++) {
            let sum = 0;
            if (typeof res.data[keys[i]] === "object") {
              // for(let j in res.data[keys[i]]){
              //   sum+=res.data[keys[i]][j];
              // }
              continue;
            } else sum = res.data[keys[i]];
            obj.label.push(keys[i]);
            obj.value.push(sum);
            if ((i + 1) % 3 === 0) {
              this.statisticData.push(obj);
              obj = Object.create({ label: [], value: [] });
            }
          }

          this.$store.dispatch("topic3/setDataset", this.dataSource);
        })
        .catch((e) => {
          console.log(e.message);
        });
    },

    filtrationData() {
      console.log(this.filtrationForm, this.dataSource);
      filtration(
        this.dataSource,
        this.filtrationForm.layer,
        this.filtrationForm.fullness
      ).then((res) => {
        return res.data
      }).then(dataName => {
        console.log(dataName)
        Promise.all([dataFiltrationinfo(dataName), dataFiltrationinfo(this.dataSource)]).then(res => {
          console.log(res)
          this.filtrationLength = Object.keys(res[0].data).length
          this.filtrationBefore = res[1].data
          this.filtrationAfter = res[0].data
        }).catch(err => {
          console.log(err)
        })
      }).catch(err => {
        console.log(err)
      })
    },
    setFiltrationGraph() {
      let BeforeData = this.filtrationBefore[this.filtrationIndex]
      let AfterData = this.filtrationAfter[this.filtrationIndex]
      let graphDataBefore = {
        nodes: [],
        edges: []
      }
      let graphDataAfter = {
        nodes: [],
        edges: []
      }
      let graphHullsBefore = [], graphHullsAfter = []

      let uniqueNodes = [];
      console.log(BeforeData, AfterData)
      for (let i = 0; i < BeforeData.edges.length; i++) {
        let member = [];
        member.push("超边" + i)
        graphDataBefore.nodes.push({
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
            graphDataBefore.nodes.push({
              id: "node" + j,
              label: j + "",
              size: 30,
              style: {
                fill: "#588c73",
              },
            });
          }
          member.push("node" + j)
          graphDataBefore.edges.push({
            id: graphDataBefore.edges.length,
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
        graphHullsBefore.push({
          id: "hull" + this.counter++,
          padding: 10,
          members: member,
          style: {
            fill: "#000",
            stroke: "#fff",
          },
        });
      }

      let uniqueNodes2 = [];

      for (let i = 0; i < AfterData.edges.length; i++) {
        let member = [];
        member.push("超边" + i)
        graphDataAfter.nodes.push({
          id: "超边" + i,
          label: "超边" + i + "-类别" + AfterData.edges[i]["relation"],
          size: 30,
          style: {
            stroke: "#ff0000",
            fillOpacity: 0,
            strokeOpacity: 0,
          },
        });
        for (let j of AfterData.edges[i]["entities"]) {
          if (uniqueNodes2.indexOf(j) < 0) {
            uniqueNodes2.push(j)
            graphDataAfter.nodes.push({
              id: "node" + j,
              label: j + "",
              size: 30,
              style: {
                fill: "#588c73",
              },
            });
          }
          member.push("node" + j)
          graphDataAfter.edges.push({
            id: graphDataAfter.edges.length,
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
        graphHullsAfter.push({
          id: "hull" + this.counter++,
          padding: 10,
          members: member,
          style: {
            fill: "#000",
            stroke: "#fff",
          },
        });
      }

      // this.showResult=true;
      this.graphDataBefore = graphDataBefore;
      this.graphDataAfter = graphDataAfter;
      this.graphHullsBefore = graphHullsBefore;
      this.graphHullsAfter = graphHullsAfter;
      this.isChangeBefore = !this.isChangeBefore;
      this.isChangeAfter = !this.isChangeAfter;

      console.log(this.graphDataBefore, this.graphDataAfter)
      console.log(this.graphHullsBefore, this.graphHullsAfter)
    }
  },
};
</script>


