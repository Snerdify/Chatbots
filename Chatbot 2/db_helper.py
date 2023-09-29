import mysql.connector
global cnx

# cnx is used to store the connection to the MYSQL database.
# here the cnx is made global so that it can be accessed by all the functions in the script
# this allows multiple functions to use the same database connection

cnx = mysql.connector.connect (
    host="localhost",
    user = "root",
    password = "root"
    database = "pandeji_eatery" ) 


def insert_order_item():
    return ""


def insert_order_tracking():
    return ""

def get_total_order_price():
    return ""

def get_next_order_id():
    return ""

def get_order_status():
    return ""

if __name__ = "__main__" : 

    print(get_next_order_id())