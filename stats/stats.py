import sys
import math

n = 100
f = open(sys.argv[1], 'r')
times = []
for _ in range(n):
    times.append(float(f.readline()))
f.close()

times.sort()
median = times[n // 2] if n % 2 else (times[n // 2 - 1] + times[n // 2]) / 2
mean = sum(times) / n
std = math.sqrt(sum([(x - mean) ** 2 for x in times]) / n)
minimum = times[0]
maximum = times[n-1]

print('Mean:', mean)
print('Median:', median)
print('Standard deviation:', std)
print('Minimum:', minimum)
print('Maximum:', maximum)