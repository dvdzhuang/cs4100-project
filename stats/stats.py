import sys
import math

n = 100
f = open(sys.argv[1], 'r')
times = []
for _ in range(n):
    times.append(float(f.readline()))

mean = sum(times) / n
std = math.sqrt(sum([(x - mean) ** 2 for x in times]) / n)
minimum = min(times)
maximum = max(times)

print('Mean:', mean)
print('Standard deviation:', std)
print('Minimum:', minimum)
print('Maximum:', maximum)