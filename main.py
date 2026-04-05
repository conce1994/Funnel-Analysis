# 1. Import Libraries
import pandas as pd
import matplotlib.pyplot as plt

# 2. Load data
df = pd.read_csv("2019-Dec.csv")
df.head()

# Load data set into DataFrame
# Each row = one user event (view, cart, purchase)

print(df.head())
print(df.info())

# 3. Data Cleaning

# Remove rows with missing user_id or event_type

df = df.dropna(subset=['user_id', 'event_type'])

# Convert event_time to datetime format
df['event_time'] = pd.to_datetime(df['event_time'])

# Why this matters:
# - Missing user_id =  cannot track users
# - Datetime conversion allows time analysis later

# 4. Basic Funnel Analysis

# Count unique users at each stage

views = df[df['event_type'] == 'view']['user_id'].nunique()
carts = df[df['event_type'] == 'cart']['user_id'].nunique()
purchases = df[df['event_type'] == 'purchase']['user_id'].nunique()

print("\nUsers at each stage:")
print("Views:", views)
print("Carts:", carts)
print("Purchases:", purchases)

# Conversion Rates

view_to_cart =  carts / views
cart_to_purchase = purchases /carts

print("\nConversion Rates:")
print("View -> Cart:", round(view_to_cart*100, 2), "%")
print("Cart -> Purchase:", round(cart_to_purchase*100, 2), "%")

# 6. Drop-off analysis

drop_view_cart = 1 - view_to_cart
drop_cart_purchase = 1 - cart_to_purchase

print("\nDrop-off Rates:")
print("View -> Cart:", round(drop_view_cart*100, 2), "%")
print("Cart -> Purchase:", round(drop_cart_purchase*100, 2), "%")

# Shows where users leave -> biggest business problem

#7. Funnel Visualization (Vertical)

stages = ['View', 'Cart', 'Purchase']
values = [views, carts, purchases]

plt.figure(figsize=(8,6))
bars = plt.bar(stages, values)

for bar in bars:
    height= bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height*1.01,
             f'{int(height)}', ha='center')


plt.title("Funnel Analysis")
plt.ylabel("Unique Users")
plt.show()

# 8 Funnel Visualization (Horizontal)

plt.figure(figsize=(6,6))
plt.barh(stages[::-1], values[::-1])

for i, v in enumerate(values[::-1]):
    plt.text(v, i, str(int(v)), va='center')

plt.title("Funnel Analysis (Horizontal)")
plt.xlabel("Users")
plt.show()

# 9. Category level analysis

# Group by category and event type
category_funnel = df.groupby(['category_code','event_type'])['user_id'].nunique().unstack()

# Calculate conversion rates per category
category_funnel['view_to_cart'] = category_funnel['cart'] /category_funnel['view']
category_funnel['cart_to_purchase'] =category_funnel['purchase'] / category_funnel['cart']

print("\nTop Categories by view -> Cart Conversion:")
print(category_funnel.sort_values('view_to_cart', ascending=False).head())

# Identifies which product categories perform well or poorly

# 10. User behavior analysis

# Count number of purchases per user
user_purchases = df[df['event_type']] == 'purchase'.groupby('user_id').size()

print("\nTop 5 Users by Purchases:")
print(user_purchases.sort_values(ascending=False).head())

# Shows that a small group drives most revenue

# 11. Time based analysis

# extract hour from timestamp
df['hour'] = df['event_time'].dt.hour

# Count events per hour
df['hour'] = df.groupby(['hour', 'event_type'])['user_id'].count().unstack()

print("\nHourly Activity:")
print(hourly.head())

# Plot hourly activity

hourly.plot(figsize=(10,6))
plt.title("User Activity by Hour")
plt.xlabel("hour of Day")
plt.ylabel("Event Count")
plt.show()

# Helps Identify peak engagement & purchase times










