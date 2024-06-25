import matplotlib.pyplot as plt
import networkx as nx
from prettytable import PrettyTable

# 打印旅行商問題的運行結果表格

def createTable(table_obj):
    """
    打印數據表格
    :param table_obj: 表格對象 obj
    :return: none
    參數示例:
    result_obj = {
        "header": ["TSP參數", "運行結果"],
        "body": [
            ["城市數量", cityNum],
            ["最短路程", distance],
            ["運行時間", time_str],
            ["最小路徑", path_str]
        ],
        # name的值要和header一致, l: 左對齊 c: 居中 r: 右對齊
        "align": [
            { "name": "TSP參數", "method": "l" },
            { "name": "運行結果", "method": "l" }
        ],
        "setting": {
            "border": True, # 默認True
            "header": True, # 默認True
            "padding_width": 5 # 空白寬度
        }
    }
    """
    pt = PrettyTable()
    for key in table_obj:
        # 打印表頭
        if key == "header":
            pt.field_names = table_obj[key]
        # 打印表格數據
        elif key == "body":
            for i in range(len(table_obj[key])):
                pt.add_row(table_obj[key][i])
        # 表格參數的對齊方式
        elif key == "align":
            for i in range(len(table_obj[key])): 
                pt.align[table_obj[key][i]["name"]] = table_obj[key][i]["method"]
        # 表格其他設置
        elif key == "setting":
            for key1 in table_obj[key]:
                if key1 == "border":
                    pt.border = table_obj[key][key1]
                elif key1 == "header":
                    pt.header = table_obj[key][key1]
                elif key1 == "padding_width":
                    pt.padding_width = table_obj[key][key1]
    print(pt)

# 存活
def timeFormat(number):
    """
    時間格式保持兩位
    :param number: 數字 int
    :return: 兩位的數字字符 str
    """
    if number < 10:
        return "0" + str(number)
    else:
        return str(number)

def calcTime(time):
    """
    將毫秒根據數值大小轉為合適的單位
    :param time: 數字 double
    :return: 時間字符串 str
    """
    count = 0
    while time < 1:
        if count == 3:
            break
        else:
            count += 1
        time *= 1000
    if count == 0:
        hour = int(time // 3600)
        minute = int(time % 3600 // 60)
        second = time % 60
        if hour > 0: return timeFormat(hour) + "時" + timeFormat(minute) + "分" + timeFormat(int(second)) + "秒"
        if minute > 0: return timeFormat(minute) + "分" + timeFormat(int(second)) + "秒"
        if second > 0: return str(round(time, 3)) + "秒"
    elif count == 1:
        return str(round(time, 3)) + "毫秒"
    elif count == 2:
        return str(round(time, 3)) + "微秒"
    elif count == 3:
        return str(round(time, 3)) + "納秒"

# 存活
def pathToString(path, everyRowNum):
    """
    將最優路徑列表轉為字符串
    :param path: 最優路徑列表 list
    :param everyRowNum: 每行打印的路徑數, 除去頭尾 int
    :return: 路徑字符串 str
    """
    min_path_str = ""
    for i in range(len(path)):
        min_path_str += str(path[i] + 1) + ("\n--> " if i != 0 and i % everyRowNum == 0 else " --> ")
    min_path_str += "1"  # 單獨輸出起點編號
    return min_path_str

# 打印表格
def printTable(path, everyRowNum, runTime, cityNum, distance):
    """
    將最優路徑列表轉為字符串
    :param path: 最優路徑列表 list
    :param everyRowNum: 每行打印的路徑數, 除去頭尾 int
    :param runTime: 程序運行時間 double
    :param cityNum: 城市數量 int
    :param distance: 最優距離 double
    :return: none
    """
    path_str = pathToString(path, everyRowNum)
    time_str = calcTime(runTime)  # 程序耗時
    # 打印的表格對象
    result_obj = {
        "header": ["TSP參數", "運行結果"],
        "body": [
            ["城市數量", cityNum],
            ["最短路程", distance],  # 最小值就在第一行最後一個
            ["運行時間", time_str],  # 計算程序執行時間
            ["最小路徑", path_str]  # 輸出路徑
        ],
        "align": [
            {"name": "TSP參數", "method": "l"},
            {"name": "運行結果", "method": "l"}
        ],
    }
    createTable(result_obj)  # 打印結果

###########################################################################
# 繪圖函數

def isPath(path, i, j):
    """
    判斷邊是否為最小路徑
    :param path: 最優路徑列表 list
    :param i: 路徑的下標 int
    :param j: 路徑的下標 int
    :return: 布爾值
    """
    idx = path.index(i)
    pre_idx = idx - 1 if idx - 1 >= 0 else len(path) - 1
    next_idx = idx + 1 if idx + 1 < len(path) else 0
    if j == path[pre_idx] or j == path[next_idx]:
        return True
    return False

def drawNetwork(coordinate, point, path, inf, *args):
    """
    畫出網絡圖
    :param coordinate: 城市坐標 list
    :param point: 城市距離矩陣 ndarray
    :param path: 最優路徑 list
    :param inf: 無窮大值 double
    :return: none
    """
    G_min = nx.Graph()  # 最短路徑解
    G = nx.Graph()  # 城市路徑圖
    edges = []
    for i in range(len(coordinate)):
        m = i + 1
        G_min.add_node(m, pos=coordinate[i])  # 添加節點
        G.add_node(m, pos=coordinate[i])
        for j in range(i + 1, len(coordinate)):
            if point[i][j] != inf:
                if isPath(path, i, j):
                    G_min.add_edge(i + 1, j + 1, weight=int(point[i][j]), color='r')
                G.add_edge(i + 1, j + 1, weight=int(point[i][j]))
    tmp_edges = nx.get_edge_attributes(G_min, 'color')
    for key in tmp_edges:
        edges.append(tmp_edges[key])
    pos = pos_min = nx.get_node_attributes(G_min, 'pos')
    labels = nx.get_edge_attributes(G_min, 'weight')
    label = nx.get_edge_attributes(G, 'weight')
    # 城市所有路徑
    plt.subplot(121)
    plt.title("TSP City Network")
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='y')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=label)  # 畫路徑長度
    # 最短路徑解
    plt.subplot(122)
    plt.title("Solution Of Ant Colony Algorithm")
    nx.draw(G_min, pos_min, with_labels=True, font_weight='bold', node_color='g', edge_color=edges)
    nx.draw_networkx_edge_labels(G_min, pos_min, edge_labels=labels)  # 畫路徑長度
    plt.show()
