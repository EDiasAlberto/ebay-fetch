#This loads in the trading API for the ebaysdk in order to fetch data from the website.
from ebaysdk.trading import Connection as Trading
import tkinter
from tkinter import messagebox, ttk


#This creates a few empty lists that are used for comparisons later on.
fetchedListings=[]
existingData=[]
modifiedExistingData=[]
ebayObjects=[]
fetchedNames=[]
existingNames=[]

#This defines the class ebayListingItem that is used to represent each ebay
#listing in order to more easily format the rows when writing to the file.
class ebayListingItem:
    def __init__(self, name, cost, postage, actual, initStock, inStock,
                 packaging=0.5):
        self.name=name
        self.cost=round(float(cost),2)
        self.postage=round(float(postage),2)
        self.packaging=round(float(packaging),2)
        self.actual=round(float(actual),2)
        self.ebay=round((int(self.actual*100)*0.11)/100, 2)
        self.paypal=round(float((self.actual/100)*5),2)
        self.minimum=round(self.ebay+
                           self.paypal+self.cost+self.postage+
                           self.packaging, 2)

        if int(inStock)>0:
            self.active=True
        self.profit=round(float(self.actual-self.minimum),2)
        self.initStock=int(initStock)
        self.inStock=int(inStock)
        self.soldStock=self.initStock-self.inStock

    #This is a function used purely for testing at the moment, that just prints
    #out all the attributes of any specific listing.
    def printInfo(self):
        print(self.name, self.cost, self.postage, self.packaging, self.actual,
              self.ebay, self.paypal, self.minimum, self.active, self.profit,
              self.initStock, self.soldStock, self.inStock)

    def __eq__(self, other):
        if isinstance(other, ebayListingItem):
            return self.name == other.name
        return False

#This is a function that loads in all the existing data from the file into a
#list called "existingData".
def loadFileData():
    global mainWindow
    global progressBar
    global progressLabel
    global percentageLabel


    mainWindow.destroy()
    mainWindow=tkinter.Tk()
    mainWindow.title("Ebay Fetch")
    mainWindow.geometry("300x200")
    progressLabel=tkinter.Label(mainWindow, text="Fetching Data from file...", font="Helvetica 12")
    progressBar=ttk.Progressbar(mainWindow, orient="horizontal", length=200, mode="determinate")
    percentageLabel=tkinter.Label(mainWindow, text="0%", font="Helvetica 12")
    progressLabel.pack()
    progressBar.pack()
    percentageLabel.pack()

    #This loads data in from the csv file.
    outputFile=open("outputFile.csv", "r")
    line = outputFile.readline()
    while line!="":
        existingData.append(line.strip(",\n").split(","))
        line=outputFile.readline()
    outputFile.close()

    #This runs the next function that loads data from the ebay site.
    loadSiteData()

#This is a function that loads all the data from teh listings on the site into
#a list called "fetchedListings".
def loadSiteData():
    global progressBar
    global progressLabel

    progressLabel.configure(text="Fetching Data from site...")
    percentageLabel.configure(text="25%")
    progressBar["value"]=25

    mainWindow.update()
    tradingApi = Trading(config_file = "ebay.yaml", site ="api.sandbox.ebay.com")

    requests = {
            "ActiveList" : {"Include" : True}
    }


    results = tradingApi.execute("GetMyeBaySelling", requests)
    for x in results.reply.ActiveList.ItemArray.Item:
        fetchedListings.append([x.Title, x.SellingStatus.CurrentPrice.value,
                                x.Quantity, x.QuantityAvailable,
                                int(x.Quantity)-int(x.QuantityAvailable)])

    #This tidies up the loaded data and removes any unnecessary parts.
    tidyData()

#This is a function that removes all listings that are not in stock.
#Then it removes all unrelated characters from each listing.
def tidyData():
    global progressBar
    global progressLabel

    progressLabel.configure(text="Tidying up data...")
    progressBar["value"]=50
    percentageLabel.configure(text="50%")

    mainWindow.update()
    header=existingData.pop(0)
    for x in existingData:
        if not("n/a" in x):
            modifiedExistingData.append(x)

    for x in modifiedExistingData:
        for y in range(len(x)):
            x[y]=x[y].replace("Â£","")

    #This creates the listing objects usign the ebayObjects class.
    createListingObjects()

