<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>商品管理</el-breadcrumb-item>
        <el-breadcrumb-item>属性列表</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card class="box-card">
        <el-row>
            <el-col :span="8">
                <el-input v-model="Productable.searchkey" placeholder="请输入要搜索的商品"  clearable @clear="get_proList">
                    <template #append>
                        <el-button :icon="Search" @click="get_proList"/>
                    </template>
                </el-input>
            </el-col>
            <el-col :span="4">
                <el-button type="primary" @click="addProHandle">添加商品</el-button>
            </el-col>
        </el-row>
        <el-row>
            <el-table :data="Productable.data">
                <el-table-column type="index" width="50"></el-table-column>
                <el-table-column label="商品名称" prop="name" show-overflow-tooltip></el-table-column>
                <el-table-column label="商品价格" prop="price" width="150"></el-table-column>
                <el-table-column label="商品数量" prop="number" width="150"></el-table-column>
                <el-table-column label="商品状态" prop="state" width="150"></el-table-column>
                <el-table-column label="操作">
                <template #default="scope">
                    <el-button type="primary" size="small">编辑</el-button>
                    <el-button type="danger" size="small" @click="delete_pro(scope.row)">删除</el-button>
                </template>
                </el-table-column>
            </el-table>
        </el-row>
    </el-card>
</template>

<script setup>
     import { ArrowRight,CirclePlus } from '@element-plus/icons-vue'
     import { Search } from '@element-plus/icons-vue'
     import { reactive,onMounted} from 'vue';
     import api from '@/api/index';
     import router from '@/router';



     onMounted(()=>{
        get_proList()
     })

     let Productable=reactive({
        data:null,
        searchkey:''
     })

     const get_proList=()=>{
        api.getProList(Productable.searchkey).then(res=>{
            if(res){
                if(res.data.status==200){
                    Productable.data=res.data.data
                }
                else{
                    ElMessage.error(res.data.msg)
                }
            }
            else{
                ElMessage.error("服务器异常")
            }
        })
        
     }
     
     const delete_pro=(row)=>{
         ElMessageBox.confirm(
            '是否要删除'+row.name+"?",
            '警告',
            {
            confirmButtonText: '确定',
            cancelButtonText: '否定',
            type: 'warning',
            }
        ) .then(() => {
            api.deleteProList(row.id).then(res=>{
                if(res){
                    console.log(res.data)
                    if(res.data.status==200){
                         ElMessage({
                            type: 'success',
                            message: '成功删除',
                        })
                        get_proList()
                    }else{
                         ElMessage({
                            type: 'warn',
                            message: res.data.msg,
                        })
                    }
                }else{
                    ElMessage({
                            type: 'warn',
                            message: "服务丢失,请稍后再试",
                        })
                }

            })
            })
            .catch(() => {
                ElMessage({
                    type: 'info',
                    message: '删除取消',
                })
            })
     }
     const addProHandle=()=>{
        router.push('/addPro')
     }
</script>

<style scoped>
 .box-card{
     margin-top: 20px;
 }
</style>