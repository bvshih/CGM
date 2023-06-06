import time

p = d1_s1.g[:1000]

ti = time.perf_counter()

r = [distance(*p['pos'][i]) for i in range(len(p))]

tf = time.perf_counter()

print(f'time: {tf-ti:.4f}') #time: 3.0697


ti = time.perf_counter()

r = [distance(p['x'][i], p['y'][i], p['z'][i]) for i in range(len(p))]

tf = time.perf_counter()

print(f'time: {tf-ti:.4f}') #time: 8.3779