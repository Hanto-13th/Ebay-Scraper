import sqlite3

def decorate_for_handling_errors(func):
    def wrapper_func(*args, **kwargs):

        try: 
            results = func(*args, **kwargs)
        except sqlite3.IntegrityError as e:
            return {"success": False, "message": f"Integrity error: {str(e)}"}
        except sqlite3.OperationalError as e:
            return {"success": False, "message": f"Operational error: {str(e)}"}
        except sqlite3.DatabaseError as e:
            return {"success": False, "message": f"Database error: {str(e)}"}
        except sqlite3.Error as e:
            return {"success": False, "message": f"SQLite error: {str(e)}"}
        except Exception as e:
            return {"success": False, "message": f"Unexpected error: {str(e)}"}
        else:
            response = {"success": True, "message": "Task executed with success"}
            if results is not None:  
                response["results"] = results
            return response
        
    return wrapper_func


@decorate_for_handling_errors
def create_database():
    """Function to create database sqlite to stock user requests,
    a request build model is: 
    {"id"(handle automatically, used to identify request in DB),"product name","price to reach","option("SELL: 0 or "BUY: 1")","days_in_a_row (to see the days in a row the price is reached)"}"""

    #open the DB and create table to stock user requests using the cursor
    with sqlite3.connect("Ebay Scraper.db") as connection:
        table = "CREATE TABLE IF NOT EXISTS user_requests (id INTEGER PRIMARY KEY AUTOINCREMENT," \
        "product TEXT NOT NULL," \
        "price INTEGER NOT NULL," \
        "option INTEGER NOT NULL," \
        "days_in_a_row INTEGER NOT NULL)"

        creation_cursor = connection.cursor()
        creation_cursor.execute(table)
        connection.commit()

@decorate_for_handling_errors
def create_requests_into_db(product,price,option):
        """Function to stock in DB the requests with user inputs, 
        take in arguments the name of product, the price to reach, the buy or sell option"""

        #open the DB and stock user requests using the cursor
        with sqlite3.connect("Ebay Scraper.db") as connection:
            insertion_cursor = connection.cursor()
            insertion_cursor.execute("INSERT INTO user_requests (product, price, option, days_in_a_row) VALUES (?, ?, ?, ?)",
                                     (product, price, option, 0))
            connection.commit()

@decorate_for_handling_errors
def read_requests_into_db_table():
    """Function to read the table in DB."""
    
    with sqlite3.connect("Ebay Scraper.db") as connection:
        requests_lst = ""
        read_cursor = connection.cursor()
        read_cursor.execute("SELECT * FROM user_requests")
        rows = read_cursor.fetchall()
        for row in rows:
            requests_lst += f"Request ID: {row[0]}, Product: {row[1]}, Price to reach: {row[2]} euros, Buy or Sell Options: {"SELL" if row[3] == 0 else "BUY"}\n" 
        return requests_lst

@decorate_for_handling_errors
def delete_requests_into_db_table(id_to_delete):
    """Function to delete a row using his ID into the table."""

    with sqlite3.connect("Ebay Scraper.db") as connection:
        delete_cursor = connection.cursor()
        delete_cursor.execute("DELETE FROM user_requests WHERE id = (?)",(id_to_delete,))


@decorate_for_handling_errors
def delete_all_requests_into_db_table():
    with sqlite3.connect("Ebay Scraper.db") as connection:
        delete_cursor = connection.cursor()
        delete_cursor.execute("DELETE FROM user_requests")


@decorate_for_handling_errors
def extract_requests_from_db_table():
    """Function to extract the data table from DB."""

    with sqlite3.connect("Ebay Scraper.db") as connection:
        extraction_cursor = connection.cursor()
        extraction_cursor.execute("SELECT * FROM user_requests")
        extracted_data = extraction_cursor.fetchall()
        
        return extracted_data

@decorate_for_handling_errors
def update_product_attributes_into_db_table(attributes_product):
    with sqlite3.connect("Ebay Scraper.db") as connection:
        update_cursor = connection.cursor()
        update_cursor.execute("UPDATE user_requests SET days_in_a_row = (?) WHERE product = (?)",(attributes_product.days_in_a_row,attributes_product.name))










