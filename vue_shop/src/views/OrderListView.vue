<template>
  <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>订单管理</el-breadcrumb-item>
        <el-breadcrumb-item>订单列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
        <el-row>
           <el-col :span="8">
                <el-input
                    v-model="m"
                    style="max-width: 600px"
                    placeholder="查询用户"
                    class="select">
                    <template #append>
                        <el-button :icon="Search" @click="SearchHandle" type="primary"/>
                    </template>
                </el-input>
            </el-col>
        </el-row>
        <el-row>
            <el-table :data="orderTable.data">
                <el-table-column type="index" width="50" />
                <el-table-column label="订单用户" prop="user" width="150"></el-table-column>
                <el-table-column label="订单价格" prop="price" width="150"></el-table-column>
                <el-table-column label="订单数量" prop="number" width="150"></el-table-column>
                <el-table-column label="是否支付" prop="pay_status" width="150">
                        <template #default="scope">
                            <el-tag type="success" v-if="scope.row.pay_status===1">已支付</el-tag>
                            <el-tag type="danger" v-else>未支付</el-tag>
                        </template>
                </el-table-column>
                <el-table-column label="是否送达" prop="is_send" width="150">
                        <template #default="scope">
                            <el-tag type="success" v-if="scope.row.is_send===1">已送达</el-tag>
                            <el-tag type="danger" v-else>未送达</el-tag>
                        </template>
                </el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="danger" size="small" :icon="Promotion" @click="OponExpressDialog(scope.row)">查看物流</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-row>
    </el-card>
    <el-dialog title="物流信息" v-model="ExpressDialog">
          <el-timeline>
            <el-timeline-item
            v-for="(activity, index) in activities.data"
            :key="index"
            :timestamp="activity.update_time"
            >
            {{ activity.content }}
            </el-timeline-item>
         </el-timeline>
    </el-dialog>
</template>

<script setup>
    import { ArrowRight,Promotion } from '@element-plus/icons-vue'
    import { Search } from '@element-plus/icons-vue'
    import { ref,reactive } from 'vue'
    import api from '@/api/index.js'

    const orderTable=reactive({
        data:[]
    })
    const activities=reactive({
        data:[]
    })
    let ExpressDialog=ref(false)
    onMounted(()=>{
        getOrdersList()
      
    })
    const getOrdersList=()=>{
        api.getOrdersList().then(res=>{
            console.log(res.data)
            orderTable.data=res.data.data
        })
    }
    const OponExpressDialog=(row)=>{
        ExpressDialog.value=true
        api.getExpressList(row.id).then(res=>{
            console.log(res.data.data)
            activities.data=res.data.data
        }) 
    }

</script>

<style scoped>
    .box-card {
        margin-top: 20px;
    }
</style>