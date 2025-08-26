"""All the functions to analyze the data from the API response"""

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
            text_for_the_message = ""
            #if it's a product to sell
            if product_attributes.option == 0:
                median = sum(all_prices)//len(all_prices)
                median_min_value = median * 0.85
                median_max_value = median * 1.15
                text_for_the_message = f"TO_SELL:\n{min_value}\n{max_value}\n{median_value}"
                #check if the price is within ±15% of the reference value
                if median_min_value <= product_attributes.price_to_reach <= median_max_value:
                    product_attributes.days_in_a_row += 1
                else:
                    product_attributes.days_in_a_row = 0
                #if the price is within ±15% of the reference value during 5 days in a row, add an alert in the message
                if product_attributes.days_in_a_row == 5:
                    text_for_the_message += "!!! ALERT: THE PRICE HAS REACHED THE AMOUNT YOU WANT = YOU CAN SELL IT !!!\n"
                return text_for_the_message,product_attributes
            #if it's a product to buy
            elif product_attributes.option == 1:
                text_for_the_message = f"TO_BUY:\n{min_value}"
                #if the price is under the reference value, add an alert in the message
                if product_attributes.price_to_reach <= min(all_prices):
                    text_for_the_message += "!!! ALERT: THE PRICE HAS REACHED THE AMOUNT YOU WANT = YOU CAN BUY IT !!!\n"
                return text_for_the_message,product_attributes
            return results         
        return wrapper
    return decorator_buy_or_sell








        
 





    
    
