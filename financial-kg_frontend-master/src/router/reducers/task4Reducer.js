import Layout from '@/layout'

const Task4Router = {
  path: '/task4',
  component: Layout,
  redirect: '/task4/task41/task411',
  name: 'task4',
  meta: {
    title: '应用验证',
    icon: 'component',
    noCache: true,
    roles: ['admin']
  },
  children: [
    {
      path: 'task41',
      component: () => import('@/views/task4/task41/index'), // Parent router-view
      name: 'task41',
      meta: { 
        icon: 'menu',
        title: '深交所中小企业信用风险监测' 
      },
      redirect: '/task4/task41/task411',
      children: [
        {
          path: 'task411',
          component: () => import('@/views/task4/task41/task411'),
          name: 'task411',
          meta: {
            title: '资本市场舆情风险监测',
            noCache: true
          }
        },
        {
          path: 'task412',
          component: () => import('@/views/task4/task41/task412'),
          name: 'task412',
          meta: {
            title: '股权穿透式分析与监管',
            noCache: true
          }
        },
        {
          path: 'task413',
          component: () => import('@/views/task4/task41/task413'),
          name: 'task413',
          meta: {
            title: '网络舆情看板',
            noCache: true
          }
        }
      ]
    }, 
    {
      path: 'task42',
      component: () => import('@/views/task4/task42/index'), // Parent router-view
      name: 'task42',
      meta: { 
        icon: 'menu',
        title: '交通银行商业票据欺诈分析'
      },
      redirect: '/task4/task42/task421',
      children: [
        {
          path: 'task421',
          component: () => import('@/views/task4/task42/task421'),
          name: 'task421',
          meta: {
            title: '票据交易可视化分析',
            noCache: true
          }
        },
        {
          path: 'task422',
          component: () => import('@/views/task4/task42/task422'),
          name: 'task422',
          meta: {
            title: '交易公司社区分析',
            noCache: true
          }
        }
      ]
    }
  ]
}

export default Task4Router;