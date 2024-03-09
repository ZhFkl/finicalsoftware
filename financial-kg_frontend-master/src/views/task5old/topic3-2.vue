<template>
  <div class="my-wrapper">
    <div class="my-title">基于“图立方”嵌入的聚类归纳方法</div>
    <div class="my-content">
      <el-row type="flex" align="middle">
        <el-col :span="4">1. 请选择金融数据集：</el-col>
        <el-col :span="10">
          <el-select v-model="dataSource" size="small" style="width: 100%">
            <el-option v-for="item in dataSourceOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-col>
        <el-col :span="5" :offset="1">
          <!-- <el-button type="primary" size="small" @click="loadData">加载数据</el-button> -->
        </el-col>
      </el-row>

      <el-row type="flex" align="middle" style="margin-top:10px">
        <el-col :span="4">2. 请选择嵌入的方法：</el-col>
        <el-col :span="10">
          <el-cascader v-model="embeddingMethod" size="small" style="width:100%" :options="embeddingMethodOptions" />
        </el-col>
        <!-- <el-col :span="5" :offset="1">
          <el-button type="primary" size="small" @click="clusterData">确定</el-button>
        </el-col> -->
      </el-row>
      <el-row type="flex" align="middle" style="margin-top:10px">
        <el-col :span="4">3. 请选择聚类的方法：</el-col>
        <el-col :span="10">
          <el-cascader v-model="clusterMethod" size="small" style="width:100%" :options="clusterMethodOptions" />
        </el-col>
        <!-- <el-col :span="5" :offset="1">
          <el-button type="primary" size="small" @click="clusterData">确定</el-button>
        </el-col> -->
      </el-row>

      <el-row type="flex" align="middle" style="margin-top:10px">
        <el-col :span="4">4. 请填写期待分类数：</el-col>
        <el-col :span="10">
          <el-input v-model="classNumber" size="small" />
        </el-col>
      </el-row>

      <el-row type="flex" align="middle" style="margin-top:10px">
        <el-col :span="4">5. 是否用filtration增强：</el-col>
        <el-col :span="10">
          <el-radio-group v-model="ifFiltration">
            <el-radio :label="true">是</el-radio>
            <el-radio :label="false">否</el-radio>
          </el-radio-group>
        </el-col>
        <el-col :span="5" :offset="1">
          <el-button type="primary" size="small" @click="clusterData">确定</el-button>
        </el-col>
      </el-row>

      <el-row v-show="showResult">
        <el-descriptions title="评估指标：" :column="2" border style="margin-top:20px">
          <el-descriptions-item v-for="(item, index) in metricList" :key="index" :label-style="{'width':'200px'}">
            <template slot="label">
              <i class="el-icon-tickets" />
              {{ item.label }}
            </template>
            {{ item.value }}
          </el-descriptions-item>
        </el-descriptions>
      </el-row>
      <el-row v-if="showResult" style="margin-top: 10px">
        <el-col :span="12" style="height:440px">
          <!-- <el-image
            :src="img.tree"
            fit="contain"></el-image>
          <div class="graph-title">
            推理树
          </div> -->
          <tmp-graph :graph-data="graphData" :hulls="graphHulls" :is-change="isChangeFlag" :ind="0" @choosePoint="clickGraph" />
          <div class="graph-title">
            规则散点图
          </div>
        </el-col>
        <el-col :span="12">
          <!-- <el-image :src="img.scatter" fit="contain"></el-image> -->
          <el-image
            :src="img.tree"
            fit="contain"
          />
          <div class="graph-title">
            推理树
          </div>
        </el-col>
      </el-row>
      <div v-if="showMotifResult">
          <el-image :src="require('./motif.gif')" fit="contain" />
      </div>

      <el-dialog :title="'规则'+dialogNodeIndex+'超图'" :visible.sync="superGraphVisible" width="50%">
        <div style="width:100%;height:350px">

          <tmp-graph :graph-data="graphDataDialog" :hulls="graphHullsDialog" :is-change="dialogIsChangeFlag" :ind="1" />
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>

import { dataList, datainfo, kernel, infohyper, motif } from '@/api/topic3'

