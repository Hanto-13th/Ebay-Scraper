class Product():
    #create a class to transform each request product in object with attributes 
    def __init__(self,name,price_to_reach,option,days_in_a_row):
        self.name = name
        self.price_to_reach = price_to_reach
        self.option = option
        self.days_in_a_row = days_in_a_row


def constructor_product_instance(data_from_requests):
    """Function to automate the transformation of each product in object.
    It takes in argument the data formated in list."""
    list_of_instances = []
    for product in data_from_requests:
        new_instance = Product(product[1],product[2],product[3],product[4])
        list_of_instances.append(new_instance)

    return list_of_instances
    

