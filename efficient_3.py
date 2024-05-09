'''
Author: Mrx
Date: 2024-05-04 16:39:06
LastEditors: Mrx
LastEditTime: 2024-05-08 22:48:40
FilePath: \Sequence-Alignment\efficient_3.py
Description: 

Copyright (c) 2024 by Mrx, All Rights Reserved. 
'''
import sys
import time
import psutil

gap = 30

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

def efficient(data):
    m = len(data[0])
    n = len(data[1])
    def divide_and_conquer_helper(X, Y):
        m = len(X)
        n = len(Y)

        if m == 0:
            return n * gap, '', '_' * n
        elif n == 0:
            return m * gap, '_' * m, ''

        # Split X into halves
        mid = m // 2
        Xl = X[:mid]
        Xr = X[mid:]

        # Compute the optimal split point in Y
        min_cost = float('inf')
        split_point = 0
        for k in range(n+1):
            cost_left, _, _ = divide_and_conquer_helper(Xr, Y[:k])
            cost_right, _, _ = divide_and_conquer_helper(Xl, Y[k:])
            total_cost = cost_left + cost_right
            if total_cost < min_cost:
                min_cost = total_cost
                split_point = k

        # Compute the optimal alignments for Xl and Xr with respect to Y
        cost_left, align_left_X, align_left_Y = divide_and_conquer_helper(Xl, Y[:split_point])
        cost_right, align_right_X, align_right_Y = divide_and_conquer_helper(Xr, Y[split_point:])

        # Combine alignments
        total_cost = cost_left + cost_right
        alignment_X = align_left_X + align_right_X
        alignment_Y = align_left_Y + align_right_Y

        return total_cost, alignment_X, alignment_Y

    # Invoke helper function
    total_cost, alignment_X, alignment_Y = divide_and_conquer_helper(data[0], data[1])

    return [total_cost, alignment_X, alignment_Y]


def main():
    if len(sys.argv) != 3:
        print("Usage: python input_generator.py input_path output_path")
        return
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    data = input(input_path)
    data_list=efficient(data)
    print(data_list)
    # start_time = time.time() 
    # data_list=efficient(data)
    # end_time = time.time()
    # time_taken = (end_time - start_time)*1000 
    
    # memory=process_memory()
    
    # data_list.append(time_taken)
    # data_list.append(memory)
    
    # output(output_path,data_list)

# Call the main function
if __name__ == "__main__":
    main()