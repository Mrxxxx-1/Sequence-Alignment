'''
Author: Mrx
Date: 2024-05-09 13:16:50
LastEditors: Mrx
LastEditTime: 2024-05-09 22:23:35
FilePath: \Sequence-Alignment\plot.py
Description: 

Copyright (c) 2024 by Mrx, All Rights Reserved. 
'''
import matplotlib.pyplot as plt

# Data
problem_size = [16, 64, 128, 256, 384, 512, 768, 1024, 1280, 1536, 2048, 2560, 3072, 3584, 3968]
memory_basic = [8, 48, 220, 716, 1316, 1432, 3120, 2592, 3044, 2772, 3296, 3572, 4052, 4420, 3628]
memory_efficient = [8, 12, 16, 52, 100, 72, 240, 80, 116, 544, 592, 676, 704, 756, 804]

# Plotting
plt.figure(figsize=(10, 6))

# Memory Plot
plt.plot(problem_size, memory_basic, marker='o', label='Basic Algorithm')
plt.plot(problem_size, memory_efficient, marker='o', label='Efficient Algorithm')

# Adding labels and title
plt.xlabel('Problem Size (m+n)')
plt.ylabel('Memory (KB)')
plt.title('Memory Usage vs Problem Size')
plt.legend()

plt.tight_layout()
plt.show()
