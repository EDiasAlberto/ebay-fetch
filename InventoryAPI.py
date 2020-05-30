from ebaysdk.shopping import Connection
api = Connection(config_file = "ebay.yaml", siteid = "EBAY-GB")
response = api.execute('FindProducts', {'QueryKeywords': 'Ghost BCAA'})

print(response.dict())
