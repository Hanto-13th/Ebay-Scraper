class Product():
    def __init__(self,name,price_to_reach,option):
        self.name = name
        self.price_to_reach = price_to_reach
        self.option = option


def constructor_product_instance(data_from_requests):
    list_of_instances = []
    for product in data_from_requests:
        new_instance = Product(product[1],product[2],product[3])
        list_of_instances.append(new_instance)

    return list_of_instances
    

