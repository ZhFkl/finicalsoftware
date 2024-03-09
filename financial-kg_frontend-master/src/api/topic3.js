import request from '@/utils/request2'

export function dataList() {
  return request({
    url: '/task3/datalist',
    method: 'get'
  })
}

export function dataList3_3(dataset) {
  return request({
    url: '/task3/cluster/dataset',
    method: 'get',
    params:{
      dataset:dataset
    }
  })
}

export function newRule(dataset) {
  return request({
    url: '/task3/cluster/new_rules',
    method: 'get',
    params:{
      dataset:dataset
    }
  })
}
export function dbcluster(dataset, id_list) {
  return request({
    url: '/task3/cluster/dbscan',
    method: 'get',
    params:{
      dataset:dataset,
      new_ids:id_list
    }
  })
}

export function datainfo(dataset) {
  return request({
    url: '/task3/datainfo/' + dataset,
    method: 'get'
  })
}

export function filtration(dataset, layer, fullness) {
  return request({
    url: '/task3/filtration',
    method: 'get',
    params:{
      dataset:dataset,
      layer:layer,
      full_or_partial:fullness
    }
  })
}

export function dataFiltrationinfo(dataset) {
  return request({
    url: '/task3/moredatainfo/' + dataset,
    method: 'get'
  })
}

export function kernel(data) {
  //str:dataset，表示数据集名称 method，表示kernel中使用的方法 int:k，聚成多少类
  return request({
    url: '/task3/cluster/kernel?dataset=' + data.dataset +
      '&method=' + data.method + '&k=' + data.k+'&use_filtration='+data.use_filtration,
    method: 'get'
  })
}

export function infohyper(data) {
  //str:dataset，数据集名称，int:k，聚成多少类
  return request({
    url: '/task3/cluster/infohyper?dataset=' + data.dataset + '&k=' + data.k+'&use_filtration='+data.use_filtration,
    method: 'get'
  })
}

export function motif(data) {
  //str:dataset，数据集名称，int:k，聚成多少类
  return request({
    url: '/task3/cluster/motif?dataset=' + data.dataset + '&k=' + data.k+'&use_filtration='+data.use_filtration,
    method: 'get'
  })
}