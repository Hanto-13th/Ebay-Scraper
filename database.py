import sqlite3

def create_database():
    """Function to create database sqlite to stock user requests,
    a request build model is: 
    {"id"(handle automatically, used to identify request in DB),"product name","price to reach","option("SELL: 0 or "BUY: 1")","contact mail"}"""

    #open the DB and create table to stock user requests using the cursor
    with sqlite3.connect("Ebay Scraper.db") as connection:
        table = "CREATE TABLE IF NOT EXISTS user_requests (id INTEGER PRIMARY KEY AUTOINCREMENT," \
        "product TEXT NOT NULL," \
        "price INTEGER NOT NULL," \
        "option INTEGER NOT NULL," \
        "contact TEXT NOT NULL)"

        creation_cursor = connection.cursor()
        creation_cursor.execute(table)
        connection.commit()

def get_user_inputs(want_to_create_request):
    """Function to get the user inputs if he want to create a request,
    it take in argument the boolean voluntees for a request creation."""

    if want_to_create_request:
        #user input for request creation
        product_to_search = (input("Insert the object to search: ")).lower()
        price_to_reach = input("Insert the price to reach: ")
        option_buy_or_sell = input("Choose your options for this request (SELL: 0 or BUY: 1): ")
        user_mail_contact = (input("Enter your mail to recieve the results: ")).lower()

        #test if infos are formated allows
        try:
            price_to_reach = float(price_to_reach)
        except ValueError:
            print("Error: the value is not allowed, Only use integers or floating point numbers")
            exit(1)

        if option_buy_or_sell not in ("0", "1"):
            print("Error: the value is not allowed, Only use '0' for SELL option or '1' for BUY option")
            exit(1)
        
        return product_to_search,float(price_to_reach),int(option_buy_or_sell),user_mail_contact

def create_requests_into_db(product,price,option,contact):
        """Function to stock in DB the requests with user inputs, 
        take in arguments the name of product, the price to reach, the buy or sell option and the user mail contact."""

        #open the DB and stock user requests using the cursor
        with sqlite3.connect("Ebay Scraper.db") as connection:
            insertion_cursor = connection.cursor()
            insertion_cursor.execute("INSERT INTO user_requests (product, price, option, contact) VALUES (?, ?, ?, ?)",
                                     (product, price, option, contact))
            connection.commit()

def look_into_db_table():
    with sqlite3.connect("Ebay Scraper.db") as connection:
        insertion_cursor = connection.cursor()
        insertion_cursor.execute("SELECT * FROM user_requests")
        rows = insertion_cursor.fetchall()
        for row in rows:
            print(row)


