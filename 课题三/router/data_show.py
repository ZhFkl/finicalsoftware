import csv
import pdb
import json
from fastapi import APIRouter

data_show = APIRouter(prefix="/data_show")

node_labels_filename = "data/partners_node_labels.csv"
hypergraph_filename = "data/hypergraph.txt"

def get_dict():
    data = {}
    with open(node_labels_filename, encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        # header = next(csv_reader)        # 读取第一行每一列的标题
        for row in csv_reader:  # 将csv 文件中的数据保存到data中
            name = row[0]
            id = row[1]
            type = row[3]
            data[id] = {
                "name": name,
                "type": type
            }
    return data

@data_show.get('/')
def get_data():
    dict = get_dict()
    f = open(hypergraph_filename)  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    result = {}
    num = 0
    while line:
        num+=1
        data = line.split(",")
        if (len(data) > 6):
            start_time = data[0]
            end_time = data[1]
            company_id = data[2].strip()
            hold_partner = []
            for i in range(3, len(data)-1):
                hold_partner.append(data[i].strip())
            res = {
                "start_time": start_time.strip(),
                "end_time": end_time.strip(),
            }
            # pdb.set_trace()
            for item in hold_partner:
                res[dict[item]["name"]] = {"type": dict[item]["type"]}
            if (int(company_id) < 1800000 and len(dict[company_id]["name"]) > 8):
                result[dict[company_id]["name"]] = res
        line = f.readline()
    f.close()
    # pdb.set_trace()
    # print(len(result))
    result2 = {}
    mp = {}
    for key in result:
        value = result[key]
        for k in value:
            if k != 'start_time' and k != 'end_time' and k in mp:
                # print("people: ", k)
                result2[mp[k]] = result[mp[k]]
                result2[key] = result[key]
            elif len(value) > 10:
                result2[key] = result[key]
            mp[k] = key
        # print(key, result[key])
        # break
    print("data show success, len(result2): ", len(result2))
    # print(result2)
    # with open("data.json", "w", encoding='utf-8') as f:
    #     json.dump(result2, f, indent=4, ensure_ascii=False)
    return result2


@data_show.get('/new')
def get_new_data():
    return json.load(open('data/task2/data_show2.json', 'r', encoding='utf-8'))

@data_show.get('/new2')
def get_new_data2():
    return json.load(open('data/task2/data_show3.json', 'r', encoding='utf-8'))

if __name__ == '__main__':
    get_data()


