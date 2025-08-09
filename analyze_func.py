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


def analyze_data_from_the_call(all_articles_from_the_call):
    """The function will take all the articles from the call and search the median of products values and the min/max values of products,
    and format him in string,
    it take in argument all the 'itemSummaries' part in articles dict from the API call which contains each product characacteristics"""

    min_value = float("+inf")
    max_value = float("-inf")
    all_price_for_median = []

    for article in all_articles_from_the_call:

        #if the article has a FIXED PRICE and not AUCTIONS PRICE
        if "price" in article and not "currentBidPrice" in article:
            value_price = float(article['price'].get('value'))
            all_price_for_median.append(value_price)
            if value_price > max_value:
                max_value = value_price
                title_max = f"Title: {article['title']}"
                url_max = f"URL: {article['itemWebUrl']}"
                fixed_price_max = f"Fixed Price: {article['price'].get('value')}"
                auction_price_max = "Auction Price: Any"
            if value_price < min_value:
                min_value = value_price
                title_min = f"Title: {article['title']}"
                url_min = f"URL: {article['itemWebUrl']}"
                fixed_price_min = f"Fixed Price: {article['price'].get('value')}"
                auction_price_min = "Auction Price: Any"

        #if the article has not FIXED PRICE but an AUCTIONS PRICE
        elif not "price" in article and "currentBidPrice" in article:
            value_bid = float(article['currentBidPrice'].get('value'))
            all_price_for_median.append(value_bid)
            if value_bid > max_value:
                max_value = value_bid
                title_max = f"Title: {article['title']}"
                url_max = f"URL: {article['itemWebUrl']}"
                auction_price_max = f"Auction Price: {article['currentBidPrice'].get('value')}"
                fixed_price_max = "Fixed Price: Any"
            if value_bid < min_value:
                min_value = value_bid
                title_min = f"Title: {article['title']}"
                url_min = f"URL: {article['itemWebUrl']}"
                auction_price_min = f"Auction Price: {article['currentBidPrice'].get('value')}"
                fixed_price_min  = "Fixed Price: Any"
        
        #if the article has a FIXED PRICE and an AUCTIONS PRICE
        else:
            value_price = float(article['price'].get('value'))
            value_bid = float(article['currentBidPrice'].get('value'))
            all_price_for_median.append(value_bid)
            if value_bid > max_value:
                max_value = value_bid
                title_max = f"Title: {article['title']}"
                url_max = f"URL: {article['itemWebUrl']}"
                fixed_price_max = f"Fixed Price: {article['price'].get('value')}"
                auction_price_max = f"Auction Price: {article['currentBidPrice'].get('value')}"
            if value_bid < min_value:
                min_value = value_bid
                title_min = f"Title: {article['title']}"
                url_min = f"URL: {article['itemWebUrl']}"
                fixed_price_min = f"Fixed Price: {article['price'].get('value')}"
                auction_price_min = f"Auction Price: {article['currentBidPrice'].get('value')}"

        #format each min/max in string
        product_min_value = f"{title_min}\n" + f"{fixed_price_min}" + f" {auction_price_min}" + f"\n{url_min}\n"
        product_max_value = f"{title_max}\n" + f"{fixed_price_max}" + f" {auction_price_max}" + f"\n{url_max}\n"

    #compute the median
    product_median = f"Products Median: {sum(all_price_for_median)//len(all_price_for_median)}\n"
    #print(sorted(all_price_for_median),median)
    return product_median,product_min_value,product_max_value,all_price_for_median


def version_buy_or_sell(product_attributes):
    """Just a function to decorate 'analyze_data_from_the_call' based on the buy or sell options of each product and return only the data we need"""
    def decorator_buy_or_sell(func):
        def wrapper(iterable):
            results = func(iterable)
            median_value,min_value,max_value,all_prices = results
            text_for_the_mail = ""
            if product_attributes.option == 0:
                median = sum(all_prices)//len(all_prices)
                median_min_value = median * 0.85
                median_max_value = median * 1.15
                text_for_the_mail = f"TO_SELL:\n{min_value}\n{max_value}\n{median_value}"
                if median_min_value <= product_attributes.price_to_reach >= median_max_value:
                    product_attributes.days_in_a_row += 1
                if product_attributes.days_in_a_row == 5:
                    text_for_the_mail += "!!! ALERT: THE PRICE HAS REACHED THE AMOUNT YOU WANT = YOU CAN SELL IT !!!\n"
                return text_for_the_mail
            elif product_attributes.option == 1:
                text_for_the_mail = f"TO_BUY:\n{min_value}"
                if product_attributes.price_to_reach <= min(all_prices):
                    text_for_the_mail += "!!! ALERT: THE PRICE HAS REACHED THE AMOUNT YOU WANT = YOU CAN BUY IT !!!\n"
                return text_for_the_mail
            return results         
        return wrapper
    return decorator_buy_or_sell








        
 





    
    
