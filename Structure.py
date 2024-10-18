# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 18:12:17 2024

@author: Administrator

"""

import numpy as np
import os
import matplotlib.pyplot as plt
import csv

def LinearStructure(c60_file_path):
    num_balls = 4  # Number of balls
    d_ball = 6.8964+3.4  # dc60=6.8964,d_vdw=3.4)
    #d_tube = 2 * 6.684507609859605  # Diameter of the nanotube(10,10)
    delta_z = d_ball
    
    # Initialize arrays for ball positions
    x_positions = []
    y_positions = []
    z_positions = []
    
    # Initial position
    x, y, z = 0, 0, 0
    
    # Construct zigzag structure
    for i in range(num_balls):
        x = 0
        y = 0  
        z = i * delta_z
        
        x_positions.append(x)
        y_positions.append(y)
        z_positions.append(z)
    
    # Convert lists to arrays
    x = np.array(x_positions)
    y = np.array(y_positions)
    z = np.array(z_positions)
    
    # Plot the zigzag structure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the balls
    # ax.scatter(x, y, z, s=500, c=['green' if i % 2 == 0 else 'red' for i in range(num_balls)], label='Zigzag Balls') # Distinguish colors
    ax.scatter(x, y, z, s=500, c=['red' if i % 2 == 0 else 'red' for i in range(num_balls)], label='Linear Chain')  # No need to distinguish colors
    
    # Draw lines connecting the centers of the balls
    ax.plot(x, y, z, label='Linear', color='black')
    
    # Set axis labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Set axis limits
    ax.set_xlim([np.min(x)-10, np.max(x)+10])
    ax.set_ylim([np.min(x)-10, np.max(x)+10])  # Since the y-coordinate remains 0, the range is small
    ax.set_zlim([np.min(z)-10, np.max(z)+10])
    ax.set_box_aspect([1, 1, 1])  # Keep aspect ratio 1:1:1 for all axes
    
    # Add legend
    ax.legend()
    
    # Show plot
    plt.show()
    
    # List of ball center coordinates
    new_centers = np.column_stack((x, y, z)).tolist()
    
    # Function to read the atomic coordinates of a single ball from a CSV file
    def read_coordinates_from_csv(c60_file_path):
        coordinates = []
        with open(c60_file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                coordinates.append([float(row[0]), float(row[1]), float(row[2])])
        return np.array(coordinates)
    
    # Function to shift the ball positions
    def shift_coordinates(coordinates, old_center, new_center):
        return coordinates - old_center + new_center
    
    # Function to save the new ball coordinates to a txt file
    def save_coordinates_to_txt(c60_file_path, coordinates):
        np.savetxt(c60_file_path, coordinates, fmt='%.6f', comments='')
    
    # Function to merge multiple txt files into a lmp file, with supplementary content inserted at the appropriate position
    def merge_files(output_dir, all_file_name, num_files, num_atoms):
        with open(all_file_name, 'w') as outfile:
            # Add the number of atoms on the first line
            outfile.write(f"{num_atoms}\n")
            # Add supplementary content on the second line
            outfile.write("C60 ATOM\n")
            
            for i in range(num_files):
                input_file = os.path.join(output_dir, f"shifted_model_{i+1}.txt")
                # column_value = "C1" if (i+1) % 2 != 0 else "C2"  # No need to distinguish between odd and even
                column_value = "2" 
                #if (i+1) % 2 != 0 else "C1"  # No need to distinguish
                try:
                    with open(input_file, 'r') as infile:
                        for line in infile:
                            if line.strip():  # Skip empty lines
                                outfile.write(f"{column_value} {line}")
                except FileNotFoundError:
                    print(f"File {input_file} not found, skipping this file.")
        print(f"All files merged into: {all_file_name}")
    
    # File paths
    
    output_file_dir = "./output_Linear/"
    os.makedirs(output_file_dir, exist_ok=True)
    
    # Read atomic coordinates
    coordinates = read_coordinates_from_csv(c60_file_path)
    old_center = np.mean(coordinates, axis=0)
    
    # Save the coordinates for each ball
    for idx, new_center in enumerate(new_centers):
        coordinates_shifted = shift_coordinates(coordinates, old_center, new_center)
        output_file_name = os.path.join(output_file_dir, f"shifted_model_{idx + 1}.txt")
        save_coordinates_to_txt(output_file_name, coordinates_shifted)
    
    # Assume each ball has 60 atoms, calculate the total number of atoms
    num_atoms = num_balls * len(coordinates)
    
    # Merge the files and generate the linear structure lmp file
    linear_lmp_file = "Linear.lmp"
    merge_files(output_file_dir, linear_lmp_file, num_balls, num_atoms)
    
    print("Linear model merged and saved to file Linear.lmp")


def ZigzagStructure(c60_file_path):

    num_balls = 6  
    d_ball = 6.8964+3.4  
    delta_x=6.8
    # =============================================================================
# =============================================================================
#     d_tube = 8.689859892817484*2(13,13)
#     delta_dzigzag=d_tube-delta_x
#     print(d_tube)
#     print(delta_dzigzag)
# =============================================================================
    #delta_x = d_tube - d_ball
    delta_z = np.sqrt(d_ball**2 - delta_x**2)
    # =============================================================================
    x_positions = []
    y_positions = []
    z_positions = []

    x, y, z = 0, 0, 0

    for i in range(num_balls):
        if i % 2 == 0:
            x = - delta_x/2
            y = 0
        else:

            x =  delta_x/2
            y = 0

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
    def read_coordinates_from_csv(c60_file_path):
        coordinates = []
        with open(c60_file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                coordinates.append([float(row[0]), float(row[1]), float(row[2])])
        return np.array(coordinates)

    # 移动小球位置的函数
    def shift_coordinates(coordinates, old_center, new_center):
        return coordinates - old_center + new_center

    # 保存新的小球坐标到txt文件
    def save_coordinates_to_txt(c60_file_path, coordinates):
        np.savetxt(c60_file_path, coordinates, fmt='%.6f', comments='')

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

    output_file_dir = "./output_Zigzag/"
    os.makedirs(output_file_dir, exist_ok=True)

    # read the c60 atom corrdinates
    coordinates = read_coordinates_from_csv(c60_file_path)
    old_center = np.mean(coordinates, axis=0)

    # save corrdinates of every ball
    for idx, new_center in enumerate(new_centers):
        coordinates_shifted = shift_coordinates(coordinates, old_center, new_center)
        output_file_name = os.path.join(output_file_dir, f"shifted_model_{idx + 1}.txt")
        save_coordinates_to_txt(output_file_name, coordinates_shifted)

    # total c60 atom number
    num_atoms = num_balls * len(coordinates)

    # merge file to Zigzag.lmp
    zigzag_lmp_file = "Zigzag.lmp"
    merge_files(output_file_dir, zigzag_lmp_file, num_balls, num_atoms)

    print("Zigzag模型已合并并保存到文件Zigzag.lmp")
    
    
def HelixStructure(c60_file_path):
    
    D = 1.96  # 直径比,1.866<D<1.9897
    num_balls = 10 # 10为周期性最小的个数
    d = 6.8964+3.4  # 小球直径
    #d_tube = 2 * 11.363662936761326  # Diameter of the nanotube(17,17)
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
    
    output_file_dir = "./output_Helix/"  # 输出文件目录，保存全部原子坐标

    # 创建输出目录（如果不存在）
    os.makedirs(output_file_dir, exist_ok=True)

    # 小球的中心坐标
    bottom_center = np.array([0, 0, 0])
    ball_centers = np.column_stack((x, y, z)) + bottom_center

    # 将小球的中心坐标转换为列表
    new_centers = [np.array(center) for center in ball_centers.tolist()]

    # 从CSV文件中读取原子坐标
    def read_coordinates_from_csv(c60_file_path):
        coordinates = []
        try:
            with open(c60_file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    coordinates.append([float(row[0]), float(row[1]), float(row[2])])
        except FileNotFoundError:
            print(f"文件 {c60_file_path} 未找到。")
        return np.array(coordinates)

    # 移动球的位置
    def shift_coordinates(coordinates, old_center, new_center):
        return coordinates - old_center + new_center

    # 保存坐标到txt文件
    def save_coordinates_to_txt(file_path, coordinates):
        np.savetxt(file_path, coordinates, fmt='%.6f', comments='')

    # 读取原子坐标
    coordinates = read_coordinates_from_csv(c60_file_path)

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


c60_file_path='C60.csv'

#LinearStructure(c60_file_path)
#ZigzagStructure(c60_file_path)
#HelixStructure(c60_file_path)