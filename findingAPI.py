from ebaysdk.finding import Connection as Finding
from ebaysdk.trading import Connection as Trading

'''findingApi = Finding(config_file = "ebay.yaml", siteid = "EBAY-GB")

requests ={
        "itemFilter": [
            {"name" : "Condition", "value" : "New"},
            {"name" : "Seller", "value" : "angelone4"}
        ],
        "paginationInput" : {
            "entriesPerPage" : 100,
            #"pageNumber" : 1 Normally shows which page will be printed
            #Default value is 1 so this is unnecessary.
        },
        "sortOrder": "PricePlusShippingLowest"
}

response = findingApi.execute("findItemsAdvanced",requests)

for item in response.reply.searchResult.item:
    print(item.title, item.sellingStatus.currentPrice.value, item)
'''

outputFile=open("outputFile.csv", "r")
tradingApi = Trading(config_file = "ebay.yaml", site ="api.sandbox.ebay.com")

requests = {
        "ActiveList" : {"Include" : True}
}

counter=0
results = tradingApi.execute("GetMyeBaySelling", requests)
for x in results.reply.ActiveList.ItemArray.Item:
    print(f'Item name: {x.Title} Item price: £{x.SellingStatus.CurrentPrice.value} Stock Remaining: {x.QuantityAvailable}')
    counter+=1

existingData=[]
line = outputFile.readline()
while line!="":
    existingData.append(line.strip(",\n").split(","))
    line=outputFile.readline()
outputFile.close()

for x in existingData:
    print(x)
