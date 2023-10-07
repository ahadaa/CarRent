import mysql.connector 
from datetime import datetime 
from mysql import connector

# Customer class 
class Customer: 
    def __init__(self, customer_ID, customer_name, phone): 
        self.customer_ID = customer_ID 
        self.customer_name = customer_name 
        self.phone = phone 

    def create_account(self, rented_car_number, bill): 
        cnx = mysql.connector.connect(user='root', password='alanoud', host='localhost', database='carrent')
        cursor = cnx.cursor(buffered=True)
        VALUES = (self.customer_ID, self.phone, self.customer_name, rented_car_number,bill)
        query = f"INSERT INTO carrent.customer (customer_ID, Phone, customer_name, num_rented, bill ) VALUES {VALUES}"
        cursor.execute(query)
        cnx.commit()
        cnx.close()



class RentalCar: 
    def __init__(self, car_id): 
        self.car_id = car_id 
        

    def rental(self, customer_ID):
        date = datetime.now().date()
        rental_date = str(datetime.strftime(date,'%Y/%m/%d'))# '01/10/2009'#
        # Connect to the MySQL database 
        db = mysql.connector.connect( host="localhost", user="root", password="alanoud", database="carrent", autocommit= True ) 
        cursor = db.cursor()
        # To change availabilty and decrement it to 1
        cursor.execute(f"select availabilty from carrent.stock where Vehicle_id = {self.car_id}")
        ava = (cursor.fetchone()[0])-1
        cursor.execute(f"UPDATE stock SET availabilty = {ava} WHERE Vehicle_id ={self.car_id}") 
        # #######################################################################
        cursor.execute(f"UPDATE carrent.customer SET order_date = {rental_date} WHERE customer_ID = {customer_ID}" ) 
        #######################################################################
        cursor.execute(f"UPDATE carrent.customer SET status = \"renting\" WHERE customer_ID = {customer_ID}" )
        # Commit the changes and close the database connection 
        db.commit() 
        db.close() 

    def return_car(customer_ID, car_ID):
        
        date = datetime.now().date()
        return_date = str(datetime.strftime(date,'%Y/%m/%d'))# '01/10/2009'#
        db = mysql.connector.connect( host="localhost", user="root", password="alanoud", database="carrent", autocommit= True ) 
        cursor = db.cursor(buffered=True)
        # update stock number
        cursor.execute(f"select availabilty from carrent.stock where Vehicle_id = {car_ID}")
        ava = (cursor.fetchone()[0])+1
        cursor.execute(f"UPDATE stock SET availabilty = {ava} WHERE Vehicle_id ={car_ID}") 
        cursor.execute(f"UPDATE carrent.customer SET status = \"rented\" WHERE customer_ID = {customer_ID}" )
        cursor.execute(f"UPDATE carrent.customer SET return_date = {return_date} WHERE customer_ID = {customer_ID}" ) 
        
        db.commit() 
        db.close() 















































# import mysql.connector 
# from datetime import datetime 
# import random

# # Customer class 
# class Customer: 
#     def __init__(self, customer_ID, customer_name, phone): 
#         self.customer_ID = customer_ID 
#         self.customer_name = customer_name 
#         self.phone = phone 
#     def test(self):
#         print(self.customer_ID,self.customer_name, self.phone)       
#     def create_account(self, car_id, rental_date, return_date): 
#         rental_date = datetime.now()
#         return_date = datetime.now()# i will fixed based on user request
#         order_number = random.getrandbits(20)
#         # Connect to the MySQL database 
#         db = mysql.connector.connect( host="localhost", user="root", password="alanoud", database="rentcars" ) 
#         cursor = db.cursor() 
#         # Insert a new rental record into the database 
#         query = "INSERT INTO rentcars.customer_table (customer_ID, car_id, order_number, rental_date,  return_date) VALUES (%s, %s, %s, %s, %s)" 
#         values = (self.customer_ID, car_id, order_number,rental_date, return_date) 
#         cursor.execute(query, values) 
#         # close connection 
#         db.commit() 
#         db.close() 


# class RentalCar: 
#     # car  id, number of cars
#     def __init__(self, car_id, model, available): 
#         self.car_id = car_id 
#         self.model = model 
#         self.available = available

#     def rental(self, available): 
#         # Connect to the MySQL database 
#         db = mysql.connector.connect( host="localhost", user="root", password="alanoud", database="rentcars" ) 
#         cursor = db.cursor() 
#         # Update the availability of the car in the database
#         query = "UPDATE cars SET available = %s WHERE car_id = %s" 
#         values = (available, self.car_id) 
#         cursor.execute(query, values) 
#         # Commit the changes and close the database connection 
#         db.commit() 
#         db.close() 

#     def return_car():
#         pass