<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>用户管理</el-breadcrumb-item>
        <el-breadcrumb-item>用户列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
        <el-button type="primary" icon="Plus"  @click="addCatedialogVisible=true">
            添加分类
        </el-button>
        <div class="table-container"> 
            <el-table
                :data="tableData.date"
                style="width: 100%; margin-bottom: 20px"
                row-key="id"
                border
                >
                    <el-table-column prop="id" label="ID" sortable />
                    <el-table-column prop="name" label="类别" sortable />
                    <el-table-column prop="level" label="等级" sortable >
                        <template #default="scope">
                            <el-tag v-if="scope.row.level==1" type="primary">1</el-tag>
                            <el-tag v-else-if="scope.row.level==2" type="success">2</el-tag>
                            <el-tag v-else-if="scope.row.level==3" type="warning">3</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" >
                        <template #default="scope">
                
                            <el-button type="primary" :icon="Edit" >编辑</el-button>
                            <el-button type="danger" :icon="Delete">删除</el-button>
                        </template>
                    </el-table-column>
                
            </el-table>
        </div>

    </el-card>

    <el-dialog
        v-model="addCatedialogVisible"
        title="添加分类"
        width="500"
        :before-close="handleClose"
    >
       <el-form ref="addCateRef" :model="addCateForm" :rules="addCateRule">
            <el-form-item label="分类名称" prop="name">
                <el-input v-model="addCateForm.name"></el-input>
            </el-form-item>
            <el-form-item label="父级" prop="pid">
                 <el-cascader
                    v-model="addcatevalue"
                    :options="addcateoptions"
                    :props="addCateprops"
                    @change="handleChange"
                     separator=' > '
                     clearable
                    />
            </el-form-item>
       </el-form>
        <template #footer>
        <div class="dialog-footer">
            <el-button @click=closeaddCate>取消</el-button>
            <el-button type="primary" @click="addCate">
            确定
            </el-button>
        </div>
        </template>
    </el-dialog>
    
</template>


<script setup>
    import { ArrowRight,Plus } from '@element-plus/icons-vue'
    import { Delete, Edit } from '@element-plus/icons-vue'
    import { ref,reactive,onMounted } from 'vue'
    import api from '../api/index.js'

    onMounted(()=>{
        getTableDate()
        getCateOptions()
    })

    //添加分类
    let addcatevalue=ref([])
    const addCateRef=ref(null)
    
    let addCateForm=reactive(
        {
            name:'',
            pid:0,
            level:''
        }
    )
    let addCateRule=reactive(
        {
            name: [
                { required: true, message: '请输入分类名称', trigger: 'blur' },
                { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
            ]
        }
    )
    let handleChange=(addcatevalue) => {
        if (addcatevalue!=null){
            console.log(addcatevalue);
            addCateForm.pid=addcatevalue[addcatevalue.length-1]
            addCateForm.level=addcatevalue.length+1
        }
        else{
            addCateForm.pid=0
            addCateForm.level=1
        }
        console.log(addCateForm);
    }

    const addCate=()=>{
        api.addCateList(addCateForm).then(res=>{
            if(res){
                console.log(res.data)
                if (res.data.code==200){
                    addCatedialogVisible.value=false
                    getTableDate()
                    getCateOptions()
                    ElMessage.success('添加成功')
                }
            }
            else{
                addCatedialogVisible.value=false
                ElMessage.error('添加失败')

            }
            
        })
        addCateRef.value.resetFields()
        addcatevalue.value=null

   }
    let addcateoptions=reactive(null)
    let addCateprops=reactive(
        {
            value: 'id',
            label: 'name',
            children: 'children',
            expandTrigger: 'hover',
            checkStrictly: true
           
        }
    )
    let addCatedialogVisible=ref(false)

    let tableData=reactive(
       {
        date:[]
       }
    )
    const getTableDate=()=>{
        api.getCatesList(3).then(res=>{
            console.log(res.data)
            tableData.date=res.data.data
        })
    }

    const getCateOptions=()=>{
        api.getCatesList(2).then(res=>{
            console.log(res.data)
            addcateoptions=res.data.data
        })
    }
    const closeaddCate=()=>{
        addCateRef.value.resetFields()
        addcatevalue.value=null
        addCatedialogVisible.value=false
    }

</script>


<style scoped>
 .box-card {
    margin-top: 20px;
 }
 .table-container {
    margin-top: 20px;
 }
</style>