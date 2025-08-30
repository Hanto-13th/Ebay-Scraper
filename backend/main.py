from flask import Flask, request, jsonify
import db.database as database
from backend.product_class import constructor_product_instance
from . import analyze_func 
from . import discord_webhook
from . import ebay_call

"""The main file for all the backend management"""


#############################
#  ______ _           _    
# |  ____| |         | |   
# | |__  | | __ _ ___| | __
# |  __| | |/ _` / __| |/ /
# | |    | | (_| \__ \   < 
# |_|    |_|\__,_|___/_|\_\
#
#############################

app = Flask(__name__)

#create the database if not already created
database.create_database()

#handle all the route for the Flask server and return a success or not message in JSON
@app.route('/create_requests_into_db',methods = ['POST'])
def creation_requests():
    data = request.get_json()
    product_name = data.get("product_name")
    price_to_reach = data.get("price")
    buy_or_sell = data.get("option")
    response = database.create_requests_into_db(product_name,price_to_reach,buy_or_sell)
    return jsonify(response)

@app.route('/read_requests_into_db_table',methods = ['GET'])
def read_requests():
    response = database.read_requests_into_db_table()
    return jsonify(response)

@app.route('/delete_requests_into_db_table',methods = ['POST'])
def deletion_requests():
    data = request.get_json()         
    request_id = data.get("id") 
    response = database.delete_requests_into_db_table(request_id)
    return jsonify(response)

@app.route('/delete_all_requests_into_db_table',methods = ['POST'])
def deletion_all_requests():
    response = database.delete_all_requests_into_db_table()
    return jsonify(response)

@app.route('/run_full_ebay_process',methods = ['POST'])
def run_full_ebay_process(is_prod = True):
    
    #the message we compare along the process to check if nothing goes wrong 
    message_success_or_fail = {"success": True, "message": "Message sent successfully!"}


    #get an automatically token to make the API call
    access_token,error_message = ebay_call.get_access_token(is_prod)
    if message_success_or_fail != error_message:
        message_success_or_fail = error_message
        return jsonify(message_success_or_fail)
    
    #extract requests formated in [(request 1),(request 2),(request 3), ...] and transform each product in instances
    # of the "Product" class with his attributes (name,price,option) to make easier manipulation and stock in a list
    data_from_requests = database.extract_requests_from_db_table()
    if data_from_requests["success"] == False:
        return jsonify(data_from_requests)
    list_of_products = constructor_product_instance(data_from_requests["results"])

    all_the_text = ""
    untreated_data = 0
    #for each product from the users requests, make a call using the 'name' attribute in the object (instance of 'Product' class)
    # after analyze the results in a decorated function 'analyze_data_from_the_call' which take in decorated arg the attributes in the product object
    # and return based on your needs the min/max/median values (sell option) or just min value (buy option) converted in a string format to send message
    for each_product in list_of_products:

        data_from_the_call,error_message = ebay_call.make_a_call(access_token,is_prod,each_product.name)
        if message_success_or_fail != error_message:
            message_success_or_fail = error_message
            return jsonify(message_success_or_fail)
        
        decorate_analyze_data_from_the_call = analyze_func.version_buy_or_sell(each_product)(analyze_func.analyze_data_from_the_call)
        try:
            part_of_text,new_product_attributes = decorate_analyze_data_from_the_call(data_from_the_call)
            database.update_product_attributes_into_db_table(new_product_attributes)
        except Exception:
            untreated_data += 1
            continue
            
        all_the_text += part_of_text+ "\n"
    
    #render the message for more lisibility
    all_the_text_rendered = discord_webhook.render_message(all_the_text)
    #truncate the message each 2000 chars and return the message slice in a list
    message = discord_webhook.truncate_the_longest_msg(all_the_text_rendered)
        
    #send the complete analyzed data from user requests (truncated if need)
    error_message = discord_webhook.send_the_data(message)
    if message_success_or_fail != error_message:
        message_success_or_fail = error_message
        return jsonify(message_success_or_fail)

    #add the untreated data if they are
    message_success_or_fail["untreated_data"] = untreated_data
    return jsonify(message_success_or_fail)


if __name__ == "__main__":
    app.run()