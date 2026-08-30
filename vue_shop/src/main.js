import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import elementIcon from "@/plugins/icons.js"
import echarts  from './plugins/echarts'


const debounce = (fn, delay) => {
  let timer
  return (...args) => {
    if (timer) {
      clearTimeout(timer)
    }
    timer = setTimeout(() => {
      fn(...args)
    }, delay)
  }
}

const _ResizeObserver = window.ResizeObserver
window.ResizeObserver = class ResizeObserver extends _ResizeObserver {
  constructor(callback) {
    callback = debounce(callback, 16) // 防抖处理，避免频繁触发
    super(callback)
  }
}

createApp(App).use(router).use(elementIcon).use(echarts).mount('#app')
