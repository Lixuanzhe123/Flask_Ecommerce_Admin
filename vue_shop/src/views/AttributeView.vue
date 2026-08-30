<template>
     <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>商品管理</el-breadcrumb-item>
        <el-breadcrumb-item>属性列表</el-breadcrumb-item>
    </el-breadcrumb>

     <el-card class="box-card">
         <el-alert title="只有分类最后一级才能添加属性！" type="warning" style="margin-top: 5px;" />
    
            <div>
                <span style="margin-right: 20px; margin-top: 10px;">选择分类</span>
                <el-cascader
                        v-model="attr_value"
                        :options="attr_options"
                        :props="attr_props"
                        @change="attr_handleChange"
                        separator=' > '
                        style="width: 300px;"
                        />
            </div>
    
            <div>
            <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
                    <el-tab-pane label="静态属性" name="static">
                        <el-button type="primary" icon="CirclePlus" @click="add_attrHandle" :disabled="add_flagTag===null">添加属性</el-button>
                        <el-table :data="attriDate.staticD">
                              <el-table-column type="expand">
                                    <template #default="scope">
                                        <el-tag type="primary" style="margin-left: 25px;">{{ scope.row.val }}</el-tag>
                                    </template>
                                </el-table-column>
                            <el-table-column type="index" />
                            <el-table-column label="属性名称" prop="name"/>
                            <el-table-column label="操作">
                                <template #default="scope">
                                    <el-button type="primary" icon="Edit" @click="">编辑</el-button>
                                    <el-button type="danger" icon="Delete" @click="">删除</el-button>
                                </template>
                            </el-table-column>
                            
                        </el-table>
                    </el-tab-pane>
                    <el-tab-pane label="动态属性" name="dynamic">
                        <el-button type="primary" icon="CirclePlus" @click="add_attrHandle" :disabled="add_flagTag===null">添加属性</el-button>
                        <el-table :data="attriDate.dymaticD" row-key="id">
                             <el-table-column type="expand" >
                                    <template #default="scope">
                                        <el-tag type="primary"
                                            style="margin-left: 20px; margin-right: 5px;" 
                                            v-for="(v,i) in scope.row.val" 
                                            closable
                                            @close="attri_cloHandle(scope.row,i)"
                                            >
                                                {{v}}
                                        </el-tag>
                                        <add_-tag-components @addTagEvent="getTagValue" :row="scope.row"/>

                                    </template>
                              </el-table-column>
                            <el-table-column type="index" />
                            <el-table-column label="属性名称" prop="name"/>
                            <el-table-column label="操作">
                                <template #default="scope">
                                    <el-button type="primary" icon="Edit" @click="">编辑</el-button>
                                    <el-button type="danger" icon="Delete" @click="">删除</el-button>
                                    </template>
                            </el-table-column>
                        </el-table>
                    </el-tab-pane>
            </el-tabs>
        </div>
     </el-card>

     <el-dialog
        v-model="add_dialogVisible"
        :title="add_flagTag"
        width="500"
        :before-close="add_handleClose"
    >
        <el-form  :model="addform" ref="addRef" :rules="addRules">
            <el-form-item prop="name">
                <el-input v-model="addform.name" placeholder="请输入属实名" ></el-input>
            </el-form-item>
            <el-form-item prop="val">
                <el-input v-model="addform.val" placeholder="请输入属实内容"></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
        <div class="dialog-footer">
            <el-button @click="add_handleClose">取消</el-button>
            <el-button type="primary" @click="add_attriHandle">
            确定
            </el-button>
        </div>
        </template>
  </el-dialog>
</template>



