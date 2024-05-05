'''
Author: Mrx
Date: 2024-05-04 16:59:54
LastEditors: Mrx
LastEditTime: 2024-05-04 19:00:16
FilePath: \Sequence-Alignment\input_generator.py
Description: 

Copyright (c) 2024 by Mrx, All Rights Reserved. 
'''
import sys

def input(input_path):
    try:
        with open(input_path, 'r') as input_file:
                lines = input_file.readlines()
                lines = [line.rstrip('\n') for line in lines]
                print(lines)
                t0 = []
                t1 = []
                # Find the index of the first occurrence of a non-numeric string
                index = next((i for i, x in enumerate(lines[1:]) if not x.isdigit()), None)
                index += 1
                if index is not None:
                    t0 = lines[:index]
                    t1 = lines[index:]
                print(index)
                print(t0)
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

def output(output_path,data):
    try:
        with open(output_path, 'w') as output_file:
            output_file.write(data)
    except FileNotFoundError:
        print("Path not found.Please make sure the output path is correct.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python input_generator.py input_path output_path")
        return
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    data = input(input_path)
    output(output_path,data[0])

# Call the main function
if __name__ == "__main__":
    main()

