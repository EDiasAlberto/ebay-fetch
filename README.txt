TO DO LIST:
1) Tighten up and make the program clean
2) Add a function to confirm price changes

To use this app, fill out the name and cost price for each item in the outputFile.csv
or skip to step 2 then fill out the prompts from the program

Run the "downloadPython.bat" by double-clicking it, which will download a ".exe" file.
Run the .exe, ensuring that you tick the checkbox "Add Python 3.8.4 to PATH" on the first screen.
Follow through the installation.
Run the "install.bat" by double-clicking it, which will install the ebaysdk for python.

Then, create a file called ebay.yaml
Paste the following into the file:
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

Create an account and app on the ebay developer page. For the trading api (not the sandbox), copy your details into this file,
where the "#Trading API - ..." line is.

Double-click the "run.bat" to run the program.