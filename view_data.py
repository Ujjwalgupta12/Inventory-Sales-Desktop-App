import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

print("Product Master:")
cursor.execute("SELECT * FROM product_master")
print(cursor.fetchall())

print("\nGoods Receiving:")
cursor.execute("SELECT * FROM goods_receiving")
print(cursor.fetchall())

print("\nSales:")
cursor.execute("SELECT * FROM sales")
print(cursor.fetchall())

conn.close()
