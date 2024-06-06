import matplotlib.pyplot as plt

data = {
    1: 1010, 2: 357, 3: 191, 4: 89, 5: 66, 6: 54, 7: 25, 8: 12, 9: 13, 10: 6, 20: 1, 25: 1, 21: 3, 38: 1, 18: 3,
    12: 5, 11: 13, 30: 1, 15: 3, 29: 2, 27: 1, 13: 6, 16: 2, 56: 1, 14: 2, 19: 1, 23: 1
}

sorted_data = dict(sorted(data.items()))

x = list(sorted_data.keys())
y = list(sorted_data.values())


plt.figure(figsize=(10, 6))
plt.plot(x, y, marker='o', color='y')
plt.title('Degree Distribution')
plt.xlabel('Degree')
plt.ylabel('Count')
plt.grid(True)
plt.savefig('../plots/degree_distribution.png', dpi=300)
