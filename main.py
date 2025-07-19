import requests
import os
from base64 import b64encode

#user input to make the call (object name, limit of search ...)
object_to_search = input("Insert the object to search: ")
limit_of_search= input("Fix a limit of object to view: ")

#recuperation of authentification ID from .env and encode them //Change between sandbox or production
client_id = os.getenv("PROD_EBAY_CLIENT_ID")
client_secret = os.getenv("PROD_EBAY_CLIENT_SECRET")
basic_auth = b64encode(f"{client_id}:{client_secret}".encode()).decode()

#load the authentification headers with the encoded ID
auth_headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {basic_auth}"
}

auth_data = {
    "grant_type": "client_credentials",
    "scope": "https://api.ebay.com/oauth/api_scope"
}

#get the HTTP endpoint to get the Access Token or make a call //Change between sandbox or production
auth_endpoint = os.getenv("PROD_AUTH_ENDPOINT")

#with the headers loaded with auth ID, post a request to get a Access Token to call API
authentification = requests.post(f"https://{auth_endpoint}/identity/v1/oauth2/token", headers=auth_headers, data=auth_data)
access_token = authentification.json().get("access_token")

#load the call headers with the Access Token
call_headers = {"Authorization":f"Bearer {access_token}", 
"X-EBAY-C-MARKETPLACE-ID":"EBAY_FR",
"X-EBAY-C-ENDUSERCTX":"affiliateCampaignId=<ePNCampaignId>,affiliateReferenceId=<referenceId>"}

#get a response from the "search" API with the call headers
response = requests.get(f"https://{auth_endpoint}/buy/browse/v1/item_summary/search?q={object_to_search}&limit={limit_of_search}&sort=price", headers = call_headers)

print(response.json())


#2- analyser résultat et stocker
#voir beautifulsoup + base SQL ?

#3 - créer une alerte par rapport a une requete prix envoyé associé a un nom produit, analyser resultat (moyenne,min,max) puis stocker
#voir request,beautifulsoup et base SQL

#4 - configurer variable d 'environnement