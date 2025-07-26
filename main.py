from analyze_func import analyze_data,get_access_token,make_a_call
from database import create_database,create_requests_into_db,get_user_inputs,look_into_db_table
from dotenv import load_dotenv
load_dotenv()


create_database()

want_to_create_request = True

product_name,price_to_reach,buy_or_sell,user_mail_contact = get_user_inputs(want_to_create_request)
if want_to_create_request:
    create_requests_into_db(product_name,price_to_reach,buy_or_sell,user_mail_contact)

look_into_db_table()

#Change between sandbox or production environment
is_prod = True

access_token = get_access_token(is_prod)
data = make_a_call(access_token,is_prod)

#call the function to get and stock only the data I need
analyze_data(data)


#3 - créer une alerte par rapport a une requete prix envoyé associé a un nom produit, analyser resultat (moyenne,min,max) puis stocker
#voir request,beautifulsoup et base SQL

#4 - configurer variable d 'environnement