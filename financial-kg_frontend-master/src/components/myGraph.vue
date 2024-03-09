<template>
  <div class="wrapper">
    <div :style="{ height: 'calc(100% - 15px)', width: '100%' }" :id="'graphContainer' + ind"></div>
    <div style="height:15px;line-height:15px;text-align:center" @click="choosePoint" v-if="picLabel">{{ picLabel }}
    </div>
  </div>
</template>

<script>
import G6 from "@antv/g6";
export default {
  name: "MyGarph",
  data() {
    return {
      canvasWidth: 0,
      canvasHeight: 0,
      graph: {},
      rec: []
    };
  },
  props: {
    graphData: {
      type: Object,
      default: {}
    },
    hulls: {
      type: Array,
      default: []
    },
    picLabel: {
      type: String,
      default: ''
    },
    height: {
      type: Number,
      default: 500
    },
    width: {
      type: Number,
      default: 1000
    },
    ind: {
      type: Number,
      default: 1
    },
    isChange: {
      type: Boolean,
      default: false,
    },
    isDestroy:{
      type:Boolean,
      default:false
    }
  },
  mounted() {
    this.initSize()
    this.setGraph()
  },
  beforeUpdate(){
    console.log(1)
  },
  watch: {
    isChange: {
      handler() {
        this.graph.data({
          nodes: this.graphData.nodes,
          edges: this.graphData.edges
          // .map(function (edge, i) {
          //   edge["id"] = "edge" + i;
          //   return Object.assign({}, edge);
          // }),
        });
        this.graph.render();
      },
      // deep:true
    },
    isDestroy:{
      handler() {
        this.graph.removeHulls();
      }
    }
  },
  methods: {
    clearHulls(){
      this.graph.createHull
    },
    initSize() {
      const self = this // 因为箭头函数会改变this指向，指向windows。所以先把this保存
      setTimeout(() => {
        // todo 浏览器窗口发生变化时
        window.onresize = function () {
          // todo 获取div parentContent 的宽度和高度
          this.canvasWidth = self.$refs.parentContent.clientWidth - 15
          this.canvasHeight = self.$refs.parentContent.clientHeight - 15
          // // todo 修改画布的大小
          // self.graph.changeSize(this.canvasWidth, this.canvasHeight)
          // // todo 将图移动到画布中心位置
          // self.graph.fitCenter()
        }
      }, 20)
    },
    choosePoint(arr) {
      //此处应该为图的点击事件
      this.$emit('choosePoint', arr)
    },
    setGraph() {
      this.graph = new G6.Graph({
        container: "graphContainer" + this.ind,
        width: this.canvasWidth,
        height: this.canvasHeight,
        modes: {
          default: ["drag-canvas", "zoom-canvas", "drag-node", "lasso-select",
            {
              type: 'click-select',
              trigger: 'ctrl',
            },
          ],
        },
        layout: {
          type: "force",
          preventOverlap: true,
          linkDistance: 100,
          nodeStrength: -50,
          edgeStrength: 0.8,
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
      this.graph.data({
        nodes: this.graphData.nodes,
        edges: this.graphData.edges
        // .map(function (edge, i) {
        //   edge["id"] = "edge" + i;
        //   return Object.assign({}, edge);
        // }),
      });
      this.graph.render();

      this.graph.on('nodeselectchange', (e) => {
        e.selectedItems.nodes && this.choosePoint(e.selectedItems.nodes)
      });


      let _this = this;
      // console.log(this.graph)
      this.graph.on("afterlayout", () => {
        // let rec = [];
        let tmp = null;
        // _this.graph.removeHulls();
        _this.rec = [];
        console.log(_this.hulls)
        for (let i of _this.hulls) {
          // console.log(this.graph, i)
          tmp = _this.graph.createHull(i);
          _this.rec.push(tmp);
        }

        _this.graph.on("afterupdateitem", (e) => {
          // console.log(_this.rec)
          for (let i of _this.rec) {
            i.updateData(i.members);
          }
        });

        // graph.on("afterupdateitem", (e) => {
        //   hull1.updateData(hull1.members);
        //   hull2.updateData(hull2.members);
        //   hull3.updateData(hull3.members);
        // });
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.wrapper {
  width: 100%;
  height: 100%;
}
</style>
