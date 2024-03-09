import Mock from 'mockjs'

const List = []
const count = 100

const baseContent = '<p>I am testing data, I am testing data.</p><p><img src="https://wpimg.wallstcn.com/4c69009c-0fd4-4153-b112-6cb53d1cf943"></p>'
const image_uri = 'https://wpimg.wallstcn.com/e4558086-631c-425c-9430-56ffb46e70b3'

for (let i = 0; i < count; i++) {
  List.push(Mock.mock({
    id: '@increment',
    timestamp: +Mock.Random.date('T'),
    author: '@first',
    reviewer: '@first',
    title: '@title(5, 10)',
    content_short: 'mock data',
    content: baseContent,
    forecast: '@float(0, 100, 2, 2)',
    importance: '@integer(1, 3)',
    'type|1': ['CN', 'US', 'JP', 'EU'],
    'status|1': ['published', 'draft'],
    display_time: '@datetime',
    comment_disabled: true,
    pageviews: '@integer(300, 5000)',
    image_uri,
    platforms: ['a-platform']
  }))
}

export default [
  {
    url: '/vue-element-admin/task/task',
    type: 'get',
    response: config => {
      // eslint-disable-next-line no-unused-vars
      const { importance, type, title, page = 1, limit = 20, sort } = config.query
      return { 'code': 10000, 'message': '接口调用成功,调用结果请参考具体的业务返回参数', 'subCode': null, 'subMessage': null, 'data': { 'pageNum': 1, 'pageSize': 10, 'size': 10, 'orderBy': null, 'startRow': 1, 'endRow': 10, 'total': 141, 'pages': 15, 'list': [{ 'id': '181206be4321450a8104e20d6fe221c0', 'taskTask': { 'id': '181206be4321450a8104e20d6fe221c0', 'createBy': '1', 'createDate': '2020-03-29T06:40:28.000+0000', 'updateBy': '1', 'updateDate': '2020-03-29T06:40:28.000+0000', 'remarks': null, 'delFlag': '0', 'name': '网络流量分析', 'description': '网络流量分析', 'algoId': '39163feca6dc4c638437fbf8fe8ab29c', 'datasetId': 'd03def44008b419280aa62e6df060e89', 'sparkId': '10', 'state': '0', 'result': '/1/KNN/网络流量分析/1585464004995/resultPath', 'resultModel': '/1/KNN/网络流量分析//modelPath', 'sparkLog': '[stdout: , \nstderr: ]' }, 'userName': '123', 'datasetName': 'dataset_platform', 'datasetUrl': '/mycode/dataset/dataset_platform.csv', 'algoName': 'KNN', 'algoUrl': 'hdfs://namenode:8020/mycode/python/spark_loadKNN_Model_0329.py', 'taskParameterVOList': [{ 'name': 'resultPath', 'taskParameter': { 'id': '3392a97a167b49069d9a8806dd6c238f', 'createBy': '1', 'createDate': '2020-03-29T06:40:28.000+0000', 'updateBy': '1', 'updateDate': '2020-03-29T06:40:28.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '9642cf9503b94b23892de295c5a643a9', 'taskId': '181206be4321450a8104e20d6fe221c0', 'context': '/1/KNN/网络流量分析/1585464004995/resultPath' }}, { 'name': 'featureCol', 'taskParameter': { 'id': '6313e1d224d644c9bd5fe5c37c424122', 'createBy': '1', 'createDate': '2020-03-29T06:40:28.000+0000', 'updateBy': '1', 'updateDate': '2020-03-29T06:40:28.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '72fa4c032caa46fe8f9a75bc3bba2767', 'taskId': '181206be4321450a8104e20d6fe221c0', 'context': '0,1,2,3,4,5,6,7' }}, { 'name': 'labelCol', 'taskParameter': { 'id': 'ef86acc156db4bd8af6ad6ccc1dde5b1', 'createBy': '1', 'createDate': '2020-03-29T06:40:28.000+0000', 'updateBy': '1', 'updateDate': '2020-03-29T06:40:28.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '0ad1ae862e174df99bd972b6aa65c5a4', 'taskId': '181206be4321450a8104e20d6fe221c0', 'context': '8' }}, { 'name': 'modelPath', 'taskParameter': { 'id': 'f806eef558a14559ab4ee7629ec6f5a1', 'createBy': '1', 'createDate': '2020-03-29T06:40:28.000+0000', 'updateBy': '1', 'updateDate': '2020-03-29T06:40:28.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '9b861b1aad6849e9898af9f582965365', 'taskId': '181206be4321450a8104e20d6fe221c0', 'context': '/1/KNN/网络流量分析//modelPath' }}] }, { 'id': '25c449f2e24343c7be9f56c49987efcc', 'taskTask': { 'id': '25c449f2e24343c7be9f56c49987efcc', 'createBy': '1', 'createDate': '2020-05-26T10:55:21.000+0000', 'updateBy': '1', 'updateDate': '2020-05-26T10:55:21.000+0000', 'remarks': null, 'delFlag': '0', 'name': '这是测试', 'description': '这是测试', 'algoId': '7f9bc12745f24ea990e3cd88236fcd23', 'datasetId': 'c57b42e34e4443568ae680179b8510a9', 'sparkId': '12', 'state': '0', 'result': '/1/PCA/这是测试/1590490518569/resultPath', 'resultModel': null, 'sparkLog': '[stdout: , \nstderr: ]' }, 'userName': '123', 'datasetName': '城镇居民家庭基本情况csv', 'datasetUrl': '/mycode/dataset/2017_城镇居民家庭基本情况.csv', 'algoName': 'PCA', 'algoUrl': 'hdfs://namenode:8020/mycode/python/PCA.py', 'taskParameterVOList': [{ 'name': 'K', 'taskParameter': { 'id': '0372a86f6e93478b8d599f12f1a4d19b', 'createBy': '1', 'createDate': '2020-05-26T10:55:21.000+0000', 'updateBy': '1', 'updateDate': '2020-05-26T10:55:21.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': 'ef6b78c91e2845198ae1d7b4637153b8', 'taskId': '25c449f2e24343c7be9f56c49987efcc', 'context': '3' }}, { 'name': 'resultPath', 'taskParameter': { 'id': 'dea80d15572149d584ada60830a2239a', 'createBy': '1', 'createDate': '2020-05-26T10:55:21.000+0000', 'updateBy': '1', 'updateDate': '2020-05-26T10:55:21.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '1608784db925494d9dae2d326878b116', 'taskId': '25c449f2e24343c7be9f56c49987efcc', 'context': '/1/PCA/这是测试/1590490518569/resultPath' }}] }, { 'id': '68bc61946e1e4005954373e1b5f3915a', 'taskTask': { 'id': '68bc61946e1e4005954373e1b5f3915a', 'createBy': '1', 'createDate': '2019-10-31T10:08:28.000+0000', 'updateBy': '1', 'updateDate': '2019-10-31T10:08:28.000+0000', 'remarks': null, 'delFlag': '0', 'name': '广播电视属性间的相关性分析', 'description': '广播电视属性间的相关性分析', 'algoId': '37a93fcba469464f852aa3db33567e9d', 'datasetId': '7f5daf7dce1a4eafb9dead35d761f6d7', 'sparkId': '459', 'state': '1', 'result': '/1/fpgrowth/广播电视属性间的相关性分析/1572487706213/resultPath', 'resultModel': '/1/fpgrowth/广播电视属性间的相关性分析/1572487706213/modelPath', 'sparkLog': '[stdout: , \nstderr: ]' }, 'userName': '123', 'datasetName': '年度广播数据10-18', 'datasetUrl': '/mycode/dataset/年度广播数据10-18.csv', 'algoName': 'fpgrowth', 'algoUrl': '/mycode/python/fpgrowth.py', 'taskParameterVOList': [{ 'name': null, 'taskParameter': { 'id': '1119ba933850454aa8a014c6480685f6', 'createBy': '1', 'createDate': '2019-10-31T10:08:28.000+0000', 'updateBy': '1', 'updateDate': '2019-10-31T10:08:28.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '585981cc396244f4a97f0daef64e8c27', 'taskId': '68bc61946e1e4005954373e1b5f3915a', 'context': '/1/fpgrowth/广播电视属性间的相关性分析/1572487706213/modelPath' }}, { 'name': null, 'taskParameter': { 'id': 'c8169e5ce061419faccfb775dd40baba', 'createBy': '1', 'createDate': '2019-10-31T10:08:28.000+0000', 'updateBy': '1', 'updateDate': '2019-10-31T10:08:28.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '7d01ba240588401585f9c56c57892135', 'taskId': '68bc61946e1e4005954373e1b5f3915a', 'context': '/1/fpgrowth/广播电视属性间的相关性分析/1572487706213/resultPath' }}] }, { 'id': '6b136d3d5d0f4a6ea0b642dbac7f2afe', 'taskTask': { 'id': '6b136d3d5d0f4a6ea0b642dbac7f2afe', 'createBy': '1', 'createDate': '2019-11-02T10:55:31.000+0000', 'updateBy': '1', 'updateDate': '2019-11-02T10:55:31.000+0000', 'remarks': null, 'delFlag': '0', 'name': '医疗保险市场网络相关信息分类', 'description': '医疗保险市场网络相关信息分类', 'algoId': '0', 'datasetId': '3693a44d0f11442e8f9b90d3605cb5f8', 'sparkId': '7', 'state': '0', 'result': '/e9067044-1c50-43a8-9d89-3167ea055305/GradienBoosted/医疗保险市场网络相关信息分类/1572692128077/resultPath', 'resultModel': '/e9067044-1c50-43a8-9d89-3167ea055305/GradienBoosted/医疗保险市场网络相关信息分类/1572692128077/modelPath', 'sparkLog': '[stdout: , \nstderr: ]' }, 'userName': '123', 'datasetName': '美国医疗保险市场网络数据集4', 'datasetUrl': '/mycode/dataset/美国医疗保险市场网络数据集4.csv', 'algoName': 'GradienBoosted', 'algoUrl': 'hdfs://namenode:8020/mycode/python/Gradien_boosted.py', 'taskParameterVOList': [{ 'name': 'featuresCol', 'taskParameter': { 'id': '3af133374fef489182a5929aae040e71', 'createBy': '1', 'createDate': '2019-11-02T10:55:31.000+0000', 'updateBy': '1', 'updateDate': '2019-11-02T10:55:31.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '0', 'taskId': '6b136d3d5d0f4a6ea0b642dbac7f2afe', 'context': '0;1;2;3;4;5;6;7;8;9;10' }}, { 'name': 'resultPath', 'taskParameter': { 'id': '458cb6500a9c4a818abac481c8848ea0', 'createBy': '1', 'createDate': '2019-11-02T10:55:31.000+0000', 'updateBy': '1', 'updateDate': '2019-11-02T10:55:31.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '2f251dc8da1d4f398b6e3381b109f8e4', 'taskId': '6b136d3d5d0f4a6ea0b642dbac7f2afe', 'context': '/e9067044-1c50-43a8-9d89-3167ea055305/GradienBoosted/医疗保险市场网络相关信息分类/1572692128077/resultPath' }}, { 'name': 'modelPath', 'taskParameter': { 'id': 'b1be47d3778b4efaa1e7e823356771b1', 'createBy': '1', 'createDate': '2019-11-02T10:55:31.000+0000', 'updateBy': '1', 'updateDate': '2019-11-02T10:55:31.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '24263f784fd74282adc8e24be5cba61b', 'taskId': '6b136d3d5d0f4a6ea0b642dbac7f2afe', 'context': '/e9067044-1c50-43a8-9d89-3167ea055305/GradienBoosted/医疗保险市场网络相关信息分类/1572692128077/modelPath' }}, { 'name': 'labelCol', 'taskParameter': { 'id': 'fcd022eb828a494da8f2195409fabef4', 'createBy': '1', 'createDate': '2019-11-02T10:55:31.000+0000', 'updateBy': '1', 'updateDate': '2019-11-02T10:55:31.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '1', 'taskId': '6b136d3d5d0f4a6ea0b642dbac7f2afe', 'context': '11' }}] }, { 'id': '84c39a488cf043be921f891a699ab2dc', 'taskTask': { 'id': '84c39a488cf043be921f891a699ab2dc', 'createBy': '1', 'createDate': '2019-10-31T01:04:17.000+0000', 'updateBy': '1', 'updateDate': '2019-10-31T01:04:17.000+0000', 'remarks': null, 'delFlag': '0', 'name': '证券股票日线回归分析', 'description': '证券股票日线回归分析1020测试', 'algoId': 'f2f3d2e4705b4dc1832e7d1fcef7e20b', 'datasetId': '1970d2efb0234636b49e8578afa005fc', 'sparkId': '458', 'state': '1', 'result': '/e9067044-1c50-43a8-9d89-3167ea055305/Glinear_regression/证券股票日线回归分析/1572455055736/resultPath', 'resultModel': '/e9067044-1c50-43a8-9d89-3167ea055305/Glinear_regression/证券股票日线回归分析/1572455055736/modelPath', 'sparkLog': '[stdout: , \nstderr: ]' }, 'userName': '123', 'datasetName': '上海证券A股日线', 'datasetUrl': '/mycode/dataset/上海证券A股日线.csv', 'algoName': 'Glinear_regression', 'algoUrl': '/mycode/python/Glinear_regression.py', 'taskParameterVOList': [{ 'name': 'labelCol', 'taskParameter': { 'id': '1c6c1997de4f4aae9269c6baa27baf10', 'createBy': '1', 'createDate': '2019-10-31T01:04:17.000+0000', 'updateBy': '1', 'updateDate': '2019-10-31T01:04:17.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '48e85c0aa3644ddbb8443dd7d31dc1ba', 'taskId': '84c39a488cf043be921f891a699ab2dc', 'context': '4' }}, { 'name': 'resultPath', 'taskParameter': { 'id': '5ffcfbc651c94a09bca144cc0aa95d62', 'createBy': '1', 'createDate': '2019-10-31T01:04:17.000+0000', 'updateBy': '1', 'updateDate': '2019-10-31T01:04:17.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': 'bf52e05249fb44f994c6a7876e721948', 'taskId': '84c39a488cf043be921f891a699ab2dc', 'context': '/e9067044-1c50-43a8-9d89-3167ea055305/Glinear_regression/证券股票日线回归分析/1572455055736/resultPath' }}, { 'name': 'modelPath', 'taskParameter': { 'id': '9b1f3cef373b477fb0f47ef81f6f57db', 'createBy': '1', 'createDate': '2019-10-31T01:04:17.000+0000', 'updateBy': '1', 'updateDate': '2019-10-31T01:04:17.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '9f233a9770e643229b7972345041e9f4', 'taskId': '84c39a488cf043be921f891a699ab2dc', 'context': '/e9067044-1c50-43a8-9d89-3167ea055305/Glinear_regression/证券股票日线回归分析/1572455055736/modelPath' }}, { 'name': 'featuresCol', 'taskParameter': { 'id': 'f5808910cf58417e993ebf9af65d421a', 'createBy': '1', 'createDate': '2019-10-31T01:04:17.000+0000', 'updateBy': '1', 'updateDate': '2019-10-31T01:04:17.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '367a143046a747609d2a85ea0512033b', 'taskId': '84c39a488cf043be921f891a699ab2dc', 'context': '0;1;2;3' }}] }, { 'id': '98e36d5deb484ecd8144aa5e6284c0bc', 'taskTask': { 'id': '98e36d5deb484ecd8144aa5e6284c0bc', 'createBy': '1', 'createDate': '2019-10-31T01:03:54.000+0000', 'updateBy': '1', 'updateDate': '2019-10-31T01:03:54.000+0000', 'remarks': null, 'delFlag': '0', 'name': '城镇居民基本家庭状况', 'description': '城镇居民基本家庭状况', 'algoId': '7f9bc12745f24ea990e3cd88236fcd23', 'datasetId': 'c57b42e34e4443568ae680179b8510a9', 'sparkId': '457', 'state': '1', 'result': '/e9067044-1c50-43a8-9d89-3167ea055305/PCA/城镇居民基本家庭状况/1572455032703/resultPath', 'resultModel': null, 'sparkLog': '[stdout: , \nstderr: ]' }, 'userName': '123', 'datasetName': '城镇居民家庭基本情况csv', 'datasetUrl': '/mycode/dataset/2017_城镇居民家庭基本情况.csv', 'algoName': 'PCA', 'algoUrl': 'hdfs://namenode:8020/mycode/python/PCA.py', 'taskParameterVOList': [{ 'name': 'resultPath', 'taskParameter': { 'id': 'd40b38bb89654c32a2be6cba218d98c5', 'createBy': '1', 'createDate': '2019-10-31T01:03:54.000+0000', 'updateBy': '1', 'updateDate': '2019-10-31T01:03:54.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '1608784db925494d9dae2d326878b116', 'taskId': '98e36d5deb484ecd8144aa5e6284c0bc', 'context': '/e9067044-1c50-43a8-9d89-3167ea055305/PCA/城镇居民基本家庭状况/1572455032703/resultPath' }}, { 'name': 'K', 'taskParameter': { 'id': 'f083bf9d606b4450b793c762f2360110', 'createBy': '1', 'createDate': '2019-10-31T01:03:54.000+0000', 'updateBy': '1', 'updateDate': '2019-10-31T01:03:54.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': 'ef6b78c91e2845198ae1d7b4637153b8', 'taskId': '98e36d5deb484ecd8144aa5e6284c0bc', 'context': '3' }}] }, { 'id': 'aaf042dfd9bb41a38ad20ae1514076a8', 'taskTask': { 'id': 'aaf042dfd9bb41a38ad20ae1514076a8', 'createBy': '1', 'createDate': '2020-05-26T10:23:48.000+0000', 'updateBy': '1', 'updateDate': '2020-05-26T10:23:48.000+0000', 'remarks': null, 'delFlag': '0', 'name': 'test', 'description': 'test', 'algoId': '39163feca6dc4c638437fbf8fe8ab29c', 'datasetId': 'd03def44008b419280aa62e6df060e89', 'sparkId': '5', 'state': '0', 'result': '/1/KNN/test/1590488620246/resultPath', 'resultModel': '/1/KNN/test/1590488620246/modelPath', 'sparkLog': '[stdout: , \nstderr: ]' }, 'userName': '123', 'datasetName': 'dataset_platform', 'datasetUrl': '/mycode/dataset/dataset_platform.csv', 'algoName': 'KNN', 'algoUrl': 'hdfs://namenode:8020/mycode/python/spark_loadKNN_Model_0329.py', 'taskParameterVOList': [{ 'name': 'modelPath', 'taskParameter': { 'id': '76a3bbf39fd8433da4b53079f8bcb128', 'createBy': '1', 'createDate': '2020-05-26T10:23:48.000+0000', 'updateBy': '1', 'updateDate': '2020-05-26T10:23:48.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '9b861b1aad6849e9898af9f582965365', 'taskId': 'aaf042dfd9bb41a38ad20ae1514076a8', 'context': '/1/KNN/test/1590488620246/modelPath' }}, { 'name': 'featureCol', 'taskParameter': { 'id': '7f36b7f9766b4bcb95125d80e27063d1', 'createBy': '1', 'createDate': '2020-05-26T10:23:48.000+0000', 'updateBy': '1', 'updateDate': '2020-05-26T10:23:48.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '72fa4c032caa46fe8f9a75bc3bba2767', 'taskId': 'aaf042dfd9bb41a38ad20ae1514076a8', 'context': '0' }}, { 'name': 'resultPath', 'taskParameter': { 'id': 'c2a7be7a50114e188070734c9799a562', 'createBy': '1', 'createDate': '2020-05-26T10:23:48.000+0000', 'updateBy': '1', 'updateDate': '2020-05-26T10:23:48.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '9642cf9503b94b23892de295c5a643a9', 'taskId': 'aaf042dfd9bb41a38ad20ae1514076a8', 'context': '/1/KNN/test/1590488620246/resultPath' }}, { 'name': 'labelCol', 'taskParameter': { 'id': 'fa6a7a68c121453395d3530fffa69ca3', 'createBy': '1', 'createDate': '2020-05-26T10:23:48.000+0000', 'updateBy': '1', 'updateDate': '2020-05-26T10:23:48.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '0ad1ae862e174df99bd972b6aa65c5a4', 'taskId': 'aaf042dfd9bb41a38ad20ae1514076a8', 'context': '7' }}] }, { 'id': 'abeb83a56a1c41209430374ec3371746', 'taskTask': { 'id': 'abeb83a56a1c41209430374ec3371746', 'createBy': '1', 'createDate': '2019-10-31T00:49:40.000+0000', 'updateBy': '1', 'updateDate': '2019-10-31T00:49:40.000+0000', 'remarks': null, 'delFlag': '0', 'name': '信用卡欺诈数据集特征变换', 'description': '信用卡欺诈数据集特征变换', 'algoId': 'b76d3e03789b44d9a6a13af02327a18a', 'datasetId': '3fcb1c77d0634cbe99d3ec739d6df5f2', 'sparkId': '456', 'state': '1', 'result': '/e9067044-1c50-43a8-9d89-3167ea055305/IndexToString/信用卡欺诈数据集特征变换/1572454177685/resultPath', 'resultModel': '/e9067044-1c50-43a8-9d89-3167ea055305/IndexToString/信用卡欺诈数据集特征变换/1572454177685/modelPath', 'sparkLog': '[stdout: , \nstderr: ]' }, 'userName': '123', 'datasetName': '信用卡欺诈数据集string', 'datasetUrl': '/mycode/dataset/信用卡欺诈数据集string.csv', 'algoName': 'IndexToString', 'algoUrl': '/mycode/python/IndexToString.py', 'taskParameterVOList': [{ 'name': 'resultPath', 'taskParameter': { 'id': '456a564519e0414884ca0a1cfde5ed80', 'createBy': '1', 'createDate': '2019-10-31T00:49:40.000+0000', 'updateBy': '1', 'updateDate': '2019-10-31T00:49:40.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': 'c93f9ef21eeb475183d1426d93a3d9af', 'taskId': 'abeb83a56a1c41209430374ec3371746', 'context': '/e9067044-1c50-43a8-9d89-3167ea055305/IndexToString/信用卡欺诈数据集特征变换/1572454177685/resultPath' }}, { 'name': 'modelPath', 'taskParameter': { 'id': 'b48b7c41b4624434a42da3d326f5bb3d', 'createBy': '1', 'createDate': '2019-10-31T00:49:40.000+0000', 'updateBy': '1', 'updateDate': '2019-10-31T00:49:40.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': 'a8563caa26984ecc919a8f7c045e6109', 'taskId': 'abeb83a56a1c41209430374ec3371746', 'context': '/e9067044-1c50-43a8-9d89-3167ea055305/IndexToString/信用卡欺诈数据集特征变换/1572454177685/modelPath' }}, { 'name': 'labelCol', 'taskParameter': { 'id': 'cdcb4a3f9ad541febaf1173fa232b012', 'createBy': '1', 'createDate': '2019-10-31T00:49:40.000+0000', 'updateBy': '1', 'updateDate': '2019-10-31T00:49:40.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '8537ca643ebc4f77aecbb1abbf6545e9', 'taskId': 'abeb83a56a1c41209430374ec3371746', 'context': '7' }}, { 'name': 'featuresCol', 'taskParameter': { 'id': 'f8427e418d234ae6bd659bb43f67aa1d', 'createBy': '1', 'createDate': '2019-10-31T00:49:40.000+0000', 'updateBy': '1', 'updateDate': '2019-10-31T00:49:40.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '3086af830c24489393e9aa7b704685f5', 'taskId': 'abeb83a56a1c41209430374ec3371746', 'context': '0;1;2;3;4;5;6' }}] }, { 'id': 'b0f2959f5f8f4b73b0656c7c1f34f3d4', 'taskTask': { 'id': 'b0f2959f5f8f4b73b0656c7c1f34f3d4', 'createBy': '1', 'createDate': '2019-10-30T13:11:24.000+0000', 'updateBy': '1', 'updateDate': '2019-10-30T13:11:24.000+0000', 'remarks': null, 'delFlag': '0', 'name': '农作物间的相关性分析', 'description': '农作物间的相关性分析', 'algoId': '37a93fcba469464f852aa3db33567e9d', 'datasetId': '5ffb9647a3c74fd8bc4a0bc60b9fe24b', 'sparkId': '450', 'state': '1', 'result': '/1/fpgrowth/农作物间的相关性分析/1572412281454/resultPath', 'resultModel': '/1/fpgrowth/农作物间的相关性分析/1572412281454/modelPath', 'sparkLog': '[stdout: , \nstderr: ]' }, 'userName': '123', 'datasetName': '年度农作物数据10-18', 'datasetUrl': '/mycode/dataset/年度农作物数据10-18.csv', 'algoName': 'fpgrowth', 'algoUrl': '/mycode/python/fpgrowth.py', 'taskParameterVOList': [{ 'name': null, 'taskParameter': { 'id': '16725a8781d34198b82562dbfa64a856', 'createBy': '1', 'createDate': '2019-10-30T13:11:24.000+0000', 'updateBy': '1', 'updateDate': '2019-10-30T13:11:24.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '7d01ba240588401585f9c56c57892135', 'taskId': 'b0f2959f5f8f4b73b0656c7c1f34f3d4', 'context': '/1/fpgrowth/农作物间的相关性分析/1572412281454/resultPath' }}, { 'name': null, 'taskParameter': { 'id': '583b415431794bce8d7e8531e19a866f', 'createBy': '1', 'createDate': '2019-10-30T13:11:24.000+0000', 'updateBy': '1', 'updateDate': '2019-10-30T13:11:24.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '585981cc396244f4a97f0daef64e8c27', 'taskId': 'b0f2959f5f8f4b73b0656c7c1f34f3d4', 'context': '/1/fpgrowth/农作物间的相关性分析/1572412281454/modelPath' }}] }, { 'id': 'e42f0d29f66b4e37bd2f3e8a044a027e', 'taskTask': { 'id': 'e42f0d29f66b4e37bd2f3e8a044a027e', 'createBy': '1', 'createDate': '2020-05-26T11:58:28.000+0000', 'updateBy': '1', 'updateDate': '2020-05-26T11:58:28.000+0000', 'remarks': null, 'delFlag': '0', 'name': '这是测试用的', 'description': '这是测试用的', 'algoId': '7f9bc12745f24ea990e3cd88236fcd23', 'datasetId': 'c57b42e34e4443568ae680179b8510a9', 'sparkId': '13', 'state': '1', 'result': '/1/PCA/这是测试用的/1590494305628/resultPath', 'resultModel': null, 'sparkLog': '[stdout: , \nstderr: ]' }, 'userName': '123', 'datasetName': '城镇居民家庭基本情况csv', 'datasetUrl': '/mycode/dataset/2017_城镇居民家庭基本情况.csv', 'algoName': 'PCA', 'algoUrl': 'hdfs://namenode:8020/mycode/python/PCA.py', 'taskParameterVOList': [{ 'name': 'resultPath', 'taskParameter': { 'id': 'dfd4fa51042247f7871936676bb54ad5', 'createBy': '1', 'createDate': '2020-05-26T11:58:28.000+0000', 'updateBy': '1', 'updateDate': '2020-05-26T11:58:28.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': '1608784db925494d9dae2d326878b116', 'taskId': 'e42f0d29f66b4e37bd2f3e8a044a027e', 'context': '/1/PCA/这是测试用的/1590494305628/resultPath' }}, { 'name': 'K', 'taskParameter': { 'id': 'f0516ac36e074c5ab9d42aa984502edb', 'createBy': '1', 'createDate': '2020-05-26T11:58:28.000+0000', 'updateBy': '1', 'updateDate': '2020-05-26T11:58:28.000+0000', 'remarks': null, 'delFlag': '0', 'algoParameterId': 'ef6b78c91e2845198ae1d7b4637153b8', 'taskId': 'e42f0d29f66b4e37bd2f3e8a044a027e', 'context': '3' }}] }], 'prePage': 0, 'nextPage': 2, 'isFirstPage': true, 'isLastPage': false, 'hasPreviousPage': false, 'hasNextPage': true, 'navigatePages': 8, 'navigatepageNums': [1, 2, 3, 4, 5, 6, 7, 8], 'navigateFirstPage': 1, 'navigateLastPage': 8, 'firstPage': 1, 'lastPage': 8 }}
    }
  },

  {
    url: '/vue-element-admin/article/detail',
    type: 'get',
    response: config => {
      const { id } = config.query
      for (const article of List) {
        if (article.id === +id) {
          return {
            code: 20000,
            data: article
          }
        }
      }
    }
  },

  {
    url: '/vue-element-admin/article/pv',
    type: 'get',
    response: _ => {
      return {
        code: 20000,
        data: {
          pvData: [
            { key: 'PC', pv: 1024 },
            { key: 'mobile', pv: 1024 },
            { key: 'ios', pv: 1024 },
            { key: 'android', pv: 1024 }
          ]
        }
      }
    }
  },

  {
    url: '/task/task/myList',
    type: 'post',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  },

  {
    url: '/vue-element-admin/article/update',
    type: 'post',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  }
]

