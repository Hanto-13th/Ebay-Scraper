import requests
import os
from base64 import b64encode
from urllib.parse import quote

"""All the functions to handle the call of Ebay API"""

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
    try:
        authentification = requests.post(f"https://{auth_endpoint}/identity/v1/oauth2/token", headers=auth_headers, data=auth_data,timeout=(5, 30))
    except requests.exceptions.ConnectionError:
        return None,{"success": False, "message": "Impossible to contact the server, verify the Flask connection"}
    except (requests.exceptions.ConnectTimeout,requests.exceptions.ReadTimeout):
        return None,{"success": False, "message": "The Flask server is taking too long to respond"}
    #handle if the call missed
    if authentification.status_code != 200:
        error_message = authentification.json()
        return None,error_message
    #get the access token from the response
    access_token = authentification.json().get("access_token")
    return access_token,{"success": True, "message": "Message sent successfully!"}


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

    #try to recieve a category ID for the product name to include in the URL call
    category_suggestions = []
    category_id = None
    try:
        tree = requests.get(f"https://{endpoint}/commerce/taxonomy/v1/get_default_category_tree_id?marketplace_id=EBAY_FR",headers=call_headers,timeout=(5, 30))
        category_tree_id = tree.json()["categoryTreeId"]
        suggestions = requests.get(f"https://{endpoint}/commerce/taxonomy/v1/category_tree/{category_tree_id}/get_category_suggestions?q={product_name}",headers=call_headers,timeout=(5, 30))
        category_suggestions = suggestions.json().get("categorySuggestions", [])
    except (requests.exceptions.ConnectionError,requests.exceptions.ConnectTimeout,requests.exceptions.ReadTimeout,ValueError):
        category_suggestions = []

    #if they are a suggestion, run the call with for a better precision of search else run without
    if category_suggestions:
        first_category = category_suggestions[0]['category']
        category_id = first_category['categoryId']
    try:
        response = requests.get(f"https://{endpoint}/buy/browse/v1/item_summary/search?q={product_name}&limit=12&offset=0&filter={encoded_filter}&category_ids={category_id}" \
                                if category_suggestions else \
                                f"https://{endpoint}/buy/browse/v1/item_summary/search?q={product_name}&limit=12&offset=0&filter={encoded_filter}", headers = call_headers,timeout=(5, 30))
    except requests.exceptions.ConnectionError:
        return None,{"success": False, "message": "Impossible to contact the server, verify the Flask connection"}
    except (requests.exceptions.ConnectTimeout,requests.exceptions.ReadTimeout):
        return None,{"success": False, "message": "The Flask server is taking too long to respond"}
    #handle if the call missed
    if response.status_code != 200:
        try:
            error_message = response.json()
        except ValueError:
            error_message = {"success": False, "message": "Invalid JSON from server"}
        return None,error_message
    #get only the "products characterestics" part of data
    product_characteristics_data = response.json().get("itemSummaries")
    return product_characteristics_data,{"success": True, "message": "Message sent successfully!"}



    
    


    
