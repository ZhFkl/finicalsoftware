<template>
  <div>
    <el-row>
      <el-col :span="leftPart" style="height:900px">
        <!-- <div
          :style="{ height: '900px', width: '100%' }"
          id="originGraph"
        ></div> -->
        <tmp-graph
          :graphData="graphData"
          :hulls="beforeHulls"
          :ind="0"
           @choosePoint="getChoosePoint" 
           :isChange="isChange"
        ></tmp-graph>
      </el-col>
      <el-col :span="24-leftPart" style="height:900px">
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
  </div>
</template>

<script>
// 引入基本模板
import G6 from "@antv/g6";
// import graphData from "@/js/data";
import * as apiDataShow from "@/api/data_show";
import TmpGraph from "./../../components/myGraph.vue";

export default {
  name: "HyperReasoning",
  components: { TmpGraph },
  data() {
    return {
      isShow: false,
      leftPart: 19,
      // leftPartWidth: "100%",
      oldLinks: [],
      newLinks: [],
      addLinks: [],
      allPoints: [],
      highlightPoints: [],
      otherPoints: [],
      graphData: {},
      afterGraphData: [],
      tableData: [],
      beforeHulls: [],
      afterHulls: [],
      isChange:false,
      nodeInfo:[]
    };
  },
  methods: {
    handleReasoning() {
      this.leftPart = 12;
      this.leftPartWidth = "700px";
      // this.$nextTick(() => {
      // let myChart = echarts.getInstanceByDom(
      //   document.getElementById("originGraph")
      // );
      // myChart.resize("700px");
      // });
      this.setGraph("reasonGraph");
      this.isShow = true;

      // let tmpLinks = this.newLinks.concat(this.addLinks);
      // let tmpGraphs = [];
      // let str = [];
      // for (let i = 0; i < this.otherPoints.length; i++) {
      //   if (str.indexOf(this.otherPoints[i]) < 0) {
      //     tmpGraphs.push({
      //       name: this.otherPoints[i],
      //       tooltip: this.otherPoints[i],
      //       category: 0,
      //       symbolSize: 20,
      //       label: {
      //         show: true,
      //       },
      //     });
      //     str.push(this.otherPoints[i]);
      //   } else continue;
      // }
      // for (let i = 0; i < this.highlightPoints.length; i++) {
      //   if (str.indexOf(this.highlightPoints[i]) < 0) {
      //     tmpGraphs.push({
      //       name: this.highlightPoints[i],
      //       tooltip: this.highlightPoints[i],
      //       category: 1,
      //       symbolSize: 20,
      //       label: {
      //         show: true,
      //       },
      //     });
      //     str.push(this.highlightPoints[i]);
      //   } else continue;
      // }
    },
    getChoosePoint(val) {
      console.log(val);
      this.nodeInfo=[]
      this.nodeInfo.push({
        label:'ID',
        value:val[0]._cfg.id
      });
      this.nodeInfo.push({
        label:'label',
        value:val[0]._cfg.model.label
      });
      this.nodeInfo.push({
        label:'type',
        value:val[0]._cfg.model.style.fill==="#f2e394"?'company':'people'
      });
      for(let i of Object.keys(val[0]._cfg.model.myData)){
        this.nodeInfo.push({
        label:i,
        value:val[0]._cfg.model.myData[i]
      });
      }
      // this.choosenPointLabel = val[0]._cfg.model.label
      // this.choosenPointType = val[0]._cfg.model.style.fill==="#f2e394"?'company':'people'

      // api.getNodeInfo({entity_id:val[0]._cfg.id, dataset:this.dataSource}).then(res =>{
      //   console.log(res)
      //   this.nodeInfo=[]
      //   for(let i of Object.keys(res.data)){
      //     this.nodeInfo.push({
      //       label:i,
      //       value:res.data[i]
      //     })
      //   }
      // }).catch(res=>{
      //   console.log(res)
      // })
    },
    setGraph(name) {
      // 基于准备好的dom，初始化echarts实例
      // let myChart = echarts.init(document.getElementById(name));
      let graph = new G6.Graph({
        container: name,
        // width: 1500,
        height: 900,
        modes: {
          default: ["drag-canvas", "zoom-canvas", "drag-node", "lasso-select"],
        },
        layout: {
          type: "force",
          preventOverlap: true,
          linkDistance: 100,
          nodeStrength: -50,
          edgeStrength: 0.7,
          // edgeStrength: (d) => {
          //   if (
          //     d.source.id === "node1" ||
          //     d.source.id === "node2" ||
          //     d.source.id === "node3"
          //   ) {
          //     return 0.7;
          //   }
          //   return 0.1;
          // },
        },
      });
      if (name === "reasonGraph") {
        this.graphData.edges = this.graphData.edges.concat(this.afterGraphData);
      }
      graph.data({
        nodes: this.graphData.nodes,
        edges: this.graphData.edges.map(function (edge, i) {
          edge["id"] = "edge" + i;
          return Object.assign({}, edge);
        }),
      });
      graph.render();

      graph.on("afterlayout", () => {
        let rec = [];
        let tmp = null;
        for (let i of this.beforeHulls) {
          tmp = graph.createHull(i);
          rec.push(tmp);
        }
        if (name === "reasonGraph") {
          for (let i of this.afterHulls) {
            tmp = graph.createHull(i);
            rec.push(tmp);
          }
        }
        // const hull1 = graph.createHull({
        //   id: "centerNode-hull",
        //   type: "bubble",
        //   members: centerNodes,
        //   padding: 10,
        // });
        // for (let i of this.beforeHulls) {
        // }
        // const hull2 = graph.createHull({
        //   id: "leafNode-hull1",
        //   type: "bubble",
        //   members: ["node6", "node7", "node8"],
        //   padding: 10,
        //   style: {
        //     fill: "lightgreen",
        //     stroke: "green",
        //   },
        // });

        // const hull3 = graph.createHull({
        //   id: "leafNode-hull2",
        //   type: "bubble",
        //   members: ["node8", "node9", "node10", "node11", "node12", "node13"],
        //   padding: 10,
        //   style: {
        //     fill: "lightred",
        //     stroke: "red",
        //   },
        // });
        graph.on("afterupdateitem", (e) => {
          for (let i of rec) i.updateData(i.members);
        });

        // graph.on("afterupdateitem", (e) => {
        //   hull1.updateData(hull1.members);
        //   hull2.updateData(hull2.members);
        //   hull3.updateData(hull3.members);
        // });
      });

      // if (typeof window !== 'undefined')
      //   window.onresize = () => {
      //     if (!graph || graph.get('destroyed')) return;
      //     if (!container || !container.scrollWidth || !container.scrollHeight) return;
      //     graph.changeSize(container.scrollWidth, container.scrollHeight - 20);
      //   };
    },
    getDateStr(tmp){
      let date = new Date(parseInt(tmp));
      let Y = date.getFullYear() + '-';
      let M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-';
      let D = date.getDate() + ' ';
      let h = date.getHours() + ':';
      let m = date.getMinutes() + ':';
      let s = date.getSeconds(); 
      return Y+M+D+h+m+s
    },
    getPicData() {
      apiDataShow.digSubgraph()
        .then((res) => {
          console.log(res)
          this.graphData.nodes = [];
          this.graphData.edges = [];
          let counter = 1;
          let uniqueNodes = [];

          for(let i of Object.keys(res.data)){
            let member = []
            member.push(counter+"");
            this.graphData.nodes.push({
              id: counter+"",
              label: "共同持股-超边"+counter,
              size: 30,
              style: {
                stroke: "#ff0000",
                fillOpacity: 0,
                strokeOpacity: 0,
              }
            });
            let start_time = res.data[i]['start_time'].length>0?this.getDateStr(res.data[i]['start_time']):""
            let end_time = res.data[i]['end_time'].length>0?this.getDateStr(res.data[i]['end_time']):""
            let company_id = res.data[i]['company_id']
            for(let j of Object.keys(res.data[i])){
                  if (j === "start_time" || j === "end_time" || j==='company_id') {
                continue;
              }
              member.push(res.data[i][j].entity_id);
              if (uniqueNodes.indexOf(res.data[i][j].entity_id) < 0) {
                uniqueNodes.push(res.data[i][j].entity_id);
                this.graphData.nodes.push({
                  id: res.data[i][j].entity_id,
                  label: res.data[i][j].name,
                  size: 30,
                  style: {
                    fill:
                      res.data[i][j]["type"] === 0 ? "#588c73" : "#f2e394",
                  },
                  myData:{
                    start_time:start_time,
                    end_time:end_time,
                    company_id:company_id
                  }
                });
              }
              this.graphData.edges.push({
                source: res.data[i][j].entity_id,
                target: counter+"",
                size: 3,
                style: {
                  stroke: "#ff0000",
                  opacity: 0,
                  fillOpacity: 0,
                  strokeOpacity: 0,
                },
              });
            }
              this.beforeHulls.push({
              id: "beforeHull" + counter++,
              padding: 10,
              members: member,
              style: {
                fill: "#000",
                stroke: "#fff",
              },
            });
          }
          this.isChange = !this.isChange
          
          // for (let i in res.data) {
          //   let member = [];
          //   member.push(i);
          //   this.graphData.nodes.push({
          //     id: i,
          //     label: i,
          //     size: 30,
          //     style: {
          //       stroke: "#ff0000",
          //       fillOpacity: 0,
          //       strokeOpacity: 0,
          //     },
          //   });
          //   for (let j in res.data[i]) {
          //     if (j === "start_time" || j === "end_time") {
          //       continue;
          //     }
          //     member.push(j);
          //     if (uniqueNodes.indexOf(j) < 0) {
          //       uniqueNodes.push(j);
          //       this.graphData.nodes.push({
          //         id: j,
          //         label: j,
          //         size: 30,
          //         style: {
          //           fill:
          //             res.data[i][j]["type"] === "0" ? "#588c73" : "#f2e394",
          //         },
          //       });
          //     }
          //     this.graphData.edges.push({
          //       source: i,
          //       target: j,
          //       size: 3,
          //       style: {
          //         stroke: "#ff0000",
          //         opacity: 0,
          //         fillOpacity: 0,
          //         strokeOpacity: 0,
          //       },
          //     });
          //   }
          //   this.beforeHulls.push({
          //     id: "beforeHull" + counter++,
          //     padding: 10,
          //     members: member,
          //     style: {
          //       fill: "#000",
          //       stroke: "#fff",
          //     },
          //   });
          // }
          // console.log(this.graphData, this.beforeHulls);

          // this.setGraph("originGraph");
        })
        .catch((res) => {
          console.log(res);
        });
    },
  },
  mounted() {
    this.getPicData();
  },
};
</script>

<style lang="scss" scoped>
#originGraph,
#reasonGraph {
  background-color: rgba(255, 255, 255, 0.8);
}
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
