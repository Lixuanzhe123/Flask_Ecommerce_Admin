<template>
  <Editor v-model="textContent" :init="init"></Editor>
</template>

<script setup>
import tinymce from 'tinymce/tinymce'
//tinymce默认hidden，不引入不显示
import Editor from '@tinymce/tinymce-vue'
import 'tinymce/themes/silver/theme' // 主题文件
import 'tinymce/icons/default'
import 'tinymce/models/dom' // Bug修复
// tinymce插件可按自己的需要进行导入
// 更多插件参考：https://www.tiny.cloud/docs/plugins/
import 'tinymce/plugins/image' // 插入上传图片插件
import "tinymce/plugins/importcss"; //图片工具
import 'tinymce/plugins/media' // 插入视频插件
import 'tinymce/plugins/table' // 插入表格插件
import 'tinymce/plugins/lists' // 列表插件
import "tinymce/plugins/charmap"; // 特殊字符
import 'tinymce/plugins/wordcount' // 字数统计插件
import "tinymce/plugins/codesample"; // 插入代码
import "tinymce/plugins/code"; // 查看源码
import "tinymce/plugins/fullscreen"; //全屏
import 'tinymce/plugins/link' //
import 'tinymce/plugins/preview' // 预览
import "tinymce/plugins/template"; //插入模板
import 'tinymce/plugins/save' // 保存
import "tinymce/plugins/searchreplace"; //查询替换
import "tinymce/plugins/pagebreak"; //分页
import "tinymce/plugins/insertdatetime"; //时间插入

import { reactive, ref, watch, onMounted } from "vue"
const emit = defineEmits(["onDataEvent"])

const props = defineProps({
  value: {
    type: String,
    default: ''
   },
  plugins: {
    type: [String, Array],
    default: 'lists image media table wordcount save preview'
   },
  toolbar: {
    type: [String, Array],
    default: 'undo redo | formatselect | bold italic underline strikethrough forecolor backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent blockquote | lists image media table | codesample code removeformat save preview'
    // default: 'formats undo redo paste print fontsizeselect fontselect template fullpage|wordcount ltr rtl visualchars visualblocks toc spellchecker searchreplace|save preview pagebreak nonbreaking|media image|outdent indent aligncenter alignleft alignright alignjustify lineheight underline quicklink h2 h3 blockquote numlist bullist table removeformat forecolor backcolor bold italic strikethrough hr charmap link insertdatetime|subscript superscript cut codesample code |anchor preview fullscreen|help'
   }
})

const init = reactive({
  width: 720,
  height: 300,
  language_url: '/tinymce/langs/zh_CN.js',
  language: 'zh_CN',
  // 皮肤：这里引入的是public下的资源文件
  skin_url: '/tinymce/skins/ui/oxide',
  // skin_url: 'tinymce/skins/ui/oxide￾dark',//黑色系
  plugins: props.plugins,
  toolbar: props.toolbar,
  content_css: '/tinymce/skins/content/default/content.css',
  branding: false,
  // 隐藏菜单栏
  menubar: false,
  // 是否显示底部状态栏
  statusbar: true,
  // convert_urls: false,
  // 初始化完成
  init_instance_callback: (editor) => {
    console.log("初始化完成：", editor)
   },
  // 此处为图片上传处理函数，这个直接用了base64的 图片形式上传图片，
  // 如需ajax上传可参考 https://www.tiny.cloud/docs/configure/file-image-upload/#images_upload_handler
  images_upload_handler: (blobInfo, success, failure) => {
    const img = 'data:image/jpeg;base64,' + blobInfo.base64()
    console.log("图片上传处理：", img)
    success(img)
   }
})
const textContent = ref("")

watch(props.value, (newValue, oldValue) => {
  textContent.value = newValue
})
watch(textContent, (newValue, oldValue) => {
  emit("onDataEvent", newValue)
})
onMounted(() => {
  // 初始化 tinymce
  tinymce.init({})
})
</script>