import TmpGraph from './../../components/myGraph.vue'
export default {

  name: 'Topic32',
  components: { TmpGraph },
  data() {
    return {
      showMotifResult:false,
      ifFiltration:"",
      colorList: ['#36b5e6', '#ff5219', '#ffa806', '#57b728', '#f6ec46',
        '#ff39a0', '#ff9f9f', '#bc371d', '#9032ba'],
      clusterClass: -1,
      counter: 0,
      dialogIsChangeFlag: false,
      isChangeFlag: false,
      superGraphVisible: false,
      graphData: {},
      graphHulls: [],
      graphDataDialog: {},
      graphHullsDialog: [],
      dataSource: '',
      dataSourceOptions: [
        {
          label: '数据1',
          value: 1
        },
        {
          label: '数据2',
          value: 2
        },
        {
          label: '数据3',
          value: 3
        }
      ],
      embeddingMethod: [],
      embeddingMethodOptions: [
        {
          label: '基于深度学习',
          value: 'infohyper'
        },
        {
          label: '基于motif',
          value: 'motif'
        }
      ],
      clusterMethod: [],
      clusterMethodOptions: [
        {
          label: 'exkmeans',
          value: '1'
        }
      ],
      classNumber: '',
      img: {
        url: process.env.VUE_APP_BASE_API,
        tree: '',
        scatter: ''
      },
      showResult: false,
      dialogNodeIndex: 0,
      metricList: [{
        label: '聚类系数',
        value: '0'
      }, {
        label: '时间',
        value: '3.54s'
      }]
    }
  },
  mounted() {
    this.graphData = {
      nodes: [],
      edges: []
    }
    dataList()
      .then((res) => {
        console.log(res)
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
      .catch((e) => console.log(e.message))
  },
  methods: {
    clickGraph(arr) {
      if (arr.length < 1) return
      // superGraphData
      // graphDataDialog: {},
      // graphHullsDialog: [],
      const nodeIndex = arr[0]._cfg.id
      this.dialogNodeIndex = nodeIndex
      const graphDataDialog = {
        nodes: [],
        edges: []
      }
      const graphHullsDialog = []
      console.log(this.superGraphData[nodeIndex].edges)
      this.clusterClass = this.superGraphData[nodeIndex].label
      const uniqueNodes = []
      for (let i = 0; i < this.superGraphData[nodeIndex].edges.length; i++) {
        const member = []
        member.push('超边' + i)
        graphDataDialog.nodes.push({
          id: '超边' + i,
          label: '超边' + i + '-类别' + this.superGraphData[nodeIndex].edges[i]['relation'],
          size: 30,
          style: {
            stroke: '#ff0000',
            fillOpacity: 0,
            strokeOpacity: 0
          }
        })
        for (const j of this.superGraphData[nodeIndex].edges[i]['entities']) {
          if (uniqueNodes.indexOf(j) < 0) {
            uniqueNodes.push(j)
            graphDataDialog.nodes.push({
              id: 'node' + j,
              label: j + '',
              size: 30,
              style: {
                fill: '#588c73'
              }
            })
          }
          member.push('node' + j)
          graphDataDialog.edges.push({
            id: graphDataDialog.edges.length,
            source: 'node' + j,
            target: '超边' + i,
            size: 3,
            style: {
              stroke: '#ff0000',
              opacity: 0,
              fillOpacity: 0,
              strokeOpacity: 0
            }
          })
        }
        graphHullsDialog.push({
          id: 'hull' + this.counter++,
          padding: 10,
          members: member,
          style: {
            fill: '#000',
            stroke: '#fff'
          }
        })
      }

      this.graphDataDialog = graphDataDialog
      this.graphHullsDialog = graphHullsDialog
      this.dialogIsChangeFlag = !this.dialogIsChangeFlag
      console.log(this.graphDataDialog, this.graphHullsDialog)
      this.superGraphVisible = true
    },
    clusterData() {
      if (this.dataSource === '') {
        this.$message.error('请选择数据源！')
        return
      }
      if (this.embeddingMethod.length === 0) {
        this.$message.error('请选择聚类方式！')
        return
      }
      if(this.embeddingMethod[0]!=='motif' && this.dataSource==='rules_3'){
        this.$message.error('因时间原因rules_3暂时只支持motif方法，请重新选择！')
        return
      }

      if (this.embeddingMethod[0] === 'infohyper') {
        infohyper({
          dataset: this.dataSource,
          k: parseInt(this.classNumber),
          use_filtration:this.ifFiltration
        })
          .then((res) => {
            console.log(res)
            // this.img.scatter = this.img.url + res.data.scatter_path;
            this.img.tree = this.img.url + res.data.tree_path
            this.metricList = [];
            this.metricList.push({
              label:'SSE',
              value:res.data.SSE});
              
            this.metricList.push({
              label:'时间',
              value:res.data.time+'s'})
            const graphData = {
              nodes: [],
              edges: []
            }
            for (const i of Object.keys(res.data.embedding)) {
              const type = res.data.cases[i].label
              graphData.nodes.push({
                id: i + '',
                label: i + '',
                fx: res.data.embedding[i][0] * 5+300,
                fy: res.data.embedding[i][1] * 5+200,
                style: {
                  fill: this.colorList[type]
                }
              })
            }
            this.graphData = graphData
            console.log(this.graphData)
            this.isChangeFlag = !this.isChangeFlag
            this.superGraphData = res.data.cases
            this.showMotifResult = false
            this.showResult = true
          })
          .catch((e) => {
            console.log(e.message)
          })
      } else {
        motif({
          dataset: this.dataSource,
          k: parseInt(this.classNumber),
          use_filtration:this.ifFiltration
        })
          .then((res) => {
            console.log(res)
            // this.img.scatter = this.img.url + res.data.scatter_path;
            this.img.tree = this.img.url + res.data.tree_path
            this.metricList = [];
            this.metricList.push({
              label:'SSE',
              value:res.data.SSE});
              
            this.metricList.push({
              label:'时间',
              value:res.data.time+'s'})
            const graphData = {
              nodes: [],
              edges: []
            }
            for (const i of Object.keys(res.data.embedding)) {
              const type = res.data.cases[i].label
              graphData.nodes.push({
                id: i + '',
                label: i + '',
                fx: res.data.embedding[i][0] * 5+300,
                fy: res.data.embedding[i][1] * 5+200,
                style: {
                  fill: this.colorList[type]
                }
              })
            }
            this.graphData = graphData
            console.log(this.graphData)
            this.isChangeFlag = !this.isChangeFlag
            this.superGraphData = res.data.cases
            this.showMotifResult = true
            this.showResult = true
          })
          .catch((e) => {
            console.log(e.message)
          })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.graph-title {
  text-align: center;
  font-weight: bold;
  margin-top: 10px;
}

.el-image {
  height: 430px;
}
</style>
