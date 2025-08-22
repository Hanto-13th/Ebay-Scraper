from . import database

#boolean to handle the read,deletion or creation requests
want_to_create_request = False
want_to_read_request = True
want_to_delete_request = False
want_to_delete_all_requests = False

def main():

    #create the database
    database.create_database()

    #if the user wants to create a request, get his inputs and stock into DB
    if want_to_create_request:
        product_name,price_to_reach,buy_or_sell = database.get_user_inputs()
        database.create_requests_into_db(product_name,price_to_reach,buy_or_sell)

    #if the user wants to read the requests which exists in the DB
    if want_to_read_request:
        requests_lst = database.read_requests_into_db_table()
        print(requests_lst)


    #if the user wants to delete a request which exists in the DB
    if want_to_delete_request:
        requests_lst = database.read_requests_into_db_table()
        print(requests_lst)
        id = input("choose an id: ")
        database.delete_requests_into_db_table(id)
    
    #if the user wants to delete all requests in DB
    if want_to_delete_all_requests:
        database.delete_all_requests_into_db_table()


if __name__ == "__main__":
    main()

