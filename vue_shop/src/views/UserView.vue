<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>用户管理</el-breadcrumb-item>
        <el-breadcrumb-item>用户列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
        <el-row :gutter="12">
            <el-col :span="8">
                <el-input
                    v-model="Userdata.quryname"
                    style="max-width: 600px"
                    placeholder="查询用户"
                    class="select">

                    <template #append>
                        <el-button :icon="Search" @click="SearchHandle"/>
                    </template>
                </el-input>

            </el-col>
            <el-col :span="12">
                <el-button type="primary" :icon="Plus" @click="dialogFormVisible = true">添加用户</el-button>
            </el-col>
        </el-row>
        
        <el-row>
            <el-table :data="Userdata.tabledata" stripe style="width: 100%" class="table">
                <el-table-column prop="id" label="ID"  width="50"/>
                <el-table-column prop="username" label="账号"  width="100"  />
                <el-table-column prop="nick_name" label="昵称"  width="100" />
                <el-table-column prop="email" label="邮箱"  />
                <el-table-column prop="phone" label="手机号" />
                <el-table-column prop="role" label="角色" />
                <el-table-column label="操作" >
                    <template #default="scope">
                        <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
                        Edit
                        </el-button>
                        <el-button
                            size="small"
                            type="danger"
                            @click="handleDelete(scope.$index, scope.row)">
                            Delete
                        </el-button>
                        <el-button
                            size="small"
                            type="success"
                            @click="handleReset(scope.$index, scope.row)">
                            reset
                        </el-button>
                    </template>
                </el-table-column>
            
            </el-table>
        </el-row>

        <el-row>
            <el-pagination
                v-model:current-page="Userdata.pnum"
                v-model:page-size="Userdata.psize"
                :page-sizes="page_sizes"
                :disabled="disabled"
                :background="background"
                layout="total, sizes, prev, pager, next, jumper"
                :total="Userdata.total"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                class="table"
                />
        </el-row>
    </el-card>

    <!-- 添加用户 对话框 -->
     <el-dialog v-model="dialogFormVisible" title="添加用户" width="500" :before-close="addFormRest">
        <el-form :model="user_from" :rules="user_from_rules" ref="addFormRef">
            <el-form-item label="账号" :label-width="formLabelWidth" prop="name" >
                <el-input v-model="user_from.name" autocomplete="off" />
            </el-form-item>
             <el-form-item label="密码" :label-width="formLabelWidth" prop="password">
                <el-input v-model="user_from.password" autocomplete="off" />
            </el-form-item>
             <el-form-item label="重复密码" :label-width="formLabelWidth" prop="re_password">
                <el-input v-model="user_from.re_password" autocomplete="off" />
            </el-form-item>
             <el-form-item label="昵称" :label-width="formLabelWidth" prop="nick_name">
                <el-input v-model="user_from.nick_name" autocomplete="off" />
            </el-form-item>
             <el-form-item label="邮箱" :label-width="formLabelWidth" prop="email">
                <el-input v-model="user_from.email" autocomplete="off" />
            </el-form-item>
             <el-form-item label="手机号" :label-width="formLabelWidth" prop="phone">
                <el-input v-model="user_from.phone" autocomplete="off" />
            </el-form-item>
            <el-form-item label="角色" :label-width="formLabelWidth" prop="role_id">
                <el-select v-model="user_from.role_id" placeholder="请选择">
                    <el-option :label="r.name" :value="r.id" v-for="r in roles" />
                </el-select>
            </el-form-item>

        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="addFormRest">取消</el-button>
                <el-button type="primary" @click="addUser(addFormRef)">
                  确定
                </el-button>
            </div>
        </template>
    </el-dialog>

     <!-- 修改用户 对话框 -->
    <el-dialog v-model="dialogFormVisible_edit" title="修改用户" width="500" :before-close="editFormRest">
        <el-form :model="edit_from" :rules="edit_rules" ref="editFormRef">
            <el-form-item label="账号" :label-width="formLabelWidth" prop="name"  >
                <el-input v-model="edit_from.name" autocomplete="off" disabled />
            </el-form-item>
             <el-form-item label="昵称" :label-width="formLabelWidth" prop="nick_name">
                <el-input v-model="edit_from.nick_name" autocomplete="off" />
            </el-form-item>
             <el-form-item label="邮箱" :label-width="formLabelWidth" prop="email">
                <el-input v-model="edit_from.email" autocomplete="off" />
            </el-form-item>
             <el-form-item label="手机号" :label-width="formLabelWidth" prop="phone">
                <el-input v-model="edit_from.phone" autocomplete="off" />
            </el-form-item>
            <el-form-item label="角色" :label-width="formLabelWidth" prop="role_id">
                <el-select v-model="edit_from.role_id" placeholder="请选择">
                    <el-option :label="r.name" :value="r.id" v-for="r in roles" />
                </el-select>
            </el-form-item>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="editFormRest">取消</el-button>
                <el-button type="primary" @click="editUser(editFormRef)">
                  确定
                </el-button>
            </div>
        </template>
    </el-dialog>


    <!-- 删除提示框 -->
    <el-dialog v-model="DeleteFormVisible" title="修改用户" width="500" >
        <el-form :model="edit_from"  >
          <span>是否将用户名为{{delete_from.name}},昵称为{{ delete_from.nick_name }}的用户删除</span>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="DeleteFormVisible=false">取消</el-button>
                <el-button type="primary" @click="DeleteUser">
                  确定
                </el-button>
            </div>
        </template>
    </el-dialog>

    <!-- 重置密码 提示框 -->
     <el-dialog v-model="ResetFormVisible" title="重置密码" width="500" >
        <el-form :model="reset_from" :rules="reset_rules" ref="resetFormRef">
            <el-form-item label="新密码" :label-width="formLabelWidth" prop="password"  >
                <el-input v-model="reset_from.password" autocomplete="off"  />
            </el-form-item>
             <el-form-item label="确定密码" :label-width="formLabelWidth" prop="re_password">
                <el-input v-model="reset_from.re_password" autocomplete="off" />
            </el-form-item>
        </el-form>
      
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="ResetFormRest">取消</el-button>
                <el-button type="primary" @click="ResetPass">
                  确定
                </el-button>
            </div>
        </template>
    </el-dialog>


