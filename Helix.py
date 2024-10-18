# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:42:28 2024

@author: Administrator
"""

import numpy as np
import os
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
import csv


# 全局参数
D = 1.96  # 直径比,1.866<D<1.9897
num_balls = 10 # 10为周期性最小的个数
d = 6.8964+3.4  # 小球直径
d_prime = D * d - d  # 螺旋线直径
R = d_prime / 2  # 螺旋线半径
print(d_prime)
# 螺旋线参数
delta_phi = np.arccos(1 - (np.sqrt(3) / (D - 1)))  # 旋转角
delta_z = np.sqrt(1 - (np.sqrt(3) * (D - 1) / 2))  # 归一化间隔
Delta_Z = d * delta_z  # 实际间隔
t = np.arange(num_balls) * delta_phi  # 小球平面位置

# 螺旋线方程
x = R * np.cos(t)
y = R * np.sin(t)
z = Delta_Z * np.arange(num_balls)

# 绘制螺旋线和小球
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, s=500)
ax.plot(x, y, z, label='helix')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 坐标轴设置
ax.set_xlim(-50, 50)
ax.set_ylim(-50, 50)
ax.set_box_aspect([1, 1, 1])  # 坐标轴各个方向比例1:1:1
plt.show()

# 处理小球坐标
# 文件目录
file_path = "./C60.csv"  # 输入文件目录，单个小球原始坐标，包含60个原子
output_file_dir = "./output_Helix/"  # 输出文件目录，保存全部原子坐标

# 创建输出目录（如果不存在）
os.makedirs(output_file_dir, exist_ok=True)

# 小球的中心坐标
bottom_center = np.array([0, 0, 0])
ball_centers = np.column_stack((x, y, z)) + bottom_center

# 将小球的中心坐标转换为列表
new_centers = [np.array(center) for center in ball_centers.tolist()]

# 从CSV文件中读取原子坐标
def read_coordinates_from_csv(file_path):
    coordinates = []
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                coordinates.append([float(row[0]), float(row[1]), float(row[2])])
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
    return np.array(coordinates)

# 移动球的位置
def shift_coordinates(coordinates, old_center, new_center):
    return coordinates - old_center + new_center

# 保存坐标到txt文件
def save_coordinates_to_txt(file_path, coordinates):
    np.savetxt(file_path, coordinates, fmt='%.6f', comments='')

# 读取原子坐标
coordinates = read_coordinates_from_csv(file_path)

# 计算球心坐标
old_center = np.mean(coordinates, axis=0)

# 遍历每个新球心坐标，计算新的原子坐标并保存
for idx, new_center in enumerate(new_centers):
    # 移动球的位置
    coordinates_shifted = shift_coordinates(coordinates, old_center, new_center)

    # 构建输出文件名
    output_file_name = os.path.join(output_file_dir, f"shifted_model_{idx + 1}.txt")

    # 保存移动后的模型到txt文件
    save_coordinates_to_txt(output_file_name, coordinates_shifted)

# 合并文件并生成lmp模型
all_file = "Helix.lmp"  # 合并后的文件名

# 合并多个TXT文件的内容到一个文件中，并删除空行和添加第一列
def merge_files(output_dir, all_file_name, num_files):
    with open(all_file_name, 'w') as outfile:
        # 写入原子数目
        outfile.write(f"{num_files * 60}\n")  # 假设每个小球对应60个原子
        # 在写入原子数目之后，写入定义内容
        outfile.write("C60 ATOM\n")
        
        for i in range(num_files):
            input_file = os.path.join(output_dir, f"shifted_model_{i + 1}.txt")
            #column_value = "C1" if (i + 1) % 2 != 0 else "C2"  # 判断奇偶数，如需区分两个链条颜色
            column_value = "2" if (i + 1) % 2 != 0 else "3"  # 判断奇偶数，不区分两个链条颜色
            try:
                with open(input_file, 'r') as infile:
                    for line in infile:
                        if line.strip():  # 跳过空行
                            outfile.write(f"{column_value} {line}")
            except FileNotFoundError:
                print(f"文件 {input_file} 未找到，跳过该文件。")

    print(f"所有文件已合并到: {all_file_name}")

# 合并文件
merge_files(output_file_dir, all_file, num_balls)