<script setup>
    import { ArrowRight,CirclePlus } from '@element-plus/icons-vue'
    import { ref, reactive,onMounted, nextTick } from 'vue'
    import api from '@/api/index.js'
    import { ElMessage, ElStep } from 'element-plus'
    import add_TagComponents from '@/components/add_TagComponents.vue'
    import Add_TagComponents from '@/components/add_TagComponents.vue'



    //添加对话框
    let addform=reactive({
        name:'',
        val:'',
    })

    let add_attrData=reactive({
            name:null,
            _type:null,
            val:null,
            cid:null
    })

    let addRef=ref(null)

    const addRules=reactive({
        name: [
            { required: true, message: '请输入属性名', trigger: 'blur' },
            { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
        ],
        val: [
            {min: 1, max: 25, message: '长度在 2 到 25 个字符', trigger: 'blur'}
        ],
    })

    const activeName = ref('static')
    let attriDate=reactive({
        staticD:[],
        dymaticD:[],
        CID:null
    })

    let add_dialogVisible=ref(false)

    let flag=reactive({
        static:false,
        dymatic:false
    })
    onMounted(()=>{
        getCateOptions()
    })
    let attr_value=ref([])

    let attr_options=ref([])

    let add_flagTag=ref(null)

    const attr_props=reactive({
        value:'id',
        label:'name',
        children:'children',
        expandTrigger: 'hover',

    })

    const attr_handleChange = (value) =>{
        
        if (value&&value.length==3){
            attriDate.CID=value[2]
            flag.static=true
            flag.dymatic=true
            add_attrData._type=activeName.value
            if(activeName.value=="static"){
                getAttr_staticDate()
                add_flagTag.value="添加静态属性"
               
            }else{
                getAttr_dymaticDate()
                add_flagTag.value="添加动态属性"
            }
        }
        else{
            attriDate.CID=null
            attriDate.staticD=""
            attriDate.dymaticD=""
            if (value && value.length !== 0) {
                 add_flagTag.value=null
                 ElMessage.warning('请选择最后一级分类！')
            }
        }
    }

    let handleClick = (tab, event) => {
     
        if(!attriDate.CID){
            ElMessage.warning('请选择分类！')
            return
        }
        add_attrData._type=tab.paneName
        if (tab.paneName=="static"&& !flag.static) return
        if (tab.paneName=="dynamic"&& !flag.dymatic) return

        
        if (tab.paneName=="static"){
            getAttr_staticDate()
            add_flagTag.value="添加静态属性"
        }
        else{
            getAttr_dymaticDate()
            add_flagTag.value="添加动态属性"
        }
    }

    const add_attrHandle=()=>{
        add_dialogVisible.value=true
    }

    const add_attriHandle=()=>{
        add_attrData.cid=attriDate.CID
        add_attrData.name=addform.name
        add_attrData.val=addform.val
      
        api.addAttriList(add_attrData).then(res=>{
            if(res){
                if(res.data.code==200){ 
                    ElMessage.success('添加成功')
                    if (add_attrData._type==="static"){
                            getAttr_staticDate()
                
                    }else{
                        getAttr_dynamicDate()
                    }
                }else{
                    ElMessage.error(res.data.msg)
                }
            }
            else{
                ElMessage.error('服务器错误，请重试')
            }
           add_handleClose()
        })
    }

    //关闭添加属性的对话框
    const add_handleClose=()=>{
        add_dialogVisible.value=false
        addRef.value.resetFields()
    }
    const getCateOptions=()=>{
        api.getCatesList(3).then(res=>{
            console.log(res.data)
            attr_options.value=res.data.data
        })
    }
    
    const getAttr_staticDate=()=>{
    
        if (!attriDate.CID) return
        api.getAttriList(attriDate.CID,"static").then(res=>{
            console.log(res.data)
            attriDate.staticD=res.data.data
            flag.static=false
        })
    }
    const getAttr_dymaticDate=()=>{
        if (!attriDate.CID) return
        console.log(attriDate.CID)
        api.getAttriList(attriDate.CID,"dynamic").then(res=>{
            console.log(res.data)
            attriDate.dymaticD=res.data.data
            attriDate.dymaticD.forEach(item=>{
                item.val=item.val?item.val.split(","):[]
            })
            flag.dymatic=false
        })
    }
    const getTagValue=(val)=>{
        if(val.inputValue==="") return
        val.row.val.push(val.inputValue)
        let params={
            "_type":add_attrData._type,
            "val":val.row.val.join(",")
        }
        api.editAttriList(val.row.id,params).then(res=>{ 
           if(res){
                
                if(res.data.code==200){
                    flag.dymatic=true
                    ElMessage({
                        message:"添加成功",
                        type:'success'
                    })
                }else{
                    ElMessage({
                        message:"添加失败",
                        type:'error'
                    })
                }
           }else{
            ElMessage({
                message:'服务器异常！请稍后再试！',
                type:'error'
            })
           }
        })
    }
    const attri_cloHandle=(row,i)=>{
        row.val.splice(i,1)
        let params={
            "val":row.val.join(",")
        }
        api.editAttriList(row.id,params).then(res=>{ 
           if(res){
                
                if(res.data.code==200){
                    flag.dymatic=true
                    ElMessage({
                        message:"删除成功",
                        type:'success'
                    })
                }else{
                    ElMessage({
                        message:"删除失败",
                        type:'error'
                    })
                }
           }
        })

    }
</script>


<style scoped>
    .box-card {
        margin-top: 20px;
    }
    .demo-tabs > .el-tabs__content {
        padding: 32px;
        color: #6b778c;
        font-size: 32px;
        font-weight: 600;
    }
</style>