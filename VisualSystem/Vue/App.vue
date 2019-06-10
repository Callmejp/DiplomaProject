<template>
  <div id="app" class="container">
    <div class="jumbotron">
      <div class="container">
         <h1>DeepPoly</h1>
         <p>A visualization system for certifying deep neural networks.</p>
         <p><a class="btn btn-primary btn-lg" href="https://github.com/Callmejp/DiplomaProject" role="button">Learn more</a></p>
      </div>
    </div>
    <div class="row">
      <div class="col-md-4">
        <div class="panel panel-success">
          <div class="panel-heading">Using .tf/.pyt format</div>
          <div class="panel-body">
            <form>
              <div class="form-group">
                <label for="network-one">Input Network One</label>
                <input type="file" id="network-one" @change="getFile($event)">
                <p class="help-block">Upload the first network here.</p>
              </div>
              <div class="form-group">
                <label for="network-two">Input Network Two</label>
                <input type="file" id="network-two" @change="getFileTwo($event)">
                <p class="help-block">Upload the second network here.</p>
              </div>
              <button type="submit" class="btn btn-default" @click="start_dp($event)">Submit</button>
            </form>
          </div>
        </div>
      </div>
      <div class="col-md-8">
        <div class="panel panel-default">
          <div class="panel-heading">Chart One</div>
          <div class="panel-body">
            <div id="chart-one" :style="{width: '100%', height: '365px'}"></div>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-4">
        <div class="panel panel-info">
          <div class="panel panel-danger">
            <div class="panel-heading">Instructions for uploading results</div>
            <div class="panel-body">
              Because 'meta' models can't be handled uniformly. So you need to achieve the
              results by improved DeepPoly in advance and upload them here.
            </div>
          </div>
          <div class="panel-heading">Using .meta format</div>
          <div class="panel-body">
            <form>
              <div class="form-group">
                <label for="result-one">Input Result One</label>
                <input type="file" id="result-one" @change="getResult($event)">
                <p class="help-block">Upload the first network's result here.</p>
              </div>
              <div class="form-group">
                <label for="result-two">Input Result Two</label>
                <input type="file" id="result-two" @change="getResultTwo($event)">
                <p class="help-block">Upload the second network's result here.</p>
              </div>
              <button type="submit" class="btn btn-default" @click="start_draw($event)">Submit</button>
            </form>
          </div>
        </div>
      </div>
      <div class="col-md-8">
        <div class="panel panel-default">
          <div class="panel-heading">Chart Two</div>
          <div class="panel-body">
            <div id="chart-two" :style="{width: '100%', height: '365px'}"></div>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="panel panel-default">
        <div class="panel-heading">Chart Three</div>
        <div class="panel-body">
          <div id="chart-three" :style="{width: '100%', height: '400px'}"></div>
        </div>
      </div>
    </div>
    <footer>
      <div class="container text-center">
        <p>Copyright &copy;JinPeng</p>
        <p>You can contact me by <a href="mailto:1321715290@qq.com">Email</a>.</p>
        <p>Thanks for using!</p>
      </div>
    </footer>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  name: 'App',
  data () {
    return {
      file: '',
      file1: '',
      result: '',
      result1: '',
      timer: '',
      yAxis: '',
      arr: '',
      arr1: ''
    }
  },
  mounted () {
    // this.drawLine()
  },
  beforeDestroy () {
    clearInterval(this.timer)
  },
  methods: {
    drawFinalChart: function (flag) {
      let formData = new FormData()
      formData.append('flag', flag)

      Vue.axios.post('http://118.25.52.27:8000/deeppoly/twocharts/', formData).then((response) => {
        if (response.status === 200) {
          let result = response.data
          this.arr = result.rst1
          this.arr1 = result.rst2
          let myChart = this.$echarts.init(document.getElementById('chart-three'))
          let length = this.arr.length
          let generatedAxis = Array.from({length}).map((v, k) => k)
          // console.log(generatedAxis)
          myChart.setOption({
            title: {
              text: ''
            },
            tooltip: {
              trigger: 'axis',
              axisPointer: {
                type: 'cross',
                label: {
                  backgroundColor: '#6a7985'
                }
              }
            },
            legend: {
              data: ['Net_1', 'Net_2']
            },
            toolbox: {
              feature: {
                saveAsImage: {}
              }
            },
            grid: {
              left: '3%',
              right: '4%',
              bottom: '3%',
              containLabel: true
            },
            xAxis: [{
              type: 'category',
              boundaryGap: false,
              data: generatedAxis
            }],
            yAxis: [{
              type: 'value'
            }],
            series: [
              {
                name: 'Net_1',
                type: 'line',
                data: this.arr
              },
              {
                name: 'Net_2',
                type: 'line',
                data: this.arr1
              }
            ]
          })
          window.onresize = myChart.resize
        }
      })
    },
    changeAxis: function () {
      Vue.axios.get('http://118.25.52.27:8000/deeppoly/result/').then((response) => {
        if (response.status === 200) {
          let rst = response.data
          // save to the local variable
          this.arr = rst.list_1
          this.arr1 = rst.list_2
          // exclude the '-1's
          let tempArr = []
          for (let i = 0; i < this.arr.length; i++) {
            if (this.arr[i] >= 0) {
              tempArr.push(this.arr[i])
            }
          }
          this.yAxis = tempArr
          this.drawLine(0)
          // if the first result is compelete, we should start to draw the second one
          if (rst.end_1) {
            tempArr = []
            for (let i = 0; i < this.arr1.length; i++) {
              if (this.arr1[i] >= 0) {
                tempArr.push(this.arr1[i])
              }
            }
            this.yAxis = tempArr
            this.drawLine(1)
          }
          if (rst.end_1 && rst.end_2) {
            clearInterval(this.timer)
            this.drawFinalChart(0)
          }
        }
      }).catch((response) => {
        // ...
      })
    },
    drawLine: function (flag) {
      // let myChart = this.$echarts.init(document.getElementById('myChart'))
      // window.addEventListener('resize', this.chart.resize)
      // console.log(this.yAxis)
      var myChart = ''
      var chartTitle = ''
      if (flag === 0) {
        myChart = this.$echarts.init(document.getElementById('chart-one'))
        chartTitle = 'Network One'
      } else {
        myChart = this.$echarts.init(document.getElementById('chart-two'))
        chartTitle = 'Network Two'
      }
      let length = this.yAxis.length
      let generatedAxis = Array.from({length}).map((v, k) => k)
      // console.log(generatedAxis)
      myChart.setOption({
        title: {
          text: ''
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        legend: {
          data: [chartTitle]
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [{
          type: 'category',
          boundaryGap: false,
          data: generatedAxis
        }],
        yAxis: [{
          type: 'value'
        }],
        series: [{
          name: chartTitle,
          type: 'line',
          data: this.yAxis
        }]
      })
      window.onresize = myChart.resize
    },
    getFile: function (event) {
      this.file = event.target.files[0]
      console.log(this.file)
    },
    getFileTwo: function (event) {
      this.file1 = event.target.files[0]
      console.log(this.file1)
    },
    getResult: function (event) {
      this.result = event.target.files[0]
      console.log(this.result)
    },
    getResultTwo: function (event) {
      this.result1 = event.target.files[0]
      console.log(this.result1)
    },
    start_dp: function (event) {
      event.preventDefault()
      if (this.file === '' || this.file1 === '') {
        alert('Please upload two networks for analysis!')
        return
      }
      let formData = new FormData()
      formData.append('file', this.file)
      formData.append('file1', this.file1)
      let config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      Vue.axios.post('http://118.25.52.27:8000/deeppoly/query/', formData, config).then((response) => {
        if (response.status === 200) {
          console.log(response)
          if (response.data.wait === 1) {
            alert('Server is busy, please try later!')
            return
          }
          this.timer = setInterval(this.changeAxis, 5000)
        }
      })
    },
    start_draw: function (event) {
      event.preventDefault()
      if (this.result === '' || this.result1 === '') {
        alert('Please upload two results for analysis!')
        return
      }
      let formData = new FormData()
      formData.append('rst', this.result)
      formData.append('rst1', this.result1)
      let config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      Vue.axios.post('http://118.25.52.27:8000/deeppoly/analyze/', formData, config).then((response) => {
        if (response.status === 200) {
          console.log(response)
          let rst = response.data
          // save to the local variable
          console.log(rst.result_1)
          this.yAxis = rst.result_1
          this.drawLine(0)
          console.log(rst.result_2)
          this.yAxis = rst.result_2
          this.drawLine(1)
          this.drawFinalChart(1)
        }
      })
    }
  }
}
</script>

<style>
footer {
    background: grey;
    color: #eee;
    font-size: 11px;
    padding: 20px;
}
</style>
