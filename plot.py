s = """B: imp -84.82060606060605, rate 0.7739393939393939
C: imp -80.07414141414142, rate 0.8561616161616162
D: imp -56.87931506849314, rate 0.8028767123287672

E(4,25): imp -264.12363636363636, rate 1.0
E(10,7): imp -270.242, rate 0.9633333333333333"""

s = [ss for ss in s.split("\n") if len(ss)>0 ]
print(s)
s = [ss.split() for ss in s]
names = [ss[0] for ss in s]
imp = [-float(ss[2][:-1]) for ss in s]
imp_rate = [float(ss[-1]) for ss in s]
print(names, imp, imp_rate)

import matplotlib.pyplot as plt

# Data
# names = ['B:', 'C:', 'D:', 'E(4,25):', 'E(10,7):']
# imp = [-84.82060606060605, -80.07414141414142, -56.87931506849314, -264.12363636363636, -270.242]
# imp_rate = [0.7739393939393939, 0.8561616161616162, 0.8028767123287672, 1.0, 0.9633333333333333]

# Assign different colors for each method
colors = ['red', 'blue', 'green', 'orange', 'purple']

# Plot
plt.figure(figsize=(10, 6))
for i in range(len(names)):
    plt.scatter(imp[i], imp_rate[i], color=colors[i], label=names[i], s=100)  # s for point size

# Labels and Title
plt.xlabel('Improvement (imp)', fontsize=14)
plt.ylabel('Improvement Rate (imp_rate)', fontsize=14)
plt.title('Method Comparison: Improvement vs. Improvement Rate', fontsize=16)

# Legend
plt.legend(title='Methods', fontsize=10)

# Show grid
plt.grid(True, linestyle='--', alpha=0.7)

# Show the plot
plt.show()


# def mean(r):
#     return sum(r)/len(r)
# print(f"C: imp {mean(imp)}, rate {mean(imp_rate)}")