import math

#tukaj vnesi vse rezultate meritev brez enot, program izpiše povprečno vrednost in efektivni odmik v istih enotah, kot so zapisane meritve
meritve = []

povp = sum(i for i in meritve)/len(meritve)
sigma = 0

for i in meritve:
    sigma += (i - povp)**2
sigma = math.sqrt(sigma/len(meritve))

print("Povprečna vrednost: ", povp)
print("Efektivni odmik: ", sigma)