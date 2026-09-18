import math
import matplotlib.pyplot as plt
import matplotlib.style
matplotlib.style.use("ggplot")
meritve = [153.737, 153.593, 153.301, 153.852, 153.384, 153.509, 153.453, 153.562, 153.684, 153.500, 153.475, 153.541, 153.787, 153.446, 153.365, 153.550, 153.447, 153.228, 153.606, 153.581, 153.360, 153.447, 153.450, 153.438, 153.436, 153.245, 153.768, 153.723, 153.289, 153.707, 153.581, 153.137, 153.621, 153.675, 153.672, 153.469, 153.150, 153.323, 153.589, 153.724, 153.338, 153.573, 154.011, 154.010, 153.950, 153.950, 153.928, 153.855, 153.873, 154.053]
meritve.sort()
indeks=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50]


povp=0
for i in meritve:
    povp+=i
povp/=50


std=0
for i in meritve:
    std+=(povp-i)**2
std/=50
std=math.sqrt(std)

print("povp: ", povp)
print("std: ", std)
print(meritve)


plt.scatter(indeks, meritve)

plt.title('Porazdelitev meritev')    
plt.ylabel('t[ms]')    
plt.xlabel('N')

plt.show()