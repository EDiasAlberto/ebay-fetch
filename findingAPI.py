#This loads in the trading API for the ebaysdk in order to fetch data from the website.
from ebaysdk.trading import Connection as Trading
import tkinter
import random
import time


#This creates a few empty lists that are used for comparisons later on.
fetchedListings=[]
existingData=[]
modifiedExistingData=[]
ebayObjects=[]
fetchedNames=[]
existingNames=[]

#This defines the class ebayListingItem that is used to represent each ebay listing in order to more easily format the rows when writing to the file.
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

    #This is a function used purely for testing at the moment, that just prints out all the attributes of any specific listing.
    def printInfo(self):
        print(self.name, self.cost, self.postage, self.packaging, self.actual, self.ebay, self.paypal, self.minimum, self.active, self.profit, self.initStock, self.soldStock, self.inStock)

#This is a function that loads in all the existing data from the file into a list called "existingData".
def loadFileData():
    global mainWindow
    mainWindow.destroy()
    mainWindow=tkinter.Tk()
    mainWindow.title("Ebay Fetch")
    mainWindow.geometry("300x200")
    tkinter.Label(mainWindow, text="Fetching Data...", font="Helvetica 12").pack()

    outputFile=open("outputFile2.csv", "r")
    line = outputFile.readline()
    while line!="":
        existingData.append(line.strip(",\n").split(","))
        line=outputFile.readline()
    outputFile.close()
    loadSiteData()

#This is a function that loads all the data from teh listings on the site into a list called "fetchedListings".
def loadSiteData():
    tradingApi = Trading(config_file = "ebay.yaml", site ="api.sandbox.ebay.com")

    requests = {
            "ActiveList" : {"Include" : True}
    }


    results = tradingApi.execute("GetMyeBaySelling", requests)
    for x in results.reply.ActiveList.ItemArray.Item:
        #print(f'Item name: {x.Title} Item price: £{x.SellingStatus.CurrentPrice.value} Initial Stock: {x.Quantity} Stock Remaining: {x.QuantityAvailable} Sold Stock {int(x.Quantity)-int(x.QuantityAvailable)}')
        fetchedListings.append([x.Title, x.SellingStatus.CurrentPrice.value, x.Quantity, x.QuantityAvailable, int(x.Quantity)-int(x.QuantityAvailable)])
    tidyData()

#This is a function that removes all listings that are not in stock.
#Then it removes all unrelated characters from each listing.
def tidyData():
    header=existingData.pop(0)
    for x in existingData:
        if not("n/a" in x):
            modifiedExistingData.append(x)

    for x in modifiedExistingData:
        for y in range(len(x)):
            x[y]=x[y].replace("Â£","")
    createListingObjects()

#This then calculates and creates objects using the class above of each listing.
#Then it stores them in the list ebayObjects.
def createListingObjects():
    for x in fetchedListings:
        for y in modifiedExistingData:
            if x[0]==y[0]:
                ebayObjects.append(ebayListingItem(x[0], y[1], 3.70, x[1], initStock=x[2], inStock=x[3]))
    newItemDetection()

def appendListing(item, value):
    for z in range(len(fetchedListings)):
        if item == fetchedListings[z]:
            position=z
            break
    ebayObjects.append(ebayListingItem(item, value, 3.70, fetchedListings[z][1], fetchedListings[z][2], fetchedListings[z][3]))



#This function first creates two lists of the names of all items.
#One list has the names of items in the file, the other has the names of online listings.
#Then it uses some simple logic to find out which are new listings that are not yet in the file.
#THen it asks teh user to input the cost for each item and creates ebayListing objects.
def newItemDetection():
    global mainWindow
    global tkinterVar


    mainWindow.destroy()
    tkinterVar = tkinter.BooleanVar(mainWindow, value=False)
    tkinterVar.set(True)


    for x in fetchedListings:
        fetchedNames.append(x[0])

    for x in modifiedExistingData:
        existingNames.append(x[0])

    for x in fetchedNames:
        if x not in existingNames:
            mainWindow=tkinter.Tk()
            mainWindow.title("NEW ITEM DETECTED!")
            tkinter.Label(mainWindow, text=f"Please enter the cost of {x}:", font="Helvetica 12").grid(row=0, columnspan=2)
            tkinter.Label(mainWindow, text="£").grid(row=1, column=0)
            priceEntry=tkinter.Entry(mainWindow)
            priceEntry.grid(row=1, column=1)
            button=tkinter.Button(mainWindow, text="Enter", fg="green", font="Helvetica 12", command=lambda:[appendListing(x, priceEntry.get()), tkinterVar.set(1)])
            button.grid(row=2, columnspan=2)
            mainWindow.wait_variable(tkinterVar)

    mainWindow=tkinter.Tk()
    mainWindow.title("Ebay Fetch")
    tkinter.Label(mainWindow, text="All data has been fetched from the website.", font="Helvetica 12").pack()
    tkinter.Button(mainWindow, text="Main Menu", fg="red", font="Helvetica 12", command=lambda :main(True)).pack()

#This function writes all the data in rows and columns to the csv file so it can be opened in Excel.
def writeData():
    outputFile=open("outputFile2.csv", "w")
    outputFile.write("Name, Cost, Postage, Package, EBay, PayPal, Minimum, Actual, Profit, Initial Stock, Sold Stock, In Stock, Active\n")
    for x in ebayObjects:
        if x.initStock>0:
            outputFile.write(f"{x.name}, {x.cost}, {x.postage}, {x.packaging}, {x.ebay}, {x.paypal}, {x.minimum}, {x.actual}, {x.profit}, {x.initStock}, {x.soldStock}, {x.inStock}, True\n")
        else:
            outputFile.write(f"{x.name}, {x.cost}, {x.postage}, {x.packaging}, {x.ebay}, {x.paypal}, {x.minimum}, {x.actual}, {x.profit}, {x.initStock}, {x.soldStock}, {x.inStock}, False\n")
    outputFile.close()

def main(returnCheck=False):
    global mainWindow

    if returnCheck:
        mainWindow.destroy()

    mainWindow=tkinter.Tk()
    mainWindow.title("Ebay Fetch")
    mainWindow.geometry("300x200")
    for x in range(3):
        mainWindow.rowconfigure(x, weight=1)
    for x in range(2):
        mainWindow.columnconfigure(x, weight=1)

    tkinter.Label(mainWindow, text="Welcome to the Ebay Fetch App.", font="Helvetica 12").grid(row=0, columnspan=2, sticky="NSEW")
    tkinter.Button(mainWindow, text="Fetch Data", fg="green", font="Helvetica 12", command=loadFileData).grid(row=1, columnspan=2, sticky="NSEW")
    tkinter.Button(mainWindow, text="Exit Program", fg="red", font="Helvetica 12", command=mainWindow.destroy).grid(row=2, columnspan=2, sticky="NSEW")
    mainWindow.mainloop()

main()
