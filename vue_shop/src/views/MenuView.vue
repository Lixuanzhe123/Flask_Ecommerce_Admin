<template>
     <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>权限管理</el-breadcrumb-item>
        <el-breadcrumb-item>权限列表</el-breadcrumb-item>
    </el-breadcrumb>

     <el-card class="box-card">
         <el-row>
            <el-table :data="tabledata.menu_list" stripe style="width: 100%" class="table">
                <el-table-column prop="id" label="id"  width="50"/>
                <el-table-column prop="name" label="菜单名"   />
                 <el-table-column prop="path" label="路径"    />
                <el-table-column prop="level" label="等级"   >
                <template #default="scope">
                    <el-tag v-if="scope.row.level==1">1级菜单</el-tag>
                    <el-tag type="success" v-else>2级菜单</el-tag>
                </template>
                </el-table-column> 
            </el-table>
        </el-row>
     </el-card>
</template>


<script setup> 
    import { ArrowRight,Plus,Search } from '@element-plus/icons-vue'

    import {  reactive ,onMounted} from 'vue'
    import api from '../api/index.js'
   
    const tabledata = reactive({
        menu_list:[{
            id:1,
            name:'用户管理',
            level:1
        },
        {
            id:2,
            name:'权限管理',
            level:2
        }
    ],
        quryname:null
    })

    const getMenus=()=>{
        api.getMenusList().then(res=>{
            if(res&&res.data.code==200){
            console.log(res);
            tabledata.menu_list=res.data.data
            }
            else{
                ElMessage('服务器异常！请稍后再试！');
            }

            
        })
    }
    onMounted(()=>{
        getMenus()
    })
</script>

<style scoped> 
 .box-card{
    margin-top: 20px;
  }
 

</style>