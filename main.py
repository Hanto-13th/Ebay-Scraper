from dotenv import load_dotenv
from analyze_func import analyze_data_from_the_call,get_access_token,make_a_call,version_buy_or_sell
from product_class import constructor_product_instance
from discord_webhook import send_the_log
import database


#switch between sandbox or production environment
is_prod = True

#boolean to handle the read,deletion or creation requests
want_to_create_request = False
want_to_read_request = False
want_to_delete_request = False
want_to_delete_all_requests = False

def main():

    #to load all data from .env
    load_dotenv()

    #create the database
    database.create_database()

    #if the user wants to create a request, get his inputs and stock into DB
    if want_to_create_request:
        product_name,price_to_reach,buy_or_sell,user_mail_contact = database.get_user_inputs()
        database.create_requests_into_db(product_name,price_to_reach,buy_or_sell,user_mail_contact)

    #if the user wants to read the requests which exists in the DB
    if want_to_read_request:
        database.read_requests_into_db_table()

    #if the user wants to delete a request which exists in the DB
    if want_to_delete_request:
        database.read_requests_into_db_table()
        database.delete_requests_into_db_table()
    
    #if the user wants to delete all requests in DB
    if want_to_delete_all_requests:
        database.delete_all_requests_into_db_table()

    #extract requests formated in [(request 1),(request 2),(request 3), ...] and transform each product in instances
    # of the "Product" class with his attributes (name,price,option) to make easier manipulation and stock in a list
    data_from_requests = database.extract_requests_from_db_table()
    list_of_products = constructor_product_instance(data_from_requests)

    #get an automatically token to make the API call
    access_token = get_access_token(is_prod)

    all_the_text_to_send = ""
    #for each product from the users requests, make a call using the 'name' attribute in the object (instance of 'Product' class)
    # after analyze the results in a decorated function 'analyze_data_from_the_call' which take in decorated arg the 'option' attribute in the product object
    # and return based on your needs the min/max/median values (sell option) or just min value (buy option) converted in a string format
    for each_product in list_of_products:

        data_from_the_call = make_a_call(access_token,is_prod,each_product.name)

        decorate_analyze_data_from_the_call = version_buy_or_sell(each_product.option)(analyze_data_from_the_call)
        try:
            part_of_text_to_send = decorate_analyze_data_from_the_call(data_from_the_call)
        except Exception as exc:
            print(f"Error: problem during data analyze, move on to the next article ({exc})")
        all_the_text_to_send += part_of_text_to_send + "\n"
    
    #send the complete analyzed data from user requests 
    send_the_log(all_the_text_to_send)

    

    # - créer une alerte par rapport a la requete prix envoyé associé a un nom produit puis envoyer mail special quand atteint
    #(si buy option inferieur ou egal au prix et si sell option superieur ou egal au prix)
    

if __name__ == "__main__":
    main()

