import Layout from '@/layout'

const Task5Router = {
  path: '/task5',
  component: Layout,
  redirect: '/task5/task51',
  name: 'org_mgmt',
  meta: {
    title: '工具集',
    icon: 'component',
    noCache: true,
    roles: ['admin']
  },
  children: [
    {
      path: 'task51',
      component: () => import('@/views/task5/task51'),
      name: 'task51',
      meta: {
        title: '数据标注平台',
        icon: 'menu',
        noCache: true
      }
    },
    {
      path: 'task52',
      component: () => import('@/views/task5/task52'),
      name: 'task52',
      meta: {
        title: '图立方的表示学习',
        icon: 'menu',
        noCache: true
      }
    },
    {
      path: 'task54',
      component: () => import('@/views/task5/task54/index'), // Parent router-view
      name: 'task54',
      meta: { 
        icon: 'menu',
        title: '舆情分析'
      },
      redirect: '/task5/task54/task541',
      children: [
        {
          path: 'task541',
          component: () => import('@/views/task5/task54/task541'),
          name: 'task541',
          meta: {
            title: '舆情主题监测',
            noCache: true
          }
        },
        {
          path: 'task542',
          component: () => import('@/views/task5/task54/task542'),
          name: 'task542',
          meta: {
            title: '基于多模态股评的舆情情感分析',
            noCache: true
          }
        }
      ]
    }, 
    {
      path: 'task55',
      component: () => import('@/views/task5/task55/index'), // Parent router-view
      name: 'task55',
      meta: { 
        icon: 'menu',
        title: '子超图规则集成归纳'
      },
      redirect: '/task5/task55/topic3-1',
      children: [
        {       
          path: 'topic3-1',
          component: () => import('@/views/task5/task55/topic3-1'),
          name: 'topic3-1',
          meta: {
            title: '基于特征的超图规则归纳',
            noCache: true
          }
        },
        {
          path: 'topic3-2',
          name: 'topic3-2',
          component: () => import('@/views/task5/task55/topic3-2'),
          meta: {
            title: '基于嵌入的超图规则归纳',
            noCache: true
          }
        },
        {
          path: 'topic3-3',
          component: () => import('@/views/task5/task55/topic3-3'),
          name: 'topic3-3',
          meta: {
            title: '基于聚类的动态规则归纳',
            noCache: true
          }
        }
      ]
    },

  ]
}

export default Task5Router;