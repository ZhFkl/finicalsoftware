import request from '@/utils/request2'

// 频繁子图挖掘
export function digSubgraph(data) {
    return request({
        // datatype: 'json',
        url: 'data_show/new2',
        method: 'get'
    })
}