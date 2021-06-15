# https://www.homedepot.com/p/writeAReview?itemId=205344405

# ID = "BACK_ORDERED"

# https://www.homedepot.com/mcc-cart/v3/appliance/deliveryAvailability/305712398/zipCode/33304

# # {
# #   "DeliveryAvailabilityResponse": {
# #     "deliveryAvailability": {
# #       "zipCode": "33304",
# #       "primaryStrNbr": "6372",
# #       "availability": [
# #         {
# #           "itemId": "305712398",
# #           "modelNbr": "LFXS26596S",
# #           "status": "BACK_ORDERED",
# #           "etaDate": "2021-08-04T23:59:59.000Z"
# #         }
# #       ],
# #       "earliestAvailabilityDate": "2021-08-04"
# #     }
# #   }
# # }

# ID="AVAILABLE"

# https://www.homedepot.com/mcc-cart/v3/appliance/deliveryAvailability/206290120/zipCode/33317

# # // 20210608163840
# # // https://www.homedepot.com/mcc-cart/v3/appliance/deliveryAvailability/206290120/zipCode/33317

# # {
# #   "DeliveryAvailabilityResponse": {
# #     "deliveryAvailability": {
# #       "zipCode": "33317",
# #       "primaryStrNbr": "0222",
# #       "availability": [
# #         {
# #           "itemId": "206290120",
# #           "modelNbr": "LDG4313ST",
# #           "status": "AVAILABLE"
# #         }
# #       ],
# #       "earliestAvailabilityDate": "2021-06-17"
# #     }
# #   }
# # }

# ID = "OUT_OF_STOCK"

# https://www.homedepot.com/mcc-cart/v3/appliance/deliveryAvailability/205905754/zipCode/33319

# # // 20210608163948
# # // https://www.homedepot.com/mcc-cart/v3/appliance/deliveryAvailability/205905754/zipCode/33319

# # {
# #   "DeliveryAvailabilityResponse": {
# #     "deliveryAvailability": {
# #       "zipCode": "33319",
# #       "primaryStrNbr": "0258",
# #       "availability": [
# #         {
# #           "itemId": "205905754",
# #           "modelNbr": "KRFC300ESS",
# #           "status": "OOS_ETA_UNAVAILABLE"
# #         }
# #       ]
# #     }
# #   }
# # }


# Configs.json


# https://assets.homedepot-static.com/mobile-apps/ios-static/config/configconios-prod.json

# https://assets.adobedtm.com/633870858fb6/2b36cb1d2041/launch-c119949b4511.json

# attributeNames

# https://assets.homedepot-static.com/mobile-apps/ios-static/FAQ/AttributeNames.json

# FULL FINDER DESCRIPTION and review:

# https://api.bazaarvoice.com/data/reviews.json?apiversion=5.4&Filter=ProductId:309731132&Stats=Reviews&Include=Products&Limit=10&Passkey=u2tvlik5g1afeh78i745g4s1d&Offset=0&Sort=Helpfulness:desc,TotalPositiveFeedbackCount:desc

# SHORT DESCRIPTION WITH REVIEW:


# https://api.bazaarvoice.com/data/reviews.json?apiversion=5.4&Filter=ProductId:309731132&Include=Products&Limit=1&Passkey=u2tvlik5g1afeh78i745g4s1d


# import urllib.request
# import json
# import requests
# import time

# product_id = 309731132
# _api_key = "u2tvlik5g1afeh78i745g4s1d"
# zip_code = 33319
# store_id = 6372


# def status_code(json_url):
#     r = requests.get(json_url)
#     return r
    
# # print(status_code(hd_url1))

# def url_reader(json_url):
#     with urllib.request.urlopen(json_url) as url:
#         data = json.loads(url.read().decode())
#         return data

# # print(url_reader(hd_url1))

# '''
# PRODUCT REVIEWS QUERY
# '''
# def review_extractor(product_id,_api_key):
#     #URL with reviews json
#     r_json_url = f"https://api.bazaarvoice.com/data/reviews.json?apiversion=5.4&Filter=ProductId:{product_id}&Include=Products&Limit=1&Passkey={_api_key}"
#     r_unformatted_json = url_reader(r_json_url)
#     return r_unformatted_json

# # print(review_extractor(product_id, _api_key))

# '''
# AVAILABILITY CHECKER
# '''

# def avaibility_checker(product_id, zip_code):
#     a_json_url = f"https://www.homedepot.com/mcc-cart/v3/appliance/deliveryAvailability/{product_id}/zipCode/{zip_code}"
#     a_unformatted_json = url_reader(a_json_url)
#     return a_unformatted_json

# # print(avaibility_checker(product_id, zip_code))


# """
# STORE LOCATOR
# finds closest store depending on latitude and longitude
# """
# latitude = 40.7128
# longitude = -74.0060
# _api_key2 = "MtNfr9rEWkRsxkc71IdtDBAp7E2p8GSy"

# def store_locator(latitude,longitude,api_key):
#     s_json_url = f"https://www.homedepot.com/StoreSearchServices/v2/storesearch?radius=50&latitude={latitude}&longitude={longitude}&key={api_key}&type=json&pagesize=40"
#     s_unformatted_json = url_reader(s_json_url)
#     return s_unformatted_json


# # print(store_locator(latitude,longitude,_api_key2))

# # def product_details_inventory():
# #     url = "https://www.homedepot.com/product-information/model"
# #     hdr = {"item_id": "308067442", "store_id": "6175"}

# #     req = urllib.request.Request(url, headers=hdr)
# #     response = urllib.request.urlopen(req)
# #     return response.read()

# # print(product_details_inventory())