#This then calculates and creates objects using the class above of each listing.
#Then it stores them in the list ebayObjects.
def createListingObjects():
    global progressBar
    global progressLabel

    progressLabel.configure(text="Creating Objects...")
    percentageLabel.configure(text="75%")
    progressBar["value"]=75
    mainWindow.update()
    for x in fetchedListings:
        for y in modifiedExistingData:
            if x[0]==y[0]:
                ebayObjects.append(ebayListingItem(x[0], y[1], 3.70, x[1],
                                   initStock=x[2], inStock=x[3]))

    #This runs the function that checks for any new products that have been
    #loaded from the website.
    newItemDetection()

#This function writes all the data in rows and columns to the csv file so it
#can be opened in Excel.
def writeData():
    global ebayObjects
    global progressLabel

    progressLabel.configure(text="Writing Data...")
    percentageLabel.configure(text="100%")
    progressBar["value"]=100
    mainWindow.update()

    ebayObjects=sorted(ebayObjects, key= lambda x:x.name)
    outputFile=open("outputFile.csv", "w")
    outputFile.write("Name, Cost, Postage, Package, EBay, PayPal, Minimum, Actual, Profit, Initial Stock, Sold Stock, In Stock, Active\n")
    for x in ebayObjects:
        outputFile.write(f"{x.name}, {x.cost}, {x.postage}, {x.packaging}, {x.ebay}, {x.paypal}, {x.minimum}, {x.actual}, {x.profit}, {x.initStock}, {x.soldStock}, {x.inStock}, {x.initStock > 0}")     
    outputFile.close()

#This function is used by the button on the new item detection window, where it
#fetches the entered cost and also creates a new listing object.
def appendListing(item, value):

    z = fetchedListings.index(item)
    ebayObjects.append(ebayListingItem(item, value, 3.70, fetchedListings[z][1],
                                       fetchedListings[z][2], fetchedListings[z][3]))



#This function first creates two lists of the names of all items.
#One list has the names of items in the file, the other has the names of online listings.
#Then it uses some simple logic to find out which are new listings that are not yet in the file.
#THen it asks teh user to input the cost for each item and creates ebayListing objects.
def newItemDetection():
    global mainWindow
    global tkinterVar



    for x in fetchedListings:
        fetchedNames.append(x[0])

    for x in modifiedExistingData:
        existingNames.append(x[0])

    for x in fetchedNames:
        if x not in existingNames:
            try:
                newItemWindow=tkinter.Tk()
                tkinterVar = tkinter.BooleanVar(newItemWindow, value=False)
                tkinterVar.set(True)
                newItemWindow.title("NEW ITEM DETECTED!")
                tkinter.Label(newItemWindow, text=f"Please enter the cost of {x}:",
                              font="Helvetica 12").grid(row=0, columnspan=2, sticky="NSEW")
                tkinter.Label(newItemWindow, text="£").grid(row=1, column=0, sticky="E")
                priceEntry=tkinter.Entry(newItemWindow)
                priceEntry.grid(row=1, column=1, sticky="W")
                button=tkinter.Button(newItemWindow, text="Enter", fg="green",
                                      font="Helvetica 12", command=lambda:[appendListing(x, priceEntry.get()), tkinterVar.set(1)])
                button.grid(row=2, columnspan=2)
                newItemWindow.wait_variable(tkinterVar)
                newItemWindow.destroy()
            except ValueError:
                messagebox.showinfo(title="Invalid input",
                                    message="The cost cannot be left empty.")

    writeData()
    mainWindow.destroy()
    mainWindow=tkinter.Tk()
    mainWindow.title("Ebay Fetch")
    tkinter.Label(mainWindow, text="All data has been fetched from the website.",
                  font="Helvetica 12").pack()
    tkinter.Button(mainWindow, text="Main Menu", fg="red", font="Helvetica 12",
                   command=lambda :main(True)).pack()



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

    tkinter.Label(mainWindow, text="Welcome to the Ebay Fetch App.",
                  font="Helvetica 12").grid(row=0, columnspan=2, sticky="NSEW")
    tkinter.Button(mainWindow, text="Fetch Data", fg="green", font="Helvetica 12",
                   command=loadFileData).grid(row=1, columnspan=2, sticky="NSEW")
    tkinter.Button(mainWindow, text="Exit Program", fg="red", font="Helvetica 12",
                   command=mainWindow.destroy).grid(row=2, columnspan=2, sticky="NSEW")


if __name__=="__main__":
    main()
    mainWindow.mainloop()
