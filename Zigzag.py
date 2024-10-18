# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 15:46:12 2024

@author: Administrator
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import csv
# 全局参数
num_balls = 6  # 小球数量
d_ball = 6.8964+3.4  # 小球之间的球心距离（小球有效直径）
delta_x=6.8

# =============================================================================
d_tube = 8.689859892817484*2
delta_dzigzag=d_tube-delta_x
print(d_tube)
print(delta_dzigzag)
#delta_x = d_tube - d_ball
delta_z = np.sqrt(d_ball**2 - delta_x**2)
# =============================================================================

# 初始化小球位置数组
x_positions = []
y_positions = []
z_positions = []

# 初始位置
x, y, z = 0, 0, 0

# 构造zigzag结构
for i in range(num_balls):
    if i % 2 == 0:
        # 偶数索引的小球（在x方向的偏移）
        x = - delta_x/2
        y = 0
    else:
        # 奇数索引的小球
        x =  delta_x/2
        y = 0  # y方向保持为0，形成二维平面上的zigzag结构

    z = i * delta_z  # z方向逐渐增加
    
    x_positions.append(x)
    y_positions.append(y)
    z_positions.append(z)

# 将列表转换为数组
x = np.array(x_positions)
y = np.array(y_positions)
z = np.array(z_positions)

# 绘制zigzag结构
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制小球
#ax.scatter(x, y, z, s=500, c=['green' if i % 2 == 0 else 'red' for i in range(num_balls)], label='Zigzag Balls') #需区分颜色
ax.scatter(x, y, z, s=500, c=['green' if i % 2 == 0 else 'green' for i in range(num_balls)], label='Zigzag Balls')  #无需区分颜色

# 绘制线条连接球心
ax.plot(x, y, z, label='zigzag', color='black')

# 设置轴标签
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 坐标轴设置
ax.set_xlim([np.min(x)-10, np.max(x)+10])
ax.set_ylim([np.min(x)-10, np.max(x)+10])  # 因为 y 坐标保持为 0，所以范围较小
ax.set_zlim([np.min(z)-10, np.max(z)+10])
ax.set_box_aspect([1, 1, 1])  # 坐标轴各个方向比例1:1:1

# 添加图例
ax.legend()

# 显示图像
plt.show()

# 小球中心坐标列表
new_centers = np.column_stack((x, y, z)).tolist()

# 读取单个小球的原子坐标函数
def read_coordinates_from_csv(file_path):
    coordinates = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            coordinates.append([float(row[0]), float(row[1]), float(row[2])])
    return np.array(coordinates)

# 移动小球位置的函数
def shift_coordinates(coordinates, old_center, new_center):
    return coordinates - old_center + new_center

# 保存新的小球坐标到txt文件
def save_coordinates_to_txt(file_path, coordinates):
    np.savetxt(file_path, coordinates, fmt='%.6f', comments='')

# 合并多个txt文件到lmp文件，并在适当位置插入补充内容
def merge_files(output_dir, all_file_name, num_files, num_atoms):
    with open(all_file_name, 'w') as outfile:
        # 添加原子数目在第一行
        outfile.write(f"{num_atoms}\n")
        # 在第二行添加补充内容
        outfile.write("C60 ATOM\n")
        
        for i in range(num_files):
            input_file = os.path.join(output_dir, f"shifted_model_{i+1}.txt")
            column_value = "2" if (i+1) % 2 != 0 else "3"  # 无需奇偶判断
            #column_value = "2"  # 无需奇偶判断
            try:
                with open(input_file, 'r') as infile:
                    for line in infile:
                        if line.strip():  # 跳过空行
                            outfile.write(f"{column_value} {line}")
            except FileNotFoundError:
                print(f"文件 {input_file} 未找到，跳过该文件。")
    print(f"所有文件已合并到: {all_file_name}")

# 文件路径
file_path = "./C60.csv"  # 单个小球的原始坐标
output_file_dir = "./output_Zigzag/"
os.makedirs(output_file_dir, exist_ok=True)

# 读取原子坐标
coordinates = read_coordinates_from_csv(file_path)
old_center = np.mean(coordinates, axis=0)

# 保存每个小球的坐标
for idx, new_center in enumerate(new_centers):
    coordinates_shifted = shift_coordinates(coordinates, old_center, new_center)
    output_file_name = os.path.join(output_file_dir, f"shifted_model_{idx + 1}.txt")
    save_coordinates_to_txt(output_file_name, coordinates_shifted)

# 假设每个小球有60个原子，计算总原子数
num_atoms = num_balls * len(coordinates)

# 合并文件并生成zigzag.lmp
zigzag_lmp_file = "Zigzag.lmp"
merge_files(output_file_dir, zigzag_lmp_file, num_balls, num_atoms)

print("Zigzag模型已合并并保存到文件Zigzag.lmp")
