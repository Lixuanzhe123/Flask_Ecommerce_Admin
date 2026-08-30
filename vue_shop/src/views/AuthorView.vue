<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>用户管理</el-breadcrumb-item>
        <el-breadcrumb-item>用户列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card" >
        <el-row>
              <el-button type="primary" :icon="CirclePlus" @click="addAuthorVisible=true">增加角色</el-button>
        </el-row>
         <el-row>
            <el-table :data="dataable.tabledate" stripe style="width: 100%" class="table">
                <el-table-column type="expand">
                    <template #default="scope">
                        <el-row v-for="(m,i) in scope.row.menus" :key="m.id" :class="['margin-left50 bottom',i===0?'top':'']">
                            <el-col :span="2" class="margin-t5" ><el-tag closable @close="delete_role_menu(scope,m.id)">{{ m.name }}</el-tag></el-col>
                            <el-col :span="1"><el-icon class="margin-t15 margin-l15" ><CaretRight /></el-icon></el-col>
                            <el-col :span="21" class=margin-t5 ><el-tag  v-for="cm in m.children" :key="cm.id" type="success" closable class="margin-r15" @close="delete_role_menu(scope,m.id)">{{ cm.name }}</el-tag></el-col>
                        </el-row>
                    </template>
                </el-table-column>
                <el-table-column prop="id" label="id"  width="50"/>
                <el-table-column prop="name" label="名称"   />
                 <el-table-column prop="desc" label="详情"    />
                <el-table-column  label="操作"   >
                <template #default="scope">
                    <el-button type="primary" size="mini" @click="EditAuthor(scope.row)">编辑编辑</el-button>
                    <el-button type="primary" size="mini" @click="AuthorMenu(scope.row)">分配权限</el-button>
                    <el-button type="danger" size="mini" @click="deleteAuthor(scope.row)">删除</el-button>
                </template>
                </el-table-column> 
            </el-table>
        </el-row>
    </el-card>
    <el-dialog
        v-model="AuthorMenuVisible"
        title="分配权限"
        width="500"
        :before-close="handleClose"
    >
         <el-tree style="max-width: 600px" 
         :data="AuthorData" 
         :props="AuthorProps" 
         @node-click="handleNodeClick" 
          show-checkbox
          node-key="id" ref="AuthorRef" default-expand-all="true"
          />
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="AuthorMenuVisible = false">取消</el-button>
                <el-button type="primary" @click="HandleAuthor()">
                 确定
                </el-button>
            </div>
        </template>
    </el-dialog>
     <el-dialog
        v-model="addAuthorVisible"
        title="增加角色"
        width="500"
        :before-close="addrolehandleClose"
    >
         <el-form :model="addForm" ref="addRef" :rules="addRules">
            <el-form-item prop="name">
                <el-input v-model="addForm.name" placeholder="请输入名称"></el-input>
            </el-form-item>
            <el-form-item prop="description">
                <el-input v-model="addForm.description" placeholder="描述"></el-input>
            </el-form-item>

         </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="addrolehandleClose">取消</el-button>
                <el-button type="primary" @click="addHandleAuthor()">
                 确定
                </el-button>
            </div>
        </template>
    </el-dialog>
     <el-dialog
        v-model="editAuthorVisible"
        title="增加角色"
        width="500"
    >
         <el-form :model="editForm" ref="editRef" :rules="deditRules">
            <el-form-item prop="name">
                <el-input v-model="editForm.name" placeholder="请输入名称"></el-input>
            </el-form-item>
            <el-form-item prop="description">
                <el-input v-model="editForm.description" placeholder="描述"></el-input>
            </el-form-item>

         </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="editAuthorVisible=false">取消</el-button>
                <el-button type="primary" @click="editHandleAuthor()">
                 确定
                </el-button>
            </div>
        </template>
    </el-dialog>
    <el-dialog
        v-model="deleteAuthorVisible"
        title="删除角色"
        width="500"
    >
    <span>确认删除角色{{deleteForm.name}}吗？</span>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="deleteAuthorVisible=false">取消</el-button>
                <el-button type="danger" @click="deleteHandleAuthor()">
                 确定
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>