</template>


<script setup>
   
    import { ArrowRight,Plus,Search } from '@element-plus/icons-vue'
    import { ref,reactive,onMounted} from 'vue'
    import api from '@/api/index.js'

    

     // 页面加载时获取用户列表
    
    onMounted(()=>{
        getUsers()
        get_roles()
    })


    const validatePass2=(rule, value, callback)=>{
        if (value === '') {
            callback(new Error('请再次输入密码'))
        } else if (value !== user_from.password) {
            callback(new Error('两次输入密码不一致!'))
        } else {
            callback()
        }
    }

    const validatePass3=(rule, value, callback)=>{
        if (value === '') {
            callback(new Error('请再次输入密码'))
        } else if (value !== reset_from.password) {
            callback(new Error('两次输入密码不一致!'))
        } else {
            callback()
        }
    }

    const validateEmail=(rule,value,callback)=>{
        if (!value) {
            callback(new Error('请输入邮箱'))
        } else {
            const reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/
            if (reg.test(value)) {
                callback()
            } else {
                callback(new Error('请输入正确的邮箱'))
            }
        }

    }

    const validatePhone=(rule,value,callback)=>{
        if (!value) {
            callback(new Error('请输入手机号'))
        } else {
            const reg = /^1[3456789]\d{9}$/
            if (reg.test(value)) {
                callback()
            } else {
                callback(new Error('请输入正确的手机号'))
            }
        }
    }

    //添加用户表单验证
    const user_from_rules=reactive({
        name: [
            { required: true, message: '请输入用户名', trigger: 'blur' },
            { min: 3, max: 25, message: '长度在 3 到 25 个字符', trigger: 'blur' }
        ],
        nick_name: [
            { required: true, message: '请输入昵称', trigger: 'blur' },
            { min: 3, max: 25, message: '长度在 3 到 25 个字符', trigger: 'blur' }
        ],
        password: [
            { required: true, message: '请输入密码', trigger: 'blur' },
            { min: 3, max: 25, message: '长度在 3 到 25 个字符', trigger:'blur'}
        ],
        re_password:[
            {required: true, message: '请输入密码', trigger: 'blur'},
            {validator:validatePass2,trigger:'blur'}
        ],
        email:[
            {validator:validateEmail,trigger:'blur'}
        ],
        phone:[
            {validator:validatePhone,trigger:'blur'}
        ]
    })

    //存储获取用户数据
    const Userdata=reactive({
        tabledata:[],
        total:0,
        pnum:1,
        psize:2,
        quryname:""
    })
    // 添加用户的表单
    const user_from=reactive({
        name:'',
        password:'',
        re_password:'',
        email:'',
        phone:'',
        nick_name:'',
        role_id:null
    })

    // 分页
    const page_sizes=reactive([1, 2, 3, 4,5,10])
    const small = ref(false)
    const background = ref(false)
    const disabled = ref(false)

    // 添加用户对话框
    const dialogFormVisible = ref(false)
    const formLabelWidth = '80px'

    //删除
    const DeleteFormVisible=ref(false)

    //修改密码
    const ResetFormVisible=ref(false)
    const resetFormRef=ref(null)

    //获得权限信息
    let roles=ref([])

    const get_roles=()=>{
        api.getRolesList().then(res=>{
        if (res ||res.data.code==200){
            roles=res.data.data;
            console.log(res);
        }
        else{
            ElMessage("服务器异常！请稍后再试！")
        }
        })
    }

    
    const reset_from=reactive({
        password:'',
        re_password:'',
        id:''
    })

    const reset_rules=reactive({
        password: [
            { required: true, message: '请输入密码', trigger: 'blur' },
            { min: 3, max: 25, message: '长度在 3 到 25 个字符', trigger:'blur'}
        ],
        re_password:[
            {required: true, message: '请输入密码', trigger: 'blur'},
            {validator:validatePass3,trigger:'blur'}
        ]
    })

    // 获取用户列表
    const getUsers=()=>{
        let params={
            pnum:Userdata.pnum,
            psize:Userdata.psize,
            name:Userdata.quryname
        }
        api.getUsers({params}).then(res=>{
            if (res==null || res.data.code!=200  ){
                return
            }
            else{
            Userdata.tabledata=res.data.data.data;
            Userdata.total=res.data.data.total;
            console.log(res.data);
            }
        })
    }
   
    // 分页   
    const handleSizeChange = (val) => {
        //每页显示多少条
        console.log(`每页 ${val} 条`);
        Userdata.psize=val
        Userdata.pnum=1
        getUsers()
    }

    // 分页
    const handleCurrentChange = (val) => {

        // 当前页码
        console.log(`当前页: ${val}`);
        Userdata.pnum=val
        getUsers()
    }

    // 查询
    const SearchHandle=()=>{
        Userdata.pnum=1
        let params={
            name:Userdata.quryname,
            pnum:Userdata.pnum,
            psize:Userdata.psize
        }
        api.getUsers({params}).then(res=>{
            if (res==null | res.data.code!=200  ){
                return
            }
            else{
            Userdata.tabledata=res.data.data.data;
            Userdata.total=res.data.data.total;

            console.log(res.data);
            }
        })
    }

    const addFormRef=ref(null)

    const addFormRest=()=>{
        //重置表单
        addFormRef.value.resetFields()
        //关闭对话
        dialogFormVisible.value=false
    }

    const addUser=(FormRef)=>{
        FormRef.validate(vail =>{
           if(vail){
                console.log('submit!')
                api.addUser(user_from).then(res=>{
                    if (res){
                        if (res.data.code==200){
                        ElMessage({
                                        message:res.data.msg,
                                        type: 'success',
                                    });
                        console.log(res);
                        // 刷新数据
                        getUsers()

                        // 关闭对话框
                        addFormRest()

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
            ElMessage('验证未通过！请检查输入！');
            console.log('error submit!!')
            return false
        }
        })

    }

    //编辑用户

    const editFormRef=ref(null)
    const edit_from=reactive({
        id:'',
        name:'',
        nick_name:'',
        email:'',
        phone:'',
        role_id:null
    })


    //删除用户
    const delete_from=reactive({
        id:'',
        name:'',
        nick_name:''
    })
    const dialogFormVisible_edit=ref(false)
    const editFormRest=()=>{
        //重置表单
        editFormRef.value.resetFields()
        //关闭对话
        dialogFormVisible_edit.value=false
    }

    const edit_rules=reactive({
        name:[
            { required: true, message: '请输入用户名', trigger: 'blur' },
            { min: 3, max: 25, message: '长度在 3 到 25 个字符', trigger: 'blur' }
        ],
        nick_name:[
            { required: true, message: '请输入昵称', trigger: 'blur' },
            { min: 2, max: 25, message: '长度在 3 到 25 个字符', trigger: 'blur'}
        ],
        email:[
            {validator:validateEmail,trigger:'blur'}
        ],
        phone:[
            {validator:validatePhone,trigger:'blur'}
        ]
    })
    const handleEdit=(index,row)=>{
        dialogFormVisible_edit.value = true
        api.getUser(row.id).then(res=>{
            if(res){
                if(res.data.code==200){
                    edit_from.id=res.data.data.id
                    edit_from.name=res.data.data.username
                    edit_from.nick_name=res.data.data.nick_name
                    edit_from.email=res.data.data.email
                    edit_from.phone=res.data.data.phone
                    edit_from.role_id=res.data.data.role_id
                    
                }
                else{
                    ElMessage(res.data.msg)
                }
            }
            else{
                ElMessage('获取用户信息失败')
            }
            
        })
        // console.log(index,row)
        // edit_from.id=row.id
        // edit_from.name=row.username
        // edit_from.nick_name=row.nick_name
        // edit_from.email=row.email
        // edit_from.phone=row.phone
        // dialogFormVisible_edit.value=true
    }

    const editUser=(FormRef)=>{
        FormRef.validate(vail=>{
               if(vail){
                console.log('submit!')
                api.EditUser(edit_from.id,edit_from).then(res=>{
                    if (res){
                        if (res.data.code==200){
                        ElMessage({
                                        message:res.data.msg,
                                        type: 'success',
                                    });
                        console.log(res);
                        // 刷新数据
                        getUsers()

                        // 关闭对话框
                        editFormRest()
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
                ElMessage('验证未通过！请检查输入！');
                console.log('error submit!!')
                return false
            }
        })
    }

    const handleDelete=(index,row)=>{
        DeleteFormVisible.value=true;
        delete_from.id=row.id;
        delete_from.name=row.username;
        delete_from.nick_name=row.nick_name;
       
    }
    const DeleteUser=()=>{
        api.deleteUser(delete_from.id).then(res=>{
            if (res){
                        if (res.data.code==200){
                        ElMessage({
                                        message:res.data.msg,
                                        type: 'success',
                                    });
                        console.log(res);
                        // 刷新数据
                        getUsers()
                        // 关闭对话框
                        DeleteFormVisible.value=false;
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

    //修改密码事件
    const handleReset=(index,row)=>{
        ResetFormVisible.value=true;
        reset_from.id=row.id;
    }

    const ResetFormRest=()=>{
        //重置表单
        resetFormRef.value.resetFields()
        //关闭对话
        ResetFormVisible.value=false
    }

    const ResetPass=()=>{
        let params={
            password:reset_from.password
        }
        api.resetPass(reset_from.id,params).then(res=>{
            if (res){
                    if (res.data.code==200){
                    ElMessage({
                                    message:res.data.msg,
                                    type: 'success',
                                });
                    console.log(res);
                    // 刷新数据
                    getUsers()
                    // 关闭对话框
                    ResetFormRest()
                    }
                    else{
                        ElMessage({
                                    message:res.data.msg,
                                    type: 'warning',
                                    })
                    }
        }
            else{
                ElMessage('服务器异常！请稍后再试！');
            }
        })
    }
</script>


<style scoped>
 .box-card{
    margin-top: 20px;
 }

 .table{
    margin-top: 20px;
 }

</style>