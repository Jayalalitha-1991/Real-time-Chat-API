# Python Data Types:
    Text Type:	str
    Numeric Types:	int, float, complex
    Sequence Types:	list, tuple, range
    Mapping Type:	dict
    Boolean Type:	bool



# # # Text Type:	str
# # name = "Jaya"

# # print(type(name))

# # # int
# # x = 10
# # print(type(x))

# # # float
# # y = 3.14
# # print(type(y))

# # # complex
# # z = 2 + 3j
# # print(type(z))  

# # #list – Ordered, mutable collection
# fruits = ["apple", "banana", "cherry"]
# print(fruits)
# print(type(fruits)) 

# # #tuple – Ordered, immutable collection

# # coordinates = (10.0, 20.0)
# # print(type(coordinates)) 

# # #range – Sequence of numbers
r = range(7, 15, 2)
for n in r:
    print(n)
print(type(r))

# # dict – Key-value pairs

# person = {"name": "Alice", "age": 25}
# print(type(person))

# # # bool – True or False
# is_active = True
# print(type(is_active))



Project: Simple Shopping Cart
 What it does:
Add items to a shopping cart (item name + price)

Stores items using a list of dictionaries

Calculates total price

Uses various data types like strings, floats, lists, and booleans