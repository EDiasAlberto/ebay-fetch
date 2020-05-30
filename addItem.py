from ebaysdk.trading import Connection

api = Connection(config_file="ebay.yaml", site="api.sandbox.ebay.com", siteID="EBAY-GB", debug=True)
request = {
    "Item": {
        "Title": "Professional Mechanical Keyboard",
        "Country":"GB",
        "Location":"GB",
        "Site": "UK",
        "ConditionID": "1000",
        "PaymentMethods": "PayPal",
        "PayPalEmailAddress": "ethanjalberto@gmail.com",
        "PrimaryCategory": {"CategoryID": "33963"},
        "Description": "The title.",
        "ListingDuration": "Days_10",
        "BuyItNow": "349.99",
        "Currency": "GBP",
        "ReturnPolicy": {
            "ReturnsAcceptedOption": "ReturnsAccepted",
            "RefundOption": "MoneyBack",
            "ReturnWithinOption": "Days_30",
            "Description": "I cba to describe a return policy.",
            "ShippingCostPaidByOption": "Buyer"
        },
        "ShippingDetails": {
            "ShippingServiceOptions": {
                "FreeShipping": "True",
                "ShippingService": "UK_RoyalMailSecondClassStandard"
            }
        },
        "DispatchTimeMax": "3"

    }
}

api.execute("VerifyAddItem", request)
