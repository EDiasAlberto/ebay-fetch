from ebaysdk.finding import Connection as Finding
from ebaysdk.trading import Connection as Trading
from decimal import Decimal

counter=0
fetchedListings=[]
existingData=[]
modifiedExistingData=[]
ebayObjects=[]
fetchedNames=[]
existingNames=[]


class ebayListingItem:
    def __init__(self, name, cost, postage, actual, initStock, inStock, packaging=0.5):
        self.name=name
        self.cost=round(float(cost),2)
        self.postage=round(float(postage),2)
        self.packaging=round(float(packaging),2)
        self.actual=round(float(actual),2)
        self.ebay=round((int(self.actual*100)*0.11)/100, 2)
        self.paypal=round(float((self.actual/100)*5),2)
        self.minimum=round(self.ebay+self.paypal+self.cost+self.postage+self.packaging, 2)
        if int(inStock)>0:
            self.active=True
        self.profit=round(float(self.actual-self.minimum),2)
        self.initStock=int(initStock)
        self.inStock=int(inStock)
        self.soldStock=self.initStock-self.inStock

    def printInfo(self):
        print(self.name, self.cost, self.postage, self.packaging, self.actual, self.ebay, self.paypal, self.minimum, self.active, self.profit, self.initStock, self.soldStock, self.inStock)


outputFile=open("outputFile2.csv", "r")
tradingApi = Trading(config_file = "ebay.yaml", site ="api.sandbox.ebay.com")

requests = {
        "ActiveList" : {"Include" : True}
}


results = tradingApi.execute("GetMyeBaySelling", requests)
for x in results.reply.ActiveList.ItemArray.Item:
    #print(f'Item name: {x.Title} Item price: £{x.SellingStatus.CurrentPrice.value} Initial Stock: {x.Quantity} Stock Remaining: {x.QuantityAvailable} Sold Stock {int(x.Quantity)-int(x.QuantityAvailable)}')
    fetchedListings.append([x.Title, x.SellingStatus.CurrentPrice.value, x.Quantity, x.QuantityAvailable, int(x.Quantity)-int(x.QuantityAvailable)])
    counter+=1



line = outputFile.readline()
while line!="":
    existingData.append(line.strip(",\n").split(","))
    line=outputFile.readline()
outputFile.close()


header=existingData.pop(0)
for x in range(len(existingData)):
    if not("n/a" in existingData[x]):
        modifiedExistingData.append(existingData[x])

for x in modifiedExistingData:
    for y in range(len(x)):
        x[y]=x[y].replace("Â£","")


for x in fetchedListings:
    fetchedNames.append(x[0])

for x in modifiedExistingData:
    existingNames.append(x[0])

for x in fetchedListings:
    for y in modifiedExistingData:
        if x[0]==y[0]:
            ebayObjects.append(ebayListingItem(x[0], y[1], 3.70, x[1], initStock=x[2], inStock=x[3]))

for x in fetchedNames:
    if x not in existingNames:
        print("\nNEW ITEM DETECTED!")
        itemCost=round(float(input(f"Please enter the cost of {x} (numbers only):")))
        for z in range(len(fetchedListings)):
            if x in fetchedListings[z]:
                position=z
                break

        ebayObjects.append(ebayListingItem(x, itemCost, 3.70, fetchedListings[z][1], fetchedListings[z][2], fetchedListings[z][3]))

#print("%-100s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %-15s %-15s %-15s %-15s \n"%("Name", "Cost", "Postage", "Packaging", "EBay", "PayPal", "Minimum", "Actual", "Profit", "Initial Stock", "Sold Stock", "In Stock"))

ebayObjects=sorted(ebayObjects, key = lambda x:x.name)

#for x in ebayObjects:
    #print("%-100s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %-15s %-15s %-15s %-15s \n"%(x.name, x.cost, x.postage, x.packaging, x.ebay, x.paypal, x.minimum, x.actual, x.profit, x.initStock, x.soldStock, x.inStock))

outputFile=open("outputFile2.csv", "w")
outputFile.write("Name, Cost, Postage, Package, EBay, PayPal, Minimum, Actual, Profit, Initial Stock, Sold Stock, In Stock\n")
for x in ebayObjects:
    outputFile.write(f"{x.name}, {x.cost}, {x.postage}, {x.packaging}, {x.ebay}, {x.paypal}, {x.minimum}, {x.actual}, {x.profit}, {x.initStock}, {x.soldStock}, {x.inStock}\n")
outputFile.close()
