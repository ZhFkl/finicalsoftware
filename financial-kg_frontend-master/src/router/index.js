import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'
import Task3Router from './reducers/task3Reducer'
import Task5Router from './reducers/task5Reducer'
import Task4Router from './reducers/task4Reducer'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    noCache: true                if set true, the page will no be cached(default is false)
    affix: true                  if set true, the tag will affix in the tags-view
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path(.*)',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/auth-redirect',
    component: () => import('@/views/login/auth-redirect'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/error-page/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/error-page/401'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/task1/task11',
    meta: {
      title: '图立方的构建',
      icon: 'component',
      noCache: true,
      roles: ['admin']
    },
    children: [

      // {
      //   path: '/task1/task12',
      //   component: () => import('@/views/task1/task12'),
      //   name: 'task12',
      //   meta: {
      //     title: '图立方的抽取',
      //     icon: 'menu',
      //     noCache: true
      //   }
      // },
      {
        path: '/task1/task11',
        component: () => import('@/views/task1/task11'),
        name: 'task11',
        meta: {
          title: '芜湖',
          icon: 'menu',
          noCache: true
        }
      },
      // {
      //   path: 'task1/task13',
      //   component: () => import('@/views/task1/task13'),
      //   name: 'task13',
      //   meta: {
      //     title: '图立方的融合',
      //     icon: 'menu',
      //     noCache: true
      //   }
      // },
      // {
      //   path: 'task1/task14',
      //   component: () => import('@/views/task1/task14'),
      //   name: 'task14',
      //   meta: {
      //     title: '图立方的概览',
      //     icon: 'menu',
      //     noCache: true
      //   }
      // }
    ]
  },
  {
    path: '/profile',
    component: Layout,
    redirect: '/profile/index',
    hidden: true,
    children: [
      {
        path: 'index',
        component: () => import('@/views/profile/index'),
        name: 'Profile',
        meta: { title: 'profile', icon: 'user', noCache: true }
      }
    ]
  },
  {
    path: '/task2',
    component: Layout,
    redirect: '/task2/task21',
    name: 'org_mgmt',
    meta: {
      title: '图立方的查询',
      icon: 'component',
      noCache: true,
      roles: ['admin']
    },
    children: [
      {
        path: 'task21',
        component: () => import('@/views/task2/task21'),
        name: 'task21',
        meta: {
          title: '简单查询',
          icon: 'menu',
          noCache: true
        }
      },
      {
        path: 'task22',
        component: () => import('@/views/task2/task22'),
        name: 'task22',
        meta: {
          title: '多跳查询',
          icon: 'menu',
          noCache: true
        }
      },
      {
        path: 'task23',
        component: () => import('@/views/task2/task23'),
        name: 'task23',
        meta: {
          title: '复杂查询',
          icon: 'menu',
          noCache: true
        }
      }
    ]
  },
  Task3Router,
  Task4Router,
  Task5Router,
]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  /**
   * 暂时不用异步路由了，避免出现刷新时因只有constants无法正确路由的问题
   */
  // {
  //   path: '/task2',
  //   component: Layout,
  //   redirect: '/task2/task21',
  //   name: 'org_mgmt',
  //   meta: {
  //     title: '图立方的查询',
  //     icon: 'component',
  //     noCache: true,
  //     roles: ['admin']
  //   },
  //   children: [
  //     {
  //       path: 'task21',
  //       component: () => import('@/views/task2/task21'),
  //       name: 'task21',
  //       meta: {
  //         title: '简单图查询',
  //         icon: 'menu',
  //         noCache: true
  //       }
  //     },
  //     {
  //       path: 'task22',
  //       component: () => import('@/views/task2/task22'),
  //       name: 'task22',
  //       meta: {
  //         title: '时序关系查询',
  //         icon: 'menu',
  //         noCache: true
  //       }
  //     },
  //     {
  //       path: 'task23',
  //       component: () => import('@/views/task2/task23'),
  //       name: 'task23',
  //       meta: {
  //         title: '超图关系查询',
  //         icon: 'menu',
  //         noCache: true
  //       }
  //     }
  //   ]
  // },
  // Task3Router,
  // //task4-->课题五待填
  // Task5Router,
  /** when your routing map is too long, you can split it into small modules **/

  // {
  //   path: '/topic2',
  //   component: Layout,
  //   redirect: '/topic2/topic2-1',
  //   meta: {
  //     title: '规则推理',
  //     icon: 'documentation'
  //   },
  //   children: [
  //     {
  //       path: 'topic2-1',
  //       name: 'topic2-1',
  //       component: () => import('@/views/topic2/topic2-1'),
  //       meta: {
  //         title: '深度特征',
  //         icon: 'documentation'
  //       }
  //     },
  //     {
  //       path: 'topic2-2',
  //       name: 'topic2-2',
  //       component: () => import('@/views/topic2/topic2-2'),
  //       meta: {
  //         title: '压缩映射',
  //         icon: 'nested',
  //         noCache: true
  //       }
  //     },
  //     {
  //       path: 'topic2-3',
  //       component: () => import('@/views/topic2/topic2-3'),
  //       name: 'permission',
  //       meta: {
  //         title: '语义结构',
  //         icon: 'chart',
  //         noCache: true
  //       }
  //     }
  //   ]
  // },

  // {
  //   path: '/topic3',
  //   component: Layout,
  //   redirect: '/topic3/topic3-1',
  //   meta: {
  //     title: '知识归纳',
  //     icon: 'documentation'
  //   },
  //   children: [
  //     // {
  //     //   path: 'topic3overview',
  //     //   component: () => import('@/views/topic3/overview'),
  //     //   name: 'overview',
  //     //   meta: {
  //     //     title: '总览',
  //     //     icon: 'people',
  //     //     noCache: true
  //     //   }
  //     // },
  //     {
  //       path: 'topic3-1',
  //       component: () => import('@/views/topic3/topic3-1'),
  //       name: 'topic3-1',
  //       meta: {
  //         title: '知识智能归纳',
  //         icon: 'people',
  //         noCache: true
  //       }
  //     },
  //     {
  //       path: 'topic3-2',
  //       name: 'topic3-2',
  //       component: () => import('@/views/topic3/topic3-2'),
  //       meta: {
  //         title: '“图立方”嵌入',
  //         icon: 'peoples',
  //         noCache: true
  //       }
  //     },
  //     {
  //       path: 'topic3-3',
  //       component: () => import('@/views/topic3/topic3-3'),
  //       name: 'topic3-3',
  //       meta: {
  //         title: '动态聚类',
  //         icon: 'skill',
  //         noCache: true
  //       }
  //     }
  //   ]
  // },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
