import math

#tukaj vnesi vse rezultate meritev brez enot, program izpiše povprečno vrednost in efektivni odmik v istih enotah, kot so zapisane meritve
meritve = {"t0":[1.847, 1.856, 1.855, 1.856], "t1":[1.762, 1.76, 1.771, 1.761], "utrip":[1.76, 1.77, 1.766, 1.758], "T":[37.13, 37.18, 37.27, 37.32], "w0":[3.402, 3.385, 3.387, 3.385], "w1":[3.566, 3.570, 3.548, 3.568], "utrip1":[3.570, 3.55, 3.558, 3.574], "wu":[0.1692, 0.169, 0.1686, 0.1684]}

for i in meritve:
    povp = sum(x for x in meritve[i])/len(meritve[i])
    sigma = 0

    for a in meritve[i]:
        sigma += (a - povp)**2
    sigma = math.sqrt(sigma/len(meritve[i]))

    print(i)
    print("Povprečna vrednost: ", povp)
    print("Efektivni odmik: ", sigma)