TO DO LIST:
1) Create a GUI
2) Tighten up and make the program clean
3) Comment my code
4) Create functions rather than just having code running

To use this app, fill out the name and cost price for each item in the outputFile.csv
or skip to step 2 then fill out the prompts from the program

Then, create a file called ebay.yaml
IN ebay.yaml:
	name: ebay_api_config

	# Trading API Sandbox - https://www.x.com/developers/ebay/products/trading-api
	api.sandbox.ebay.com:
		compatability: 719
		appid: YOUR_APP_ID
		certid: YOUR_CERT_ID
		devid: YOUR_DEV_ID
		token: YOUR_AUTH_TOKEN

	# Trading API - https://www.x.com/developers/ebay/products/trading-api
	api.ebay.com:
		compatability: 719
		appid: YOUR_APP_ID
		certid: YOUR_CERT_ID
		devid: YOUR_DEV_ID
		token: YOUR_AUTH_TOKEN

	# Finding API - https://www.x.com/developers/ebay/products/finding-api
	svcs.ebay.com:
		appid: YOUR_APP_ID

	# Shopping API - https://www.x.com/developers/ebay/products/shopping-api
	open.api.ebay.com:
		appid: YOUR_APP_ID
