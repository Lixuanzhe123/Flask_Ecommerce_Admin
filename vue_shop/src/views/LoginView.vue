<template>
<!-- http -->
 <!-- <h1>登录页面</h1> -->
  <div class="main">
    <div class="Login">
        <div class="logo">
            <img src="../assets/Login_log.png" alt="Login_logo">
        </div>

        <el-form  :model="user"  class="user_login" :rules="user_rules" ref="User_form">
            <el-form-item prop="username">
                <el-input v-model="user.username" placeholder="用户名"  :prefix-icon="User"></el-input>
            </el-form-item>
            <el-form-item prop="pwd">
                <el-input v-model="user.pwd" placeholder="密码"  :prefix-icon="Lock" type="password"></el-input>
            </el-form-item>
            <el-form-item class="btns">
                <el-button type="primary" @click="onSubmit(User_form)">登录</el-button>
                <el-button>注册</el-button>
            </el-form-item>
        </el-form>
    </div>
  </div>

</template>


<script setup>
// 引入icon
import {User,Lock} from '@element-plus/icons-vue'
import { reactive,ref } from 'vue'
// import { ElMessage } from 'element-plus'
import router from '@/router'

import api from "../api/index"

const user=reactive({
    username:'',
    pwd:''
})

const User_form=ref(null)

const user_rules=reactive({
    username:[
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
    ],
    pwd:[
        { required: true, message: '请输入密码', trigger: 'blur' },
    ]
})



const onSubmit=(FormRf)=>{
     FormRf.validate((vail)=>{
        if(vail){
            console.log('submit!')
            api.getLogin(user).then(res=>{
                if (res){
                    if (res.data.code==200){
                     ElMessage({
                                    message:res.data.msg,
                                    type: 'success',
                                });
                     console.log(res);
                     sessionStorage.setItem('token',res.data.data.token)
                      router.push('/')
                    }
                    else{
                        ElMessage({
                                    message:res.data.msg,
                                    type: 'warning',
                                });
                        console.log(res.data.msg);
                    }
                }
                else{
                    ElMessage('服务器异常！请稍后再试！');
                }
            })
        }
        else{
            ElMessage('请填写用户名和密码！');
            console.log('error submit!!')
            return false
        }
     })
   }
  
</script>


<!-- scoped是样式作用域 -->

<style scoped>
    .main{
        width:100%;
        height:100%;
        background-color: rgb(0, 166, 255);
        display: flex;
        justify-content: center;
        align-items: center;
        
    }
    .Login{
        width: 500px;
        height: 350px;
        background-color: rgb(249, 248, 243);
        border-radius: 10px;
    }
    .logo{
        width: 300px;
        /* height: 200px; */
        margin: 0 auto;
        /* border: 1px solid #ebebeb; */
        border-radius: 5px;
        margin-top: -160px;
        
    }
    img{
        width: 100%;
        height: 100%;
        
    }
    .user_login{
        padding: 50px;
    }
    .btns{
        display: flex;
        justify-content: space-between;
    }
    .btns button{
       flex: 1;
    }
</style>