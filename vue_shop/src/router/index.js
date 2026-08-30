import { createRouter, createWebHistory } from 'vue-router'

const routes = [
      {
          path:'/login',
          name:'Login',
          component:()=>import('../views/LoginView.vue')
      },
      {
          path:'/',
          name:'Home',
          component:()=>import('../views/HomeView.vue'),
          redirect:'/welcome',
          children:[
            {
              path:'/welcome',
              name:'Welcome',
              component:()=>import('../views/WelcomeView.vue')
            },
            {
              path:'/user_list',
              name:'UserList',
              component:()=>import('../views/UserView.vue')
            },
            {
              path:'/role_list',
              name:'role_list',
              component:()=>import('../views/MenuView.vue')
            },
            {
              path:'/author_list',
              name:'author_list',
              component:()=>import('../views/AuthorView.vue')
            },
            {
              path:'/group_list',
              name:'group_list',
              component:()=>import('../views/GroupView.vue')
            },
            {
              path:'/attribute_list',
              name:'attribute_list',
              component:()=>import('../views/AttributeView.vue')
            },
            {
              path:'/product_list',
              name:'product_list',
              component:()=>import('../views/ProductView.vue')
            },
            {
              path:'/addPro',
              name:'addPro',
              component:()=>import('../views/AddProductView.vue')
            },
            {
              path:'/order_list',
              name:'order_list',
              component:()=>import('../views/OrderListView.vue')
            },
            {
              path:'/data_list',
              name:'data_list',
              component:()=>import('../views/DataListView.vue')
            }
          ]
      }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

//做router跳转的login_required的验证
router.beforeEach((to,from,next)=>{
  if(to.path=='/login'){
    next()
  }
  else{
    const token=sessionStorage.getItem('token')
    if(token){
      next()
    }
    else{
      next('/login')
    }
  }

})

