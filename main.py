from analyze_func import analyze_data_from_the_call,get_access_token,make_a_call
from product_class import constructor_product_instance
import database

#to load all data from .env
from dotenv import load_dotenv
load_dotenv()

#create the database
database.create_database()

#switch between sandbox or production environment
is_prod = True

#boolean to handle the read,deletion or creation requests
want_to_create_request = False
want_to_read_request = False
want_to_delete_request = False

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

#extract requests formated in [(request 1),(request 2),(request 3), ...] and transform each product in instances
# of the "Product" class with his attributes (name,price,option) to make easier manipulation and stock in a list
data_from_requests = database.extract_requests_from_db_table()
list_of_products = constructor_product_instance(data_from_requests)

#get an automatically token to make the API call
access_token = get_access_token(is_prod)
for each_product in list_of_products:

    data_from_the_call = make_a_call(access_token,is_prod,each_product.name)
    #en fonction de l'option 0 ou 1, créer 2 variante de la fonction analyze_data_from_the_call et rediriger vers celle ci
    analyze_data_from_the_call(data_from_the_call)
    

#3 - créer une alerte par rapport a une requete prix envoyé associé a un nom produit, analyser resultat (moyenne,min,max) puis stocker
#voir request,beautifulsoup et base SQL

#4 - configurer variable d 'environnement