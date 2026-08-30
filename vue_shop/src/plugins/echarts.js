import * as echarts from 'echarts'

export default {
    //echarts作为全局变量使用
    install:app=>{
        //配置全局变量，element代表将图表渲染到那个元素上
        app.config.globalProperties.$echarts=(element,option)=>{
            let myChart=echarts.init(document.getElementById(element))
            //建立图表需要显示数据
            myChart.setOption(option)
            return myChart
        }
    }
}