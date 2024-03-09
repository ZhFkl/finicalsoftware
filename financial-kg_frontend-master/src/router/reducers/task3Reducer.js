import Layout from '@/layout'

const Task3Router = {
  path: '/task3',
  component: Layout,
  redirect: '/task3/task31/task311',
  name: 'task3',
  meta: {
    title: '图立方的挖掘、推理与风控',
    icon: 'component',
    noCache: true,
    roles: ['admin']
  },
  children: [
    {
      path: 'task31',
      component: () => import('@/views/task3/task31/index'), // Parent router-view
      name: 'task31',
      meta: {
        icon: 'menu',
        title: '图立方的挖掘'
      },
      redirect: '/task3/task31/task311',
      children: [
        {
          path: 'task311',
          component: () => import('@/views/task3/task31/topic1-1'),
          name: 'task311',
          meta: {
            title: '频繁子超图挖掘',
            noCache: true
          }
        },
        {
          path: 'task313',
          component: () => import('@/views/task3/task31/task313'),
          name: 'task313',
          meta: {
            title: '周期模式挖掘',
            noCache: true
          }
        },
        {
          path: 'task312',
          component: () => import('@/views/task3/task31/task312'),
          name: 'task312',
          meta: {
            title: '一阶谓词逻辑规则挖掘',
            noCache: true
          }
        }
      ]
    },
    {
      path: 'task32',
      component: () => import('@/views/task3/task32/index'), // Parent router-view
      name: 'task32',
      meta: {
        icon: 'menu',
        title: '图立方的推理'
      },
      redirect: '/task3/task32/task321',
      children: [
        {
          path: 'task321',
          component: () => import('@/views/task3/task32/task321'),
          name: 'task321',
          meta: {
            title: '基于规则的三步推理',
            noCache: true
          }
        },
        {
          path: 'task322',
          component: () => import('@/views/task3/task32/task322'),
          name: 'task322',
          meta: {
            title: '基于超图编辑距离的可解释性推理',
            noCache: true
          }
        },
        {
          path: 'task323',
          name: 'task323',
          component: () => import('@/views/task3/task32/task323'),
          meta: {
            title: '基于逻辑规则的关键节点推理',
            noCache: true
          }
        },
        {
          path: 'task324',
          name: 'task324',
          component: () => import('@/views/task3/task32/task324'),
          meta: {
            title: '基于深度特征的超边推理'
          }
        },
        {
          path: 'task325',
          name: 'task325',
          component: () => import('@/views/task3/task32/task325'),
          meta: {
            title: '基于压缩映射的超边推理',
            noCache: true
          }
        }
      ]
    },
    {
      path: 'task33',
      component: () => import('@/views/task3/task33/index'), // Parent router-view
      name: 'task33',
      meta: {
        icon: 'menu',
        title: '图立方的风控'
      },
      redirect: '/task3/task31/task331',
      children: [
        {
          path: 'task331',
          component: () => import('@/views/task3/task33/task331'),
          name: 'task331',
          meta: {
            title: '频繁子超图规则的风险评估',
            noCache: true
          }
        },
        {
          path: 'task332',
          component: () => import('@/views/task3/task33/task332'),
          name: 'task332',
          meta: {
            title: '互联网金融风险辨识',
            noCache: true
          }
        },
        {
          path: 'task333',
          component: () => import('@/views/task3/task33/task333'),
          name: 'task333',
          meta: {
            title: '金融黑天鹅事件的传播预测',
            noCache: true
          }
        },
        {
          path: 'task334',
          component: () => import('@/views/task3/task33/task334'),
          name: 'task334',
          meta: {
            title: '股市金融风险辨识',
            noCache: true
          }
        },
        {
          path: 'task335',
          component: () => import('@/views/task3/task33/task335'),
          name: 'task335',
          meta: {
            title: '基于逻辑规则的风险预警与防控',
            noCache: true
          }
        }
      ]
    }
  ]
}

export default Task3Router
