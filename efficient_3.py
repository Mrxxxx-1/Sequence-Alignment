'''
Author: Mrx
Date: 2024-05-04 16:39:06
LastEditors: Mrx
LastEditTime: 2024-05-07 22:48:01
FilePath: \Sequence-Alignment\efficient_3.py
Description: 

Copyright (c) 2024 by Mrx, All Rights Reserved. 
'''
import sys
from resource import * 
import time
import psutil
from input_generator import*

gap = 30
mismatch = {"AA":0, "AC":110, "AG": 48, "AT":94, "CA":110, "CC":0, "CG":118, "CT":48, 
            "GA":48, "GC":118, "GG":0, "GT":110, "TA": 94, "TC":48, "TG":110, "TT":0}

'''Your program should print the following information at the respective lines in output file:
1. Cost of the alignment (Integer)
2. First string alignment ( Consists of A, C, T, G, _ (gap) characters)
3. Second string alignment ( Consists of A, C, T, G, _ (gap) characters )
4. Time in Milliseconds (Float)
5. Memory in Kilobytes (Float)'''

def process_memory():
    process = psutil.Process() 
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024) 
    return memory_consumed

def time_wrapper(data): 
    start_time = time.time() 
    efficient(data)
    end_time = time.time()
    time_taken = (end_time - start_time)*1000 
    return time_taken

def efficient(data):
    data_list=[]
    return data_list

def main():
    if len(sys.argv) != 3:
        print("Usage: python input_generator.py input_path output_path")
        return
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    data = input(input_path)
    
    data_list=efficient(data)
    memory=process_memory()
    # print(memory)
    data_list.append(time_wrapper(data))
    data_list.append(memory)
    output(output_path,data_list)

# Call the main function
if __name__ == "__main__":
    main()