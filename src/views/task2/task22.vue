<template>
  <div class="my-wrapper">
    <div class="my-title">图立方的多跳查询
      <i v-if="!originFlag" class="el-icon-back" @click="originFlag = true;showMetricFlag=false">返回</i>
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
        <el-col :span="4">请选择查询类型：</el-col>
        <el-col :span="10">
          <el-select size="small" style="width: 100%" v-model="queryClass">
            <el-option
              v-for="item in classOptions"
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
        </el-col>
      </el-row>

      <el-row type="flex" align="middle"  style="margin-bottom:10px;margin-top:10px">
        <el-col :span="4">请选择查询请求：</el-col>
        <el-col :span="10">
          <el-select size="small" style="width: 100%" v-model="queryType">
            <el-option
              v-for="item in queryOptions[queryClass]"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="5" :offset="1">
          <el-button type="primary" size="small" @click="handleQuery"
            >查询</el-button
          >
        </el-col>
      </el-row>

      <el-row v-show="showMetricFlag">
        <el-descriptions title="指标描述" :column="2" border>
          <el-descriptions-item v-for="(item, index) in metricList" :key="index" :labelStyle="{'width':'200px'}">
            <template slot="label">
              <i class="el-icon-tickets"></i>
              {{ item.label }}
            </template>
            {{ item.value }}
          </el-descriptions-item>
        </el-descriptions>
      </el-row>

      <el-row v-if="showResults" style=" height: 500px; margin-top: 10px">
        <el-col :span="18" style="height:100%">
          <el-card style="white-space: pre-wrap;" class="box-card">
            <div slot="header" class="clearfix">
              <span>查询请求</span>
            </div>
            {{query.text}}
          </el-card>

          <el-card style="white-space: pre-wrap;" class="box-card">
            <div slot="header" class="clearfix">
              <span>查询结果（显示全部{{query.row}}条结果中的前{{query.row > 5000 ? 5000 : query.row}}条）</span>
            </div>

            <el-table :data="query.results.slice((rulePage.curPage - 1) * rulePage.pageSize, rulePage.curPage * rulePage.pageSize)" border>
              <div v-for="(variable, index) in query.variables" :key="index">
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

            查询执行时延：{{query.latency}}
          </el-card>
        </el-col>

        <el-col :span="6">
          <el-card>
            <div slot="header" class="clearfix">
              <span>数据集信息</span>
            </div>
            <div>{{datasetInfo.name}}</div>
            <div>{{datasetInfo.vertex}}</div>
            <div>{{datasetInfo.triple}}</div>
            <br>
            <a :href="datasetInfo.refer">参考链接</a>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import queries from '../../assets/topic-query-results/topic-time-result.json'
import TmpGraph from "./../../components/myGraph.vue";
import tmpData from "@/js/data";
import *  as api from "@/api/topic2";
export default {
  name: "task22",
  components: { TmpGraph },
  data() {
    return {
      datasetInfo:{name: "数据集名称：FIN-1B-time", vertex: "顶点数量：3.36亿", triple: "三元组数量：10.8亿", refer: "http://swat.cse.lehigh.edu/projects/lubm/"},
      originFlag: true,
      metricList: [
        {label: "指标1", value: "支持十亿级金融时序图谱的高效存储与索引"},
        {label: "指标2", value: "实现时序图谱查询每笔处理平均延时在10毫秒以内"},
        {label: "指标3", value: "十亿级量级下不低于4层时序复杂关系的查询，平均延迟小于1秒"},
      ],
      dataSource: "",
      sourceOptions: [
        {
          label: "FIN-1B-time",
          value: 1,
        },
      ],
      queryClass: "",
      classOptions: [
        {
          label: "一跳查询",
          value: 0,
        },
        {
          label: "二跳查询",
          value: 1,
        },
        {
          label: "四跳普通查询",
          value: 2,
        },
        {
          label: "四跳上限查询",
          value: 3,
        }
      ],
      queryType:'',
      queryOptions: [
        [
          {
            label: "查询1",
            value: 0,
          },
          {
            label: "查询2",
            value: 1,
          },
          {
            label: "查询3",
            value: 2,
          },
        ],
        [
          {
            label: "查询1",
            value: 3,
          },
          {
            label: "查询2",
            value: 4,
          },
          {
            label: "查询3",
            value: 5,
          }
        ],
        [
          {
            label: "查询1",
            value: 6,
          },
          {
            label: "查询2",
            value: 7,
          },
          {
            label: "查询3",
            value: 8,
          }
        ],
        [
          {
            label: "查询1",
            value: 9,
          }
        ]
      ],
      rulePage: "",
      query: "",
      showMetricFlag:false,
      showResults:false,
      img: {
        url: process.env.VUE_APP_BASE_API,
        path:''
      },
      counter:0
    };
  },
  created() {
  },
  mounted() {
  },
  methods: {
    handlePageChange(val) {
      this.rulePage.curPage =  val;
    },
    showMetric(){
      this.showMetricFlag=true
    },
    handleQuery(){
      if(this.dataSource===''){
        this.$message.error('请选择数据集！');
        return;
      }
      if(this.queryType===''){
        this.$message.error('请选择查询请求！');
        return;
      }
      this.showQueryResults();
    },
    showQueryResults() {
      this.showResults = true;
      this.query = queries[this.queryType];
      this.rulePage = {
        curPage: 1,
        pageSize: 50,
        total: queries[this.queryType].row > 5000 ? 5000 : queries[this.queryType].row
      };
    }
  }
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
a:link {
       color: #0000cc;
       font-family: 宋体;
       text-decoration: underline;
}
</style>
