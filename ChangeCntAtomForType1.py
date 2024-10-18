def ReplaceCntFileCto1(file_path):

    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for i in range(2, len(lines)):  
        parts = lines[i].split()  
        if parts and parts[0] == 'C':  
            parts[0] = '1'  # Replace 'c' to '1'
        lines[i] = ' '.join(parts) + '\n'  
    
    with open(file_path, 'w') as file:
        file.writelines(lines)
    
    print("文件修改成功！")
    
    
file_path = r"./CNT_L.lmp"
file_path = r"./CNT_Z.lmp"
file_path = r"./CNT_H.lmp"

ReplaceCntFileCto1(file_path)