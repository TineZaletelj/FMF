import matplotlib.pyplot as plt
import matplotlib.style
matplotlib.style.use("ggplot")

#meritve
x1 = [3*2,3*2,5*2,10*2,8*2,5*2,6*2,3*2,4*2,3*2]
y = [1,2,3,4,5,6,7,8,9,10]

#Gauss
x2 = [3.2, 6, 9.7, 13.3, 15.6, 15.6, 13.3, 9.7, 6, 3.2]

plt.scatter(y, x1)
plt.plot(y, x2, color='g')

    
plt.ylabel('verjetnost, da meritev pade v interval[%]')    
plt.xlabel('zap. št. intervala')

plt.show()
