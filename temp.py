import seaborn as sns
import matplotlib.pyplot as plt

# Sample data
categories = ['Category A', 'Category B', 'Category C', 'Category D']
values = [15, 30, 10, 25]

# Create a bar plot using Seaborn
sns.set(style="whitegrid")  # Set the style of the plot
plt.figure(figsize=(10, 6))  # Set the size of the plot

# Create the bar plot
sns.barplot(x=categories, y=values, palette="viridis")

# Adding labels and title
plt.xlabel("Categories")
plt.ylabel("Values")
plt.title("Bar Plot Example")

# Save the plot as an image
plt.savefig("output.png")

# Display the plot
plt.show()