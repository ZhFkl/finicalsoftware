<template>
  <div class="my-wrapper">

    <!-- title -->
    <div class="my-title">
      图立方的复杂查询
    </div>

    <div class="my-content">

      <!-- dataset selector -->
      <el-row type="flex" align="middle">
        <el-col :span="4">请选择超图数据集：</el-col>
        <el-col :span="10">
          <el-select size="small" style="width: 100%" v-model="dataset">
            <el-option
              v-for="item in datasetOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="5" :offset="1">
          <el-button type="primary" size="small" @click="getDatasetInfo">查看数据集信息</el-button>
        </el-col>
      </el-row>

      <!-- hyper query selector -->
      <el-row type="flex" align="middle"  style="margin-bottom:10px;margin-top:10px">
        <el-col :span="4">请选择查询语句：</el-col>
        <el-col :span="10">
          <el-select size="small" style="width: 100%" v-model="query">
            <el-option
              v-for="item in queryOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="5" :offset="1">
          <!-- <el-button type="primary" size="small" @click="getQueryContent">查看查询内容</el-button> -->
          <el-button type="primary" size="small" @click="getQueryResult">查看查询结果</el-button>
        </el-col>
      </el-row>

      <!-- hyper query text && result display -->
      <el-row style=" height: 500px; margin-top: 10px">
        <el-col :span="18" style="height:100%">
          
          <!-- hyper query text display -->
          <el-card  v-if="showQueryContent" style="white-space: pre-wrap;" class="box-card">
            <div slot="header" class="clearfix">
              <span>查询请求</span>
            </div>
            {{queryContent}}
          </el-card>

          <!-- hyper query result table -->
          <el-card  v-if="showQueryResult" style="white-space: pre-wrap;" class="box-card">
            <div slot="header" class="clearfix">
              <span>查询结果（显示全部{{queryResult.rows}}条结果中的前{{queryResult.rows > 5000 ? 5000: queryResult.rows}}条）</span>
            </div>

            <!-- <el-table :data="queryResult.tableData" border>
              <div v-for="(variable, index) in queryResult.variables" :key="index">
                <el-table-column :prop="variable" :label="variable" align="center">
              </el-table-column>
              </div>
            </el-table> -->

            <el-table :data="queryResult.tableData.slice((rulePage.curPage - 1) * rulePage.pageSize, rulePage.curPage * rulePage.pageSize)" border>
              <div v-for="(variable, index) in queryResult.variables" :key="index">
                <el-table-column :prop="variable" :label="variable" align="center">
              </el-table-column>
              </div>
            </el-table>
            <el-pagination
              background
              layout="prev, pager, next"
              :total="rulePage.total" 
              :current-page="rulePage.curPage"
              :page-size="rulePage.pageSize"
              @current-change="handlePageChange">
            </el-pagination>

            查询执行时延：{{queryResult.latency}} 微秒
          </el-card>
        </el-col>

        <el-col :span="6">
          <el-card  v-if="showDatasetInfo">
            <div slot="header" class="clearfix">
              <span>数据集信息</span>
            </div>
            <div>数据集名称：{{datasetInfo.name}}</div>
            <div>顶点数量：{{datasetInfo.vertex}}</div>
            <div>三元组数量：{{datasetInfo.triple}}</div>
          </el-card>
        </el-col>
      </el-row>

    </div>
  </div>
</template>

<script>
// import fs from 'fs'
import queryData from '../../assets/topic-query-results/topic-hyper-result.json'

export default {
  name: "task23",
  data() {
    return {
      showDatasetInfo: false,
      showQueryContent: false,
      showQueryResult: false,
      dataset:'',
      datasetOptions: [
        {label: "hypergraph_30", value: 1,}
      ],
      datasetInfo:{
          name: "graphcube-30-hyper", 
          vertex: "30万", 
          triple: "30万", 
      },
      rulePage:"",
      query:'',
      queryContent: '',
      queryOptions: [
        {label: "简单查询-V2E查询1", value: 0,}, 
        {label: "简单查询-V2E查询2", value: 1,}, 
        {label: "简单查询-E2V查询1", value: 2,}, 
        {label: "简单查询-E2V查询2", value: 3,},
        {label: "简单查询-E2E查询1", value: 4,},
        {label: "简单查询-E2E查询2", value: 5,},
        {label: "简单查询-E2E查询3", value: 6,},
        {label: "简单查询-V2V查询", value: 7,},
        {label: "复杂查询-二跳查询1", value: 8,},
        {label: "复杂查询-二跳查询2", value: 9,},
        {label: "复杂查询-二跳查询3", value: 10,},
        {label: "复杂查询-三跳查询", value: 11,},
        {label: "复杂查询-四跳查询", value: 12,},
        {label: "复杂查询-五跳查询1", value: 13,},
        {label: "复杂查询-五跳查询2", value: 14,},
        ],
      queryResult: {}
    }
  },

  mounted() {},
  methods: {
    getDatasetInfo() {
      if(this.dataset===''){
        this.$message.error('请选择数据集！');
        return;
      }
      this.showDatasetInfo = true;
    },

    getQueryContent() {
      if(this.dataset===''){
        this.$message.error('请选择数据集！');
        return;
      }
      if(this.query===''){
        this.$message.error('请选择查询！');
        return;
      }
      // this.queryContent = "\t PREFIX ub: <http://swat.cse.lehigh.edu/onto/univ-bench.owl#>\n \
      //           SELECT ?X ?S ?E WHERE {\n \
      //           \t [?S, ?E]  ?X  ub:subOrganizationOf  <http://www.Company1.Group10059.com>  .\n \
      //           }"
      this.queryContent = queryData[this.query].content
      this.showQueryContent = true
    },

    getQueryResult() {
      if(this.dataset===''){
        this.$message.error('请选择数据集！');
        return;
      }
      if(this.query===''){
        this.$message.error('请选择查询！');
        return;
      }
      this.queryContent = queryData[this.query].content
      this.queryResult = queryData[this.query].result
      this.showQueryContent = true
      this.showQueryResult = true
      this.rulePage = {
        curPage: 1,
        pageSize: 50,
        total: this.queryResult.rows > 5000 ? 5000 : this.queryResult.rows
      };
      // console.log(this.queryResult);
    },

    handlePageChange(val) {
      this.rulePage.curPage =  val;
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