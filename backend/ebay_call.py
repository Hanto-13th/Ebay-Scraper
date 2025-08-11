import requests
import os
from base64 import b64encode
from urllib.parse import quote

def get_access_token(production_env_enable):
    """Function to get the access token from Ebay endpoint to make a API call (client ID and client secret ID, watch the .env),
    it take in argument the boolean activation of production environment."""

     #recuperation of authentification ID from .env and encode them
    client_id = os.getenv("PROD_EBAY_CLIENT_ID" if production_env_enable else "SAND_EBAY_CLIENT_ID")
    client_secret = os.getenv("PROD_EBAY_CLIENT_SECRET" if production_env_enable else "SAND_EBAY_CLIENT_SECRET")
    basic_auth = b64encode(f"{client_id}:{client_secret}".encode()).decode()

    #load the authentification headers with the encoded ID
    auth_headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": f"Basic {basic_auth}"}

    auth_data = {
    "grant_type": "client_credentials",
    "scope": "https://api.ebay.com/oauth/api_scope"}

    #get the HTTP endpoint to get the Access Token
    auth_endpoint = os.getenv("PROD_AUTH_ENDPOINT" if production_env_enable else "SAND_AUTH_ENDPOINT")

    #with the headers loaded with auth ID, post a request to get a Access Token to call API
    authentification = requests.post(f"https://{auth_endpoint}/identity/v1/oauth2/token", headers=auth_headers, data=auth_data)
    access_token = authentification.json().get("access_token")

    return access_token

def make_a_call(access_token,production_env_enable,product_name):
    """Function to make a API call with the access token,
    it take in argument the access token and the boolean activation of production environment."""

    #load the call headers with the Access Token
    call_headers = {"Authorization":f"Bearer {access_token}", 
    "X-EBAY-C-MARKETPLACE-ID":"EBAY_FR",
    "X-EBAY-C-ENDUSERCTX":"affiliateCampaignId=<ePNCampaignId>,affiliateReferenceId=<referenceId>"}

    #get the HTTP endpoint to make a call 
    endpoint = os.getenv("PROD_AUTH_ENDPOINT" if production_env_enable else "SAND_AUTH_ENDPOINT")
    #encode the filter "{AUCTION|FIXED_PRICE}" to make the call
    encoded_filter = quote('buyingOptions:{AUCTION|FIXED_PRICE}')


    #get a response from the "search" API with the call headers (a JSON string)
    response = requests.get(f"https://{endpoint}/buy/browse/v1/item_summary/search?q={product_name}&limit=12&offset=0&filter={encoded_filter}", headers = call_headers)

    #handle if the call missed
    if response.status_code == 200:
        #convert the JSON string in python dict (JSON format)
        data = response.json()
        #get only the "products characterestics" part of data
        product_characacteristics_data = data.get("itemSummaries")
        return product_characacteristics_data
    else:
        print(f"Error retrieving data, status code: {response.status_code}")
