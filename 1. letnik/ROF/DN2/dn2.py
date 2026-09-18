import numpy as np
import matplotlib.pyplot as plt

np.random.seed(12345)

plt.rcParams.update({"text.usetex": True})

lst = [1,2,3,4,5,6]

def met():
    return np.sum(np.random.choice(lst, 20))

meti = np.array([met() for x in range(10000)])

print(np.mean(meti), np.std(meti))

def gauss(t, povp, sigma):
    return 1/np.sqrt(2*np.pi*sigma**2)*np.exp(-(t-povp)**2/(2*sigma**2))
x0 = np.linspace(40, 100, 100)

plt.hist(meti, bins=20, ec="black", fc="lime", density=True, alpha=0.5, label="delež metov")
plt.plot(x0, gauss(x0, np.mean(meti), np.std(meti)),  'r-.', lw=2, label="Gaussova porazdelitev")
plt.xlim(40, 100)
plt.title('Histogram')
plt.xlabel('Vsota 20-ih metov')
plt.ylabel('Število ponovitev')
plt.legend()

plt.show() 


