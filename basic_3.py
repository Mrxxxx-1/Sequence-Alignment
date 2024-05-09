'''
Author: Mrx
Date: 2024-05-04 16:38:36
LastEditors: Mrx
LastEditTime: 2024-05-08 22:48:05
FilePath: \Sequence-Alignment\basic_3.py
Description: 

Copyright (c) 2024 by Mrx, All Rights Reserved. 
'''
import sys
import time
import psutil

gap = 30
mismatch = {"AA":0, "AC":110, "AG": 48, "AT":94, "CA":110, "CC":0, "CG":118, "CT":48, 
            "GA":48, "GC":118, "GG":0, "GT":110, "TA": 94, "TC":48, "TG":110, "TT":0}
infinity = 23600

'''Your program should print the following information at the respective lines in output file:
1. Cost of the alignment (Integer)
2. First string alignment ( Consists of A, C, T, G, _ (gap) characters)
3. Second string alignment ( Consists of A, C, T, G, _ (gap) characters )
4. Time in Milliseconds (Float)
5. Memory in Kilobytes (Float)'''
def input(input_path):
    try:
        with open(input_path, 'r') as input_file:
                lines = input_file.readlines()
                lines = [line.rstrip('\n') for line in lines]
                # print(lines)
                t0 = []
                t1 = []
                # Find the index of the first occurrence of a non-numeric string
                index = next((i for i, x in enumerate(lines[1:]) if not x.isdigit()), None)
                index += 1
                if index is not None:
                    t0 = lines[:index]
                    t1 = lines[index:]
                # print(index)
                # print(t0)
                data = []
                data.append(generator(t0))
                data.append(generator(t1))
                return data
    except FileNotFoundError:
        print("File not found. Please make sure the input path is correct.")
def generator(list):
    s = list[0]
    for item in list[1:]:
        index = int(item) + 1
        s = s[:index] + s + s[index:]
    return s

def output(output_path,data_list):
    try:
        with open(output_path, 'w') as output_file:
            for line in data_list:
                output_file.write(str(line)+'\n')
    except FileNotFoundError:
        print("Path not found.Please make sure the output path is correct.")
def process_memory():
    process = psutil.Process() 
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024) 
    return memory_consumed


def basic(data):
    m = len(data[0])
    n = len(data[1])

    array = [[infinity for _ in range(n+1)] for _ in range(m+1)]
    
    # Setting values for [0][k] and [k][0]
    for k in range(n+1):
        array[0][k] = k * gap
    
    for k in range(m+1):
        array[k][0] = k * gap
    for i in range(1,m+1):
        for j in range(1,n+1):
            ms = data[0][i-1] + data[1][j-1]
            array[i][j] = min((array[i-1][j-1]+mismatch[ms]), 
                              (array[i-1][j]+gap), (array[i][j-1])+gap )
    # print(array[m][n])
    alignment_data_0 = ''
    alignment_data_1 = ''
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and array[i][j] == array[i-1][j-1] + mismatch[data[0][i-1] + data[1][j-1]]:
            alignment_data_0 = data[0][i-1] + alignment_data_0
            alignment_data_1 = data[1][j-1] + alignment_data_1
            i -= 1
            j -= 1
        elif i > 0 and array[i][j] == array[i-1][j] + gap:
            alignment_data_0 = data[0][i-1] + alignment_data_0
            alignment_data_1 = '_' + alignment_data_1
            i -= 1
        else:
            alignment_data_0 = '_' + alignment_data_0
            alignment_data_1 = data[1][j-1] + alignment_data_1
            j -= 1

    # print("Alignment of data[0]:", alignment_data_0)
    # print("Alignment of data[1]:", alignment_data_1)
    data_list=[]
    data_list.append(array[m][n])
    data_list.append(alignment_data_0)
    data_list.append(alignment_data_1)
    return data_list
    # print(array)
    # print(len(array))

def main():
    start_time = time.time()
    if len(sys.argv) != 3:
        print("Usage: python input_generator.py input_path output_path")
        return
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    data = input(input_path)

 
    data_list=basic(data)
    end_time = time.time()
    time_taken = (end_time - start_time)*1000 
    
    memory=process_memory()
    
    data_list.append(time_taken)
    data_list.append(memory)
    
    output(output_path,data_list)

# Call the main function
if __name__ == "__main__":
    main()