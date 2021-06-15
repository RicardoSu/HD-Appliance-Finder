import urllib
import requests
import json

def url_decoder(url_encoded):
    # uses urllib to open json file and read
    with urllib.request.urlopen(url_encoded) as url:
        # decodes json file
        json_response = json.loads(url.read().decode())

    return json_response


appliance_url = f"https://api.bazaarvoice.com/data/reviews.json?apiversion=5.4&Filter=ProductId:309731132&Include=Products&Limit=1&Passkey=u2tvlik5g1afeh78i745g4s1d"

#uses url decode function to loop through url and extract data
print(url_decoder(appliance_url))

