import ACO
import numpy as np
import flet as ft

# 初始化城市數據函數
def InitD(cityNum, coordinate, point):
    return cityNum, coordinate, point

def main(page: ft.Page):
    page.title = "旅行商問題參數輸入"
    
    # 創建輸入框
    city_num_input = ft.TextField(label="城市數量", width=1000)
    coordinate_inputs = []
    point_inputs = []

    coordinates_container = ft.Column()
    points_container = ft.Column()

    def update_inputs(e):
        nonlocal coordinate_inputs, point_inputs
        # 清空舊的輸入框
        coordinates_container.controls.clear()
        points_container.controls.clear()
        coordinate_inputs.clear()
        point_inputs.clear()

        cityNum = int(city_num_input.value)
        
        # 創建城市坐標輸入框
        for i in range(cityNum):
            x_input = ft.TextField(label=f"城市 {i+1} X 坐標", width=100)
            y_input = ft.TextField(label=f"城市 {i+1} Y 坐標", width=100)
            coordinate_inputs.append((x_input, y_input))
            coordinates_container.controls.append(ft.Row([x_input, y_input]))
        
        # 創建距離矩陣輸入框
        for i in range(cityNum):
            row = []
            row_controls = []
            for j in range(cityNum):
                dist_input = ft.TextField(label=f"({i+1},{j+1})", width=80)
                row.append(dist_input)
                row_controls.append(dist_input)
            point_inputs.append(row)
            points_container.controls.append(ft.Row(row_controls))
        
        # 更新界面
        page.update()

    def submit(e):
        cityNum = int(city_num_input.value)
        coordinate = [(float(x.value), float(y.value)) for x, y in coordinate_inputs]
        point = np.zeros((cityNum, cityNum))
        MAX_INT = 1e8
        
        for i in range(cityNum):
            for j in range(cityNum):
                value = point_inputs[i][j].value
                point[i][j] = float(value) if value != "-1" else MAX_INT
        
        # 在這裡可以使用 InitD 函數或進一步處理輸入數據
        cityNum, coordinate, point = InitD(cityNum, coordinate, point)
        
        # 調用 ACO 函數進行計算
        ACO.antColonyOptimization(cityNum, coordinate, point, setting={
            "iter_max": 300,
            "ifOptimanation": False,
            "threshold": 6,
            "skipNum": 20
        })

    page.add(
        city_num_input,
        ft.ElevatedButton(text="生成輸入框", on_click=update_inputs),
        ft.ListView(
            controls=[coordinates_container],
            height=200,
            width=400,
            padding=5,
            spacing=5
        ),
        ft.ListView(
            controls=[points_container],
            height=300,
            width=1000,
            padding=10,
            spacing=10
        ),
        ft.ElevatedButton(text="提交", on_click=submit)
    )

ft.app(target=main)
