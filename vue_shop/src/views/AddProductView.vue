<template>
     <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>商品管理</el-breadcrumb-item>
        <el-breadcrumb-item>属性列表</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card class="box-card">
        <el-alert title="下面输入要《添加商品》的信息" type="info" center show-icon />
        <el-steps
            :space="200"
            :active="active"
            finish-status="success"
            align-center
        >
            <el-step title="基本信息" />
            <el-step title="商品静态属性" />
            <el-step title="商品动态属性" />
            <el-step title="商品图片" />
            <el-step title="商品内容" />
            <el-step title="完成" />
        </el-steps>
        <el-tabs tab-position="left" class="el-tabs" v-model="active" :before-leave="beforeLeave">
            <el-tab-pane label="基本信息" :name="0">
                <el-form :model="addForm" ref="addRef" :rules="addRules">
                    <el-form-item prop="name" label="商品名称">
                        <el-input v-model="addForm.name" ></el-input>
                    </el-form-item>
                    <el-form-item prop="price" label="商品价格">
                        <el-input v-model="addForm.price"></el-input>
                    </el-form-item>
                    <el-form-item prop="number" label="商品库存">
                        <el-input v-model="addForm.number"></el-input>
                    </el-form-item>
                    <el-form-item prop="weight" label="商品权重">
                        <el-input v-model="addForm.weight"></el-input>
                    </el-form-item>
                    <el-form-item label="商品分类">
                        <el-cascader
                        v-model="attri_value"
                        :options="attri_options"
                        :props="attri_props"
                        @change="attri_handleChange"
                        separator=' > '
                        clearable
                        style="width: 400px;"
                        />
                    </el-form-item>
                </el-form>
            </el-tab-pane>
            <el-tab-pane label="商品静态属性" :name="1">
                <el-form-item  :label="s.name" v-for="s in attriDate.static" :key="s.id">
                        <el-input v-model="s.val"></el-input>
                </el-form-item>
            </el-tab-pane>
            <el-tab-pane label="商品动态属性":name="2">
                <el-form-item  :label="d.name" v-for="d in attriDate.dynamic" :key="d.id">
                        <el-checkbox-group v-model="d.val">
                            <el-checkbox v-for="(v,i) in d.val" :key="i" :label="v" name="type" border/>
                        </el-checkbox-group>
                </el-form-item>
            </el-tab-pane>
            <el-tab-pane label="商品图片" :name="3">
                    <el-upload
                        v-model:file-list="fileList"
                        class="upload-demo"
                        :action="base.BaseUrl+base.upload_img_url"
                        list-type="picture"
                        :on-success="upImghandleSuccess"
                        :on-remove="upImghandleRemove"
                        :on-preview="upImghandlePreview"
                    >
                     <el-button type="primary">上传图片</el-button>
                    </el-upload>
            </el-tab-pane>
            <el-tab-pane label="商品内容" :name="4">
                <EditorComponent @onDataEvent="handleDataEvent" />
                 <el-button type="primary" @click="addProduct">添加商品</el-button>
            </el-tab-pane>
        </el-tabs>
        <el-dialog
            v-model="Pre_Visible"
            width="500"
            title="图片预览"
            append-to-body
            >
            <img :src="Pre_Img" class='pre-img'>
        </el-dialog>
    </el-card>
</template>

