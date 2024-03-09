import request from '@/utils/request2'

// 频繁子图挖掘
export function digSubgraph(data) {
    return request({
        // datatype: 'json',
        url: 'task1/1?support=' + data.support + '&time=' + data.time + '&data='+ data.data,
        method: 'get'
    })
}

// 获得规则挖掘到统计信息
export function getMineInfo() {
    return request({
        datatype: 'json',
        url: 'task1/mine_info',
        method: 'get'
    })
}

// 获得风险评估到统计信息
export function getRiskInfo() {
    return request({
        datatype: 'json',
        url: 'task1/risk_info',
        method: 'get'
    })
}


// 获得风险评估到统计信息
export function getRiskExample() {
    return request({
        datatype: 'json',
        url: 'task1/risk_ex',
        method: 'get'
    })
}