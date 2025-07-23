import json

def analyze_and_stock_data(data):
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
    for index,product in enumerate(all_products):
        item_attributes = {}
        item_attributes["title"] = product["title"]
        item_attributes["price"] = product["price"]
        item_attributes["condition"] = product["condition"]
        try:
            item_attributes["shippingOptions"] = product["shippingOptions"]
        except Exception as e:
            item_attributes["pickupOptions"] = product["pickupOptions"]
        item_attributes["itemWebUrl"] = product["itemWebUrl"]
        item_attributes["itemCreationDate"] = product["itemCreationDate"]
        #stock the dict with info of each product in the file "results.json"
        product_to_stock = json.dumps(item_attributes,indent=4)
        with open("results.json", "a") as file:
            file.write(f"{index}: {product_to_stock}\n")





    
    
