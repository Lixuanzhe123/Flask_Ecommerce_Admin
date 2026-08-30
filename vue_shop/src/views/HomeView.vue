<template>
<div class="common-layout container">
    <el-container class="container">
      <el-header class="Header">
        <div class="logo">
             <img src="../assets/Login_log.png" alt="logo" >
             <span>电商后台管理系统</span>
        </div>
        <div class="user">
             <el-button type="primary" @click="Logouy">退出</el-button>
              <!-- <el-button type="primary" @click="test_">测试</el-button> -->
        </div>
      </el-header>
      <el-container>
        <el-aside  class="Aside">
          <el-menu active-text-color="#ffd04b" 
                   background-color="#001529" 
                   class="el-menu-vertical-demo"
                   default-active="2"
                   text-color="#fff"
                   :unique-opened="true"
                   router>
                <el-sub-menu :index="index+''"  v-for="(item,index) in menus.menuList" >
                  <template #title>
                    <el-icon>
                      <component :is="menus.iconlist[index+1]"></component>
                    </el-icon>
                    <span>{{ item.name }}</span>
                  </template>
                 
                    <el-menu-item :index="childItem.path" v-for="childItem in item.children">
                       {{ childItem.name }}
                    </el-menu-item>
                </el-sub-menu>
          </el-menu>
        </el-aside>
        <el-main class="Main">
          <router-view/>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
  import {ref,reactive,onMounted} from 'vue'
  import {useRouter} from 'vue-router'
  import api from '../api/index.js'


  onMounted(()=>{
   get_menu()
  })
  const router = useRouter()

  const menus=reactive({
    menuList:[],
    iconlist:{
      '1':'User',
      '2':'Tools',
      '3':'Goods',
      '4':'Shop',
      '5':'PieChart'
    }
  })
  const Logouy = () => {
    sessionStorage.removeItem('token')
    router.push('/login')
  }

//   const test_ = () => {
//     api.getTest().then(res=>{
//       console.log(res);
//     })
//   }
  const get_menu=()=>{ 
  api.getMenus().then(res=>{
        if (res){
          if (res.data.code==200){
            console.log(res.data.data);
            menus.menuList=res.data.data
          }
          else{
            
            console.log(res.data.msg);
          }
        }
        else{
          ElMessage('服务器异常！请稍后再试！');
        }
      })
}
  
</script>


<style scoped>
   .Header{
    background-color: #2588df75;
    height: 50px;
    width: 100%;
    box-shadow: 0 0 5px rgba(0,0,0,.3);
    font-size: 20px;
    
   }
   .logo{
    float: left;
    height: 50px;

    display: flex;
    align-items: center;  
    justify-content: center; 
   }
    .logo img{
        height: 50px;
        width: 50px;
        margin-right: 10px;
    }
    .user{
        float: right;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .Aside{
        width: 200px;
        background-color: #001529;
      }
    .Main{
        /* background-color: #2588df75; */
        height: 100%;
    }
    .container{
        height: 100%;
    }
</style>
