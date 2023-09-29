import mysql.connector
global cnx

# cnx is used to store the connection to the MYSQL database.
# here the cnx is made global so that it can be accessed by all the functions in the script
# this allows multiple functions to use the same database connection

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="pandeyji_eatery"
)


# function that handles adding an order item
def insert_order_item(food_item, quantity, order_id):
    # cursor is a database object that is used to interact with the database
    # it is used to execute SQL queries , fetch query results , manage transactions
    try:
        cursor = cnx.cursor()
# a "stored-procedure" is a pre-defined database routine
# here we use callproc named insert_order_item by using sql cursor
# the stored procedure takes three items, and stores them as a tuple
        cursor.callproc("insert_order_item",(food_item,quantity,order_id))
# after inserting an item , we commit the changes in the databse to ensure that 
# the changes are permanently saved
        cursor.commit()
# its important to close the cursor after the operation is complete
        cursor.close()
        print("Item successfully inserted")
        return 1
    
#  If an error of type sql.connector.Error occurs , below code executed. 
# we print an error msg whilst giving the info about what the msg is , 
#and rollback the changes
    except mysql.connector.Error as err:
        print(f"Error inserting an item: {err}")

        # if any changes have been made that are incorrect
        cnx.rollback()
        return -1
# if any other changes other than mysql.connector.Error occur , then below code is executed
    except Exception as e:
        print(f"An error occured:{e}")
        cnx.rollback()
        return -1


def insert_order_tracking():
    return ""

def get_total_order_price():
    return ""

def get_next_order_id():
    return ""

def get_order_status():
    return ""

if __name__ == "__main__" : 

    print(get_next_order_id())