<script setup>
    import { ArrowRight } from '@element-plus/icons-vue';
    import { ElMessage } from 'element-plus';
    import api from "@/api/index"
    import {ref,reactive,onMounted} from 'vue'
    import base from "@/api/base"
    import EditorComponent from "@/components/EditorComponent.vue"
    import router from '@/router';

    //定义预览的可见性
    let Pre_Visible=ref(false)
    //定义预览的图片
    let Pre_Img=ref('')

    const active = ref(0)
    onMounted(()=>{
        getAttriList()
    })
    //添加的配置
    let addForm=reactive({
        name:'',
        price:'',
        number:'',
        weight:'',
        cid_one:'',
        cid_two:'',
        cid_three:'',
        pics:[],
        introduct:'',
        attr_static:[],
        attr_dynamic:[]
    })

    //添加表的名字
    let addRef=ref(null)

    const addRules=reactive({
        name:[
            {required:true,message:'请输入商品名称',trigger:'blur'},
            {min:3,max:510,message:'商品名称长度必须在2到510之间',trigger:'blur'}
        ],
        price:[
            {required:true,message:'请输入商品价格',trigger:'blur'},
            {type:'number',message:'请输入数字',trigger:'blur',transform:(val)=>Number(val)}
        ],
        number:[
            {required:true,message:'请输入商品库存',trigger:'blur'},
            {type:'number',message:'请输入数字',trigger:'blur',transform:(val)=>Number(val)}
        ],
        weight:[
            {required:true,message:'请输入商品权重',trigger:'blur'},
            {type:'number',message:'请输入数字',trigger:'blur',transform:(val)=>Number(val)}
        ]
    })

    //attri属性
    let attri_value=ref([])
    let attri_options=ref([])
    let attri_props=reactive({
        value:'id',
        label:'name',
        children:'children',
        expandTrigger: 'hover',
    })
    //定义获得属性
    let attriDate=reactive({
        static:[],
        dynamic:[]
    })

    //定义上传文件的列表
    let fileList=ref([])

    //attri属性改变时的回调函数
    let attri_handleChange=(val)=>{
       if(val){
          if(val.length==3){
            addForm.cid_one=val[0]
            addForm.cid_two=val[1]
            addForm.cid_three=val[2]
          }
       }
       console.log(addForm)
    }
    const getAttriList=()=>{
        api.getCatesList(3).then(res=>{
            if(res.data.code==200){
                attri_options.value=res.data.data
                
            }
        })
    }

    const beforeLeave=(tab,done)=>{
       if(attri_value.value){
           if(attri_value.value.length==3){
                getAttri(attri_value.value[2],"static")
                getAttri(attri_value.value[2],"dynamic")
                return true
           }
           ElMessage.error('请选择商品最后一级分类！')
           return false
       }
       ElMessage.error('请选择商品分类！')
       return false
    }
    const getAttri=(c_id,c_type)=>{
        if(c_type=="static"){
            api.getAttriList(c_id,c_type).then(res=>{
                console.log(res)
                if(res.data.code==200){
                    attriDate.static=res.data.data
                }
            })
        }else if(c_type=="dynamic"){
            api.getAttriList(c_id,c_type).then(res=>{
                if(res.data.code==200){
                    attriDate.dynamic=res.data.data
                    attriDate.dynamic.forEach(item=>{
                        item.val=item.val?item.val.split(','):[]
                    })
                }
            })
        }

    }
    //上传图片成功时的回调函数
   const upImghandleSuccess=(response,uploadfile,uploadFiles)=>{
    console.log(response)
    if(response.code==200){
        addForm.pics.push(response.data.path)
        ElMessage.success('上传成功！')
    }
    else{
        ElMessage.error('上传失败！')
    }
   }
   //删除图片前的回调函数
   const upImghandleRemove=(file,uploadFiles)=>{
       let romvepath=file.response.data.path
       let index=addForm.pics.indexOf(romvepath)
       addForm.pics.splice(index,1)
       ElMessage.success('删除成功！')
   }
   //预览图片前的回调函数
   const upImghandlePreview=(file)=>{
       console.log(file)
       Pre_Visible.value=true
       Pre_Img.value=file.response.data.url
   }

   //商品内容改变时的回调函数
   const handleDataEvent=(val)=>{
        addForm.introduct=val
   }
   //添加商品
   const addProduct=()=>{
      addForm.attr_static=attriDate.static
      addForm.attr_dynamic=attriDate.dynamic
      console.log(addForm)
      api.addProList(addForm).then(res=>{
        if(res.data.status==200){
            ElMessage.success('添加成功！')
            router.push('/product_list')
        }
        else{
            ElMessage.error('添加失败！')
        }
      })
   }
</script>

<style scoped>
    .box-card{
        margin-top: 20px;
    }
    .el-tabs{
         margin-top: 20px;
    }
    .pre-img{
        width: 100%;
        height: 100%;
    }

</style>