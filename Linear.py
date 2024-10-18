# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 10:31:39 2024

@author: Administrator
"""

import numpy as np
import os
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
import csv

# Global parameters
num_balls = 4  # Number of balls
d_ball = 6.8964+3.4  # dc60=6.8964,d_vdw=3.4)
d_tube = 2 * 6.684507609859605  # Diameter of the nanotube(10,10)
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
def read_coordinates_from_csv(file_path):
    coordinates = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            coordinates.append([float(row[0]), float(row[1]), float(row[2])])
    return np.array(coordinates)

# Function to shift the ball positions
def shift_coordinates(coordinates, old_center, new_center):
    return coordinates - old_center + new_center

# Function to save the new ball coordinates to a txt file
def save_coordinates_to_txt(file_path, coordinates):
    np.savetxt(file_path, coordinates, fmt='%.6f', comments='')

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
file_path = "./C60.csv"  # Original coordinates of a single ball
output_file_dir = "./output_Linear/"
os.makedirs(output_file_dir, exist_ok=True)

# Read atomic coordinates
coordinates = read_coordinates_from_csv(file_path)
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