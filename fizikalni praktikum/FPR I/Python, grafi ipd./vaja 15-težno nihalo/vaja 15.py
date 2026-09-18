import math

meritve = [296.89, 297.48, 297.34, 297.37, 297.15, 297.06, 297.25, 297.11, 297.34, 297.09, 297.48, 297.23, 297.2, 296.99, 297.12, 296.97, 296.95, 297.26, 297, 297.05, 297.21, 297.36, 297.42, 297.34, 297.52, 297.66, 297.36, 297.58, 297.22, 297.71, 297.63]

povp = sum(i for i in meritve)/len(meritve)
sigma = 0

for i in meritve:
    sigma += (i - povp)**2
sigma = math.sqrt(sigma/len(meritve))

print(povp)
print(sigma)