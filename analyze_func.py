import requests
import os
from base64 import b64encode
import json



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

def make_a_call(access_token,production_env_enable):
    """Function to make a API call with the access token,
    it take in argument the access token and the boolean activation of production environment."""

     #load the call headers with the Access Token
    call_headers = {"Authorization":f"Bearer {access_token}", 
    "X-EBAY-C-MARKETPLACE-ID":"EBAY_FR",
    "X-EBAY-C-ENDUSERCTX":"affiliateCampaignId=<ePNCampaignId>,affiliateReferenceId=<referenceId>"}

    #get the HTTP endpoint to make a call 
    endpoint = os.getenv("PROD_AUTH_ENDPOINT" if production_env_enable else "SAND_AUTH_ENDPOINT")

    #get a response from the "search" API with the call headers
    response = requests.get(f"https://{endpoint}/buy/browse/v1/item_summary/search?q=iphone&limit=3&offset=0", headers = call_headers)

    #handle if the call missed
    if response.status_code == 200:
    #receive a formated JSON string
        data = response.text
        return data
    else:
        print(f"Error retrieving data, status code: {response.status_code}")


def analyze_data(data):
    """Function which take the data to analyze and get only the informations we needed,
    after stock this infos in a dict and convert him in JSON to stock on a file 'results.json'.

    It takes in argument the data we want analyze formated in python dictionnaries."""

    #open a json file to stock the non sorted data temporarily and convert into python dict
    with open("data.json","w") as file:
        file.write(f"{data}\n")
    with open("data.json", "r") as file:
        data_to_analyze = json.load(file)
    #get only the products characterestics part of data
    all_products = data_to_analyze.get("itemSummaries")
    #create the file to stock and clear him for each call
    with open("results.json", "w") as file:
            file.write("")
    #iterate on each product and stock the info we needed in a dict
    item_attributes = ["title","price","condition","shippingOptions","pickupOptions","itemWebUrl","itemCreationDate"]
    for index,product in enumerate(all_products):
        infos_to_stock = {}
        for attribute in item_attributes:
             if attribute in product:
                  infos_to_stock[attribute] = product[attribute]
        #stock the dict with info of each product in the file "results.json"
        product_to_stock = json.dumps(infos_to_stock,indent=4)
        with open("results.json", "a") as file:
            file.write(f"{index}: {product_to_stock}\n")





    
    
