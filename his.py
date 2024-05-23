import matplotlib.pyplot as plt

data = [1, 2, 3, 3, 4, 4, 4, 5, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 8]

plt.hist(data, bins=8, color='blue', edgecolor='black')

plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram')

plt.show()