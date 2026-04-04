import pandas as pd
import matplotlib.pyplot as plt

#Load the data
df = pd.read_csv("2019-Dec.csv")
df.head()

# clean the data
df = df.dropna(subset=['user_id', 'event_type'])
df['event_time'] = pd.to_datetime(df['event_time'])

# Build the funnel

# Count users at each stage

views = df[df['event_type'] == 'view']['user_id'].nunique()
carts = df[df['event_type'] == 'cart']['user_id'].nunique()
purchases = df[df['event_type'] == 'purchase']['user_id'].nunique()

print("Users at each stage:", views, carts, purchases)

#Calculate conversion rates
view_to_cart =  carts / views
cart_to_purchase = purchases /carts

print("view -> cart conversion rate:", round(view_to_cart*100, 2), "%")
print("cart -> purchase conversion rate:", round(cart_to_purchase*100, 2), "%")

#Visualize funnel
stages = ['View', 'cart', 'purchase']
values = [views, carts, purchases]

plt.figure(figsize=(8,6))
bars = plt.bar(stages, values, color=['skyblue', 'orange', 'green'])

#Add labels on top of bars
for bar in bars:
    height= bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height*1.01, f'{height}', ha='center', fontsize=12)

plt.title("Funnel Anlysis", fontsize=16)
plt.ylabel("Unique Users")
plt.show()

# Optional: Funnel-style visualization (descending width)
plt.figure(figsize=(6,6))
plt.barh(stages[::-1], values[::-1], color=['green', 'orange','skyblue'])
for i, v in enumerate(values[::-1]):
    plt.text(v + 10, i, str(v), va='center')
    plt.title("Funnel Analysis (Horizontal)", fontsize=16)
    plt.xlabel("Unique Users")
    plt.show()


