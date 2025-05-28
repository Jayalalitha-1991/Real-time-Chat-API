cart = []
shopping = True

print("Welcome to the Simple Shopping Cart!")

while shopping:
    item = input("Enter item name: ")
    price = float(input(f"Enter price for {item}: $"))

    cart.append({"name": item, "price": price})

    choice = input("Add another item? (yes/no): ").lower()
    if choice != "yes":
        shopping = False

# Calculate total
total = sum(item["price"] for item in cart)

# Print cart summary
print("\n--- Shopping Cart ---")
for item in cart:
    print(f"{item['name']}: ${item['price']:.2f}")
print(f"Total: ${total:.2f}")
