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



# this function is used to add a new record into order_tracking table.
def insert_order_tracking(order_id, status):
    cursor = cnx.cursor()
    # insert value in the order_tracking table
    insert_query= "INSERT INTO order_tracking (order_id, status) VALUES (%s,%s)"
    cursor.execute(insert_query , (order_id , status))
    cnx.commit()
    cursor.close()


# fetch the total price of a specific order from the database 
def get_total_order_price(order_id):
    cursor=cnx.cursor()
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)
    result= cursor.fetchone()[0]
    return result





# could be mainly used to generate order_id for the new item
# also could be used to retrieve the next order id in the db
def get_next_order_id():
    cursor = cnx.cursor
    # MAX is an aggregate value in SQL. we want to get the max value of the order_id from the orders table
    # we need to select the max order_id in the orders table to get a unique identifier to be 
    # most of the times order ids are arranged in sequential manners, so getting the max order id refers to getting the 
    # id of the latest order.
    query= "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    if result is None:
        return 1
    else:
        return result+1



# we need to get the status of an order from sql db , provided that we have an order id
def get_order_status(order_id):
    cursor= cnx.cursor()
    query= f"SELECT status FROM order_tracking WHERE order_id={order_id}"
    cursor.execute(query)
    # method to retrieve the first row of the query result.
    result = cursor.fetchone()
    # closing the cursor is necessary to release db resources
    cursor.close()
    # return the order status
    if result:
        # if the query has a positive match then , return the 1st element of the result
        return result[0]
    else:
        return None



if __name__ == "__main__" : 

    print(get_next_order_id())