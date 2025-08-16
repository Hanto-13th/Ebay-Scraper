from flask import Flask,request
import db.database as database
from backend.product_class import constructor_product_instance
from . import analyze_func 
from . import discord_webhook
from . import ebay_call


app = Flask(__name__)

@app.route('/create_database',methods = ['POST'])
def creation_database():
    database.create_database()
    return "Database Created"


@app.route('/create_requests_into_db',methods = ['POST'])
def creation_requests():
    product_name,price_to_reach,buy_or_sell = request.get_json()
    database.create_requests_into_db(product_name,price_to_reach,buy_or_sell)
    return "Requests Created"

@app.route('/read_requests_into_db_table',methods = ['GET'])
def read_requests():
    requests_list = database.read_requests_into_db_table()
    return requests_list

@app.route('/delete_requests_into_db_table',methods = ['POST'])
def deletion_requests():
    database.read_requests_into_db_table()
    database.delete_requests_into_db_table()
    return "Requests Deleted"

@app.route('/delete_all_requests_into_db_table',methods = ['POST'])
def deletion_all_requests():
    database.delete_all_requests_into_db_table()
    return "All Requests Deleted"

@app.route('/run_full_ebay_process',methods = ['POST'])
def run_full_ebay_process(is_prod = True):

    #get an automatically token to make the API call
    access_token = ebay_call.get_access_token(is_prod)

    #extract requests formated in [(request 1),(request 2),(request 3), ...] and transform each product in instances
    # of the "Product" class with his attributes (name,price,option) to make easier manipulation and stock in a list
    data_from_requests = database.extract_requests_from_db_table()
    list_of_products = constructor_product_instance(data_from_requests)

    all_the_text = ""
        #for each product from the users requests, make a call using the 'name' attribute in the object (instance of 'Product' class)
        # after analyze the results in a decorated function 'analyze_data_from_the_call' which take in decorated arg the 'option' attribute in the product object
        # and return based on your needs the min/max/median values (sell option) or just min value (buy option) converted in a string format
    for each_product in list_of_products:

        data_from_the_call = ebay_call.make_a_call(access_token,is_prod,each_product.name)

        decorate_analyze_data_from_the_call = analyze_func.version_buy_or_sell(each_product)(analyze_func.analyze_data_from_the_call)
        try:
            part_of_text,new_product_attributes = decorate_analyze_data_from_the_call(data_from_the_call)
            database.update_product_attributes_into_db_table(new_product_attributes)
        except Exception as exc:
            print(f"Error: problem during data analyze, move on to the next article ({exc})")
            continue
            
        all_the_text += part_of_text+ "\n"
    
    #render the message fro more lisibility
    all_the_text_rendered = discord_webhook.render_message(all_the_text)
    #truncate the message each 2000 chars and return the message slice in a list
    message = discord_webhook.truncate_the_longest_msg(all_the_text_rendered)
        
    #send the complete analyzed data from user requests (truncated if need)
    discord_webhook.send_the_data(message)

    return "Process completed successfully"


if __name__ == "__main__":
    app.run()