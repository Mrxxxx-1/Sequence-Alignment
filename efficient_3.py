'''
Author: Mrx
Date: 2024-05-04 16:39:06
LastEditors: Mrx
LastEditTime: 2024-05-08 23:41:49
FilePath: \Sequence-Alignment\efficient_3.py
Description: 

Copyright (c) 2024 by Mrx, All Rights Reserved. 
'''
import sys
import time
import psutil

gap = 30
infinity = float("inf")
mismatch = {"AA":0, "AC":110, "AG": 48, "AT":94, "CA":110, "CC":0, "CG":118, "CT":48, 
            "GA":48, "GC":118, "GG":0, "GT":110, "TA": 94, "TC":48, "TG":110, "TT":0}

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

def eff_bottom_up(str_1, str_2):
    # Initialize the OPT matrix
    m = len(str_1) + 1
    n = len(str_2) + 1
    OPT = [0 for _ in range(m)]

    # Initialize first column
    for i in range(m):
        OPT[i] = i * gap

    # Bottom-up pass
    for j in range(1, n):
        temp_OPT = [0 for _ in range(m)]
        temp_OPT[0] = j * gap
        for i in range(1, m):
            gap_1 = temp_OPT[i - 1] + gap  
            gap_2 = OPT[i] + gap 
            # Match/Mismatch
            alpha = OPT[i - 1] + mismatch[str_1[i - 1]+str_2[j - 1]]
            temp_OPT[i] = min(gap_1, gap_2, alpha)

        OPT = temp_OPT

    return OPT


def divide(cost, str_1, str_2, ):
    # General cases for DnC
    if not (len(str_1) <= 2 or len(str_2) <= 2):
        # Divide str_2 by half
        idx = len(str_2) // 2
        str_2_l = str_2[:idx]
        str_2_r = str_2[idx:]

        # Find OPT arrays for left and right strings
        OPT_left = eff_bottom_up(str_1, str_2_l)
        OPT_right = eff_bottom_up(str_1[::-1], str_2_r[::-1])[::-1]

        # Initialize min optimal value and index
        min_idx = None
        min_cost = infinity

        # Find the optimal split
        for idx in range(len(OPT_right)):
            opt_cost = OPT_left[idx] + OPT_right[idx]
            if opt_cost < min_cost:
                min_cost = opt_cost
                min_idx = idx

        # Dive str_1 into 2 according to min idx
        str_1_l = str_1[:min_idx]
        str_1_r = str_1[min_idx:]

        # Recursive call to the divide function for left and right strings
        opt_cost_l, str_1_l_opt, str_2_l_opt= divide(
            cost, str_1_l, str_2_l
        )
        opt_cost_r, str_1_r_opt, str_2_r_opt= divide(
            cost, str_1_r, str_2_r
        )

        str_1_opt = str_1_l_opt + str_1_r_opt
        str_2_opt = str_2_l_opt + str_2_r_opt
        opt_cost = opt_cost_l + opt_cost_r

        return [opt_cost, str_1_opt, str_2_opt]

    # Base case for DnC
    else:
        return basic([str_1, str_2])


def main():
    if len(sys.argv) != 3:
        print("Usage: python input_generator.py input_path output_path")
        return
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    data = input(input_path)

    start_time = time.time() 
    data_list=divide(3,data[0],data[1])
    end_time = time.time()
    time_taken = (end_time - start_time)*1000 
    
    memory=process_memory()
    
    data_list.append(time_taken)
    data_list.append(memory)
    
    output(output_path,data_list)

# Call the main function
if __name__ == "__main__":
    main()