# payload = {
# 	"operationName": "productClientOnlyProduct",
# 	"variables": {
# 		"skipSpecificationGroup": True,
# 		"itemId": "308067442",
# 		"storeId": "6175",
# 		"zipCode": "10001"
# 	},
# 	"query": "query productClientOnlyProduct($storeId: String, $zipCode: String, $itemId: String!, $dataSource: String, $skipSpecificationGroup: Boolean = false) {\n product(itemId: $itemId, dataSource: $dataSource) {\n fulfillment(storeId: $storeId, zipCode: $zipCode) {\n backordered\n fulfillmentOptions {\n type\n fulfillable\n services {\n type\n locations {\n isAnchor\n inventory {\n isLimitedQuantity\n isOutOfStock\n isInStock\n quantity\n isUnavailable\n maxAllowedBopisQty\n minAllowedBopisQty\n __typename\n }\n type\n storeName\n locationId\n curbsidePickupFlag\n isBuyInStoreCheckNearBy\n distance\n state\n storePhone\n __typename\n }\n deliveryTimeline\n deliveryDates {\n startDate\n endDate\n __typename\n }\n deliveryCharge\n dynamicEta {\n hours\n minutes\n __typename\n }\n hasFreeShipping\n freeDeliveryThreshold\n totalCharge\n __typename\n }\n __typename\n }\n anchorStoreStatus\n anchorStoreStatusType\n backorderedShipDate\n bossExcludedShipStates\n excludedShipStates\n seasonStatusEligible\n onlineStoreStatus\n onlineStoreStatusType\n inStoreAssemblyEligible\n __typename\n }\n itemId\n dataSources\n identifiers {\n canonicalUrl\n brandName\n itemId\n modelNumber\n productLabel\n storeSkuNumber\n upcGtin13\n specialOrderSku\n toolRentalSkuNumber\n upc\n isSuperSku\n parentId\n productType\n sampleId\n __typename\n }\n availabilityType {\n discontinued\n status\n type\n buyable\n __typename\n }\n details {\n description\n collection {\n url\n collectionId\n __typename\n }\n highlights\n __typename\n }\n media {\n images {\n url\n sizes\n type\n subType\n __typename\n }\n video {\n shortDescription\n thumbnail\n url\n videoStill\n link {\n text\n url\n __typename\n }\n title\n type\n videoId\n longDescription\n __typename\n }\n threeSixty {\n id\n url\n __typename\n }\n augmentedRealityLink {\n usdz\n image\n __typename\n }\n __typename\n }\n pricing(storeId: $storeId) {\n promotion {\n dates {\n end\n start\n __typename\n }\n type\n description {\n shortDesc\n longDesc\n __typename\n }\n dollarOff\n percentageOff\n savingsCenter\n savingsCenterPromos\n specialBuySavings\n specialBuyDollarOff\n specialBuyPercentageOff\n experienceTag\n subExperienceTag\n anchorItemList\n itemList\n reward {\n tiers {\n minPurchaseAmount\n minPurchaseQuantity\n rewardPercent\n rewardAmountPerOrder\n rewardAmountPerItem\n __typename\n }\n __typename\n }\n __typename\n }\n value\n alternatePriceDisplay\n alternate {\n bulk {\n pricePerUnit\n thresholdQuantity\n value\n __typename\n }\n unit {\n caseUnitOfMeasure\n unitsOriginalPrice\n unitsPerCase\n value\n __typename\n }\n __typename\n }\n original\n mapAboveOriginalPrice\n message\n specialBuy\n unitOfMeasure\n __typename\n }\n reviews {\n ratingsReviews {\n averageRating\n totalReviews\n __typename\n }\n __typename\n }\n seoDescription\n specificationGroup @skip(if: $skipSpecificationGroup) {\n specifications {\n specName\n specValue\n __typename\n }\n specTitle\n __typename\n }\n taxonomy {\n breadCrumbs {\n label\n url\n browseUrl\n creativeIconUrl\n deselectUrl\n dimensionName\n refinementKey\n __typename\n }\n brandLinkUrl\n __typename\n }\n favoriteDetail {\n count\n __typename\n }\n info {\n hidePrice\n ecoRebate\n quantityLimit\n sskMin\n sskMax\n unitOfMeasureCoverage\n wasMaxPriceRange\n wasMinPriceRange\n fiscalYear\n productDepartment\n classNumber\n forProfessionalUseOnly\n globalCustomConfigurator {\n customButtonText\n customDescription\n customExperience\n customExperienceUrl\n customTitle\n __typename\n }\n movingCalculatorEligible\n label\n recommendationFlags {\n visualNavigation\n __typename\n }\n replacementOMSID\n hasSubscription\n minimumOrderQuantity\n projectCalculatorEligible\n subClassNumber\n calculatorType\n isLiveGoodsProduct\n protectionPlanSku\n hasServiceAddOns\n consultationType\n __typename\n }\n sizeAndFitDetail {\n attributeGroups {\n attributes {\n attributeName\n dimensions\n __typename\n }\n dimensionLabel\n productType\n __typename\n }\n __typename\n }\n keyProductFeatures {\n keyProductFeaturesItems {\n features {\n name\n refinementId\n refinementUrl\n value\n __typename\n }\n __typename\n }\n __typename\n }\n badges(storeId: $storeId) {\n color\n creativeImageUrl\n endDate\n label\n message\n name\n timerDuration\n __typename\n }\n installServices {\n scheduleAMeasure\n __typename\n }\n subscription {\n defaultfrequency\n discountPercentage\n subscriptionEnabled\n __typename\n }\n __typename\n }\n}\n"
# }

# url = "https://www.homedepot.com/product-information/model?"

# r = requests.post(url,  json=payload)
# print(r)




    
