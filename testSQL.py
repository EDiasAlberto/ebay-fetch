import pyodbc

dbConnection = pyodbc.connect("DRIVER={MySQL ODBC 8.0 ANSI Driver};" "SERVER=localhost;" "DATABASE=ebay;" "UID=python;" ,autocommit=True)

cursor = dbConnection.cursor()

#loop through all drivers
#for driver in pyodbc.drivers():
    #print(driver)





cursor.execute("UPDATE items SET ebay = actual*0.11")
cursor.execute("UPDATE items SET paypal = actual*0.05")
cursor.execute("UPDATE items SET minimum = cost_price+postage+packaging+ebay+paypal")
cursor.execute("UPDATE items SET profit = actual-minimum")
cursor.execute("UPDATE items SET in_stock = inv_stock-sold_stock")


for x in cursor.execute("SELECT * FROM items;"):
    for y in x:
        print(y, end=" ")

cursor.close()
dbConnection.close()
