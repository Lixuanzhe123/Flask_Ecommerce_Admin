/**
 * 所有api封装
 * 
 * 
 */


import axios  from "../utils/request.js"
import base from './base.js'

const api={
    getLogin(params){
        return axios.post(base.BaseUrl+base.login_url,params)
    },
    getTest(){
        return axios.get(base.BaseUrl+base.test_url)
    },
    getMenus(){
        return axios.get(base.BaseUrl+base.menus_url)
    },
    getUsers(params){
        return axios.get(base.BaseUrl+base.get_users_url,params)
    },
    addUser(params){
        return axios.post(base.BaseUrl+base.get_users_url,params)
    },
    EditUser(id,params){
        return axios.put(base.BaseUrl+base.edit_user_url+id+'/',params)
    },
    getUser(id){
        return axios.get(base.BaseUrl+base.edit_user_url+id+'/')
    },
    deleteUser(id){
        return axios.delete(base.BaseUrl+base.delete_user_url+id+'/')
    },
    resetPass(id,params){
        return axios.put(base.BaseUrl+base.resetpass_url+id+'/',params)
    },
    getMenusList(){
        return axios.get(base.BaseUrl+base.get_menus_url)
    },
    getRolesList(){
        return axios.get(base.BaseUrl+base.get_roles_url)
    },
    addRole(params){
        return axios.post(base.BaseUrl+base.add_role_url,params)
    },
    DeleteRoleMenu(rid,mid){
        return axios.delete(base.BaseUrl+base.delete_role_menu_url+rid+'/'+mid+'/')
    },
    EditRoleMenu(rid,params){ 
        return axios.post(base.BaseUrl+base.EditRoleMenu_url+rid+'/',params)
    },
    getCatesList(level){
        return axios.get(base.BaseUrl+base.get_cates_url+'?level='+level)
    },
    addCateList(params){ 
        return axios.post(base.BaseUrl+base.add_cate_url,params)
    },
    getAttriList(cid,_type){ 
        return axios.get(base.BaseUrl+base.get_attri_url+'?cid='+cid+'&_type='+_type)
    },
    addAttriList(params){ 
        return axios.post(base.BaseUrl+base.add_attri_url,params)
    },
    editAttriList(id,params){ 
        return axios.put(base.BaseUrl+base.emit_attriD_url+id+'/',params)
    },
    getProList(name){
        return axios.get(base.BaseUrl+base.get_pro_url+'?name='+name)
    },
    deleteProList(id){
        return axios.delete(base.BaseUrl+base.delele_pro_url+id+'/')
    },
    addProList(params){
        return axios.post(base.BaseUrl+base.add_pro_url,params)
    },
    getOrdersList(){
        return axios.get(base.BaseUrl+base.get_orders_url)
    },
    getExpressList(id){
        return axios.get(base.BaseUrl+base.get_express_url+id+'/')
    },
    getCateGroupList(){
        return axios.get(base.BaseUrl+base.get_cateGroup_url)
    },
    editRole(id,params){
        return axios.put(base.BaseUrl+base.edit_role_url+id+'/',params)
    },
    deleteRole(id){
        return axios.delete(base.BaseUrl+base.delete_role_url+id+'/')
    },
}

export default api