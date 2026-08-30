/*
*
存储所有网络请求的接口
*
*/

const base = { 
    BaseUrl:'http://localhost:5000',
    login_url:'/user/login/',
    test_url:'/user/test/',
    menus_url:'/menu/menus/?type_=trea',
    get_menus_url:'/menu/menus/',
    get_users_url:'/user/users/',
    edit_user_url:'/user/user/',
    delete_user_url:'/user/user/',
    resetpass_url:'/user/reset_password/',
    get_roles_url:'/role/roles/',
    delete_role_menu_url:'/role/roles/',
    add_role_url:'/role/roles/',
    EditRoleMenu_url:'/role/',
    edit_role_url:'/role/role/',
    delete_role_url:'/role/role/',
    get_cates_url:'/category/',
    add_cate_url:'/category/',
    get_attri_url:'/attributes/',
    add_attri_url:'/attributes/',
    emit_attriD_url:'/attribute/',
    get_pro_url:"/products/",
    delele_pro_url:"/product/",
    upload_img_url:"/upload_img",
    add_pro_url:"/products/",
    get_orders_url:"/orders/",
    get_express_url:"/express/",
    get_cateGroup_url:"/category/cate_group/"
}


export default base;