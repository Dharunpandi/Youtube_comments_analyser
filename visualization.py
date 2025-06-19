import matplotlib.pyplot as plt

# Overall score in percentage (e.g. 8.1 out of 10 = 81%)
score = 8.1
percentage = score * 10  # Convert to percentage

# Data for the donut chart
sizes = [percentage, 100 - percentage]
colors = ['#a6d854', '#e0e0e0']  # green and grey
labels = ['', '']  # no labels for now

# Plot
fig, ax = plt.subplots(figsize=(4, 4))
wedges, _ = ax.pie(
    sizes, labels=labels, colors=colors, startangle=90, counterclock=False,
    wedgeprops={'width': 0.2, 'edgecolor': 'white'}
)

# Center Text
plt.text(0, 0, f"{int(percentage)}%", ha='center', va='center', fontsize=18, fontweight='bold')

# Remove axes
ax.axis('equal')  
plt.title("Overall Score")
plt.tight_layout()
plt.show()