<script setup>
    import { ArrowRight,CirclePlus } from '@element-plus/icons-vue'
    import { ref, reactive,onMounted, nextTick } from 'vue'
    import api from "../api/index"

    //添加角色参数
    let addAuthorVisible=ref(false)
    let addRef=ref(null)
    const addForm=reactive({
        "name":null,
        "description":null
    })
    let addRules=reactive({
        "name":[
            { required: true, message: '请输入角色名称', trigger: 'blur' },
            { min: 3, max: 25, message: '长度在 3 到 25 个字符', trigger: 'blur' }
        ],
        "description":[
            { required: true, message: '请输入角色描述', trigger: 'blur' },
            {  max: 128, message: '长度不超过255个字符', trigger: 'blur' }
        ]
    })
    //编辑角色参数
    let editAuthorVisible=ref(false)
    let editRef=ref(null)
    const editForm=reactive({
        "id":null,
        "name":null,
    })
    let deditRules=reactive({
        "name":[
            { required: true, message: '请输入角色名称', trigger: 'blur' },
            { min: 3, max: 25, message: '长度在 3 到 25 个字符', trigger: 'blur' }
        ],
        "description":[
            { required: true, message: '请输入角色描述', trigger: 'blur' },
            {  max: 128, message: '长度不超过255个字符', trigger: 'blur' }
        ]
    })
    //删除角色参数
    let deleteAuthorVisible=ref(false)
    let deleteForm=reactive({
        "id":null,
        "name":null,
    })

    let AuthorMenuVisible = ref(false)

    let AuthorRef=ref([])

    let r_id=ref(null)

    let keyList = reactive([])

    const AuthorProps=reactive({
        children: 'children',
        label: 'name',
    })

    let AuthorData=reactive([])

    const dataable=reactive({
        tabledate:[]
    })

     onMounted(()=>{
        get_roles()
        get_menus()
    })

    const get_roles=()=>{
       api.getRolesList().then(res=>{
        if(res){
            if(res.data.code==200){
                console.log(res.data.data);
                dataable.tabledate=res.data.data;
            }
            else{
                ElMessage(res.data.msg);
            }
        }
        else{
            ElMessage('服务器异常！请稍后再试！');
        }

       })
    }

    //删除角色权限
    const delete_role_menu = (row,mid) => {
        ElMessageBox.confirm(
            '确定要删除该权限吗？',
            '警告',
            {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
            }
        )
            .then(() => {
                console.log(row.row.id,mid)
                api.DeleteRoleMenu(row.row.id,mid).then(res=>{
                    console.log(res)
                    if(res){
                        if(res.data.code==200){
                            ElMessage({
                                type: 'success',
                                message: '删除成功！',
                            })
                            get_roles();
                        }
                        else{
                            ElMessage({
                                type: 'error',
                                message: res.data.message,

                            });
                        }
                    }
                    else{
                        ElMessage('服务器异常！请稍后再试！');
                    }
                })
               
            })
            .catch(() => {
                ElMessage({
                    type: 'info',
                    message: '已取消',
                })
            })
    }

    const AuthorMenu=(row)=>{
        AuthorMenuVisible.value=true

        keyList=[]

        r_id.value=row.id

        row.menus.forEach(element => {
            element.children.forEach(celement => {
                keyList.push(celement.id)
            });
        });

        //渲染完后
        nextTick(()=>{ 
            AuthorRef.value.setCheckedKeys(keyList)
        })
        
    }

    const AuthorMenuClose = () => {
        AuthorMenuVisible.value = false
        //重置
        
    }

    const HandleAuthor=()=>{

        let mids=[
            AuthorRef.value.getCheckedKeys(),
            AuthorRef.value.getHalfCheckedKeys()
        ]
        mids=mids.join(",")

        api.EditRoleMenu(r_id.value,{'mids':mids}).then(res=>{
            if(res){
                console.log(res)
                if(res.data.code==200){
                    ElMessage({
                        type: 'success',
                        message: '分配成功！',
                    })
                    AuthorMenuClose()
                    get_roles()
                }
                else{
                    ElMessage({
                        type: 'error',
                        message: res.data.msg,

                    });
                }
            }
            else{
                ElMessage('服务器异常！请稍后再试！');
            }
        })
    }
    //获得菜单
    const get_menus=()=>{
        api.getMenus().then(res=>{
            if(res){
                if(res.data.code==200){
                    console.log(res.data.data);
                    AuthorData=res.data.data;
                }
                else{
                    ElMessage(res.data.msg);
                }
            }
            else{
                ElMessage('服务器异常！请稍后再试！');
            }
        })
    }
    //添加角色对话框关闭
    const addrolehandleClose=()=>{
        addAuthorVisible.value=false
        addRef.value.resetFields()
    }
    //添加角色事件
    const addHandleAuthor=()=>{
        api.addRole(addForm).then(res=>{
            console.log(res.data)
            if(res.data.code==200){
                ElMessage.success("添加成功")
                get_roles()
            }
            else{
                ElMessage.error("添加失败")
            }
            addrolehandleClose()
        })
    }
    //打开编辑角色对话框
    const EditAuthor=(row)=>{
        editAuthorVisible.value=true
        editForm.id=row.id
        editForm.name=row.name
        editForm.description=row.desc
    }
    //编辑角色事件
    const editHandleAuthor=()=>{
        api.editRole(editForm.id,editForm).then(res=>{
            console.log(res.data)
            if(res.data.code==200){
                ElMessage.success("修改成功")
                get_roles()
            }
            else{
                ElMessage.error("编辑失败")
            }
            editAuthorVisible.value=false
        })
    }
    const deleteHandleAuthor=()=>{
        api.deleteRole(deleteForm.id).then(res=>{
            console.log(res.data)
            if(res.data.code==200){
                ElMessage.success("删除成功")
                get_roles()
            }
            else{
                ElMessage.error("删除失败")
            }
            deleteAuthorVisible.value=false
        })
    }
    //打开删除角色对话框
    const deleteAuthor=(row)=>{
        deleteAuthorVisible.value=true
        deleteForm.id=row.id
        deleteForm.name=row.name
    }
</script>

<style scoped>
  .box-card{
    margin-top: 20px;
  }
  .margin-left50{
    margin-left: 50px;
  }
  .margin-t5{
    margin-top: 5px;
  }
  .margin-t15{
    margin-top: 10px;
  }
  .margin-r15{
    margin-right: 15px;
  }
  .margin-l15{
        margin-left: 15px;
  }
  .top{
    border-top: 1px solid #eee;
  }
  .bottom{
    border-bottom: 1px solid #eee;
  }
</style>