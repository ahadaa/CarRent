
import mysql.connector
from prettytable import PrettyTable, from_db_cursor
import datetime
from  project2 import Customer,RentalCar
import random
connection = mysql.connector.connect(host='localhost',user='root',password='alanoud',db='carrent')
m = connection.cursor()

def main_menue():
    # to present starting menu
    print("#"*59)
    if datetime.datetime.now().hour < 12:
        print('       Good morning, Welcome to 4group For Cars Rental')
    elif datetime.datetime.now().hour > 12:
        print('       Good afternoon, Welcome to 4group For Cars Rental ')
    elif datetime.datetime.now().hour > 6:
        print('       Good evening, Welcome to 4group For Cars Rental ')
    print("\n      Experience the Thrill of the Road With Our Rentals\n") 
    print("#"*59+'\n\n')
    print("***********************************************************")
    print("\nHow Can We Help You?\n")  
    print("***********************************************************")
    print("\n(1) Rent Car.\n(2) Return Rental Car.\n(3) Exit.\n") 
    print("***********************************************************\n")

    user_choice = int(input("Please Select Service Number:\n"))
    return user_choice

def second_menue():
    # to present cars table
    ####################################
    m.execute("select Vehicle_id as Vehicle_ID , concat(Model,\"_\",model_year) as Model, price_Inhour as Price_In_Hour from carrent.stock;")
    mytable = from_db_cursor(m)
    print(mytable,'\n')
    ####################################
    car_id = int(input("Vehicle ID:\n"))

    return car_id

def calculate(Vehicle_ids):
    m.execute(f"select price_Inhour from carrent.stock where Vehicle_id = {Vehicle_ids}")
    price = m.fetchone()
    print("\n")
    print("For How Many Days You Would To Rent The Car?")
    print("(1) 12 Hour.")
    print("(2) 1 Day.")
    print("(3) 1 Week.")
    rent = int(input('Enter What Package You Want:\n'))
    final_price = 0
    if rent == 1:
        final_price = price[0] * 12
        return final_price, "12 Hour"
    elif rent == 2:
        final_price = price[0] * 24
        return final_price, "1 Day"
    else:
        final_price = price[0] * 168
        return final_price, "1 Week"
                
def cars_minue():
    ####################################
    m.execute("select Vehicle_id from carrent.stock")
    Vehicle_ids = m.fetchall()
    ####################################
    # to present table
    print("***********************************************************")
    print("\nCould You Please Choose Which Car Would You Like To Rent?\n")
    print("***********************************************************")
    ID = second_menue()
    while True:
        # check if Vehicle ID correct available
        if (any(ID in i for i in Vehicle_ids)):
            # check if vichel available
            m.execute(f"select availabilty from carrent.stock where Vehicle_id = {ID}")
            myresult = m.fetchone()
            if myresult[0] == 0: # he cann't rent 
                print('*'*5, "Sorry this Vehicle out of stock.",'*'*5)
                print("Would you like to:\n")
                print("(1) Choose another car.")
                print("(2) Exit.")
                u = int(input("Your choice:\n"))
                if u == 1:
                    cars_minue()
                else:
                    print("\n***********************************************************")
                    print("\nThanks For Using Our Application\nHave a Nice Day.\n")
                    print("***********************************************************")
                    break
            else:
                # add car ID & name list
                cars_id.append(ID) 
                price, day  = calculate(ID)
                m.execute(f"select Model from carrent.stock where Vehicle_id = {ID}")
                model = m.fetchone()
                model_name.append(model[0])
                cars_price.append(price)
                cars_day.append(day)
                print("***********************************************************")
                print("What would you like to do?\n(1) Confirm.\n(2) Rent another car.\n(3) Cancel.")
                selct = int(input("\nPlease choose:\n"))
                if selct == 1 :
                    # call rent class 
                    print("***********************************************************")
                    print("\nPlease full the form:")
                    global customer_name
                    customer_name = input("\nYour Full Name:\n")
                    while True:
                        try:
                            global customer_phone
                            customer_phone =int(input("Please Enter The Phone Number, No Spaces In Between: \n"))
                        except ValueError:
                            print("\n**************  Only numbers  **************\n")
                            continue
                        else:
                            phone=str(customer_phone)
                            if(len(phone)==9):
                                break
                            else:
                                print("\n**************  Your Phone Number Is Less Than 10  **************\n ")
                                continue
                    customer_total_car = len(cars_id)
                    print("\n***********************************************************")

                    print(f"\nDear {customer_name} your order is:\n")
                    for key,value in enumerate(cars_id):
                        print(f"-  Ordered Car: {model_name[key]}.")
                        print(f"-  Total: {cars_price[key]} SR, for {cars_day[key]}.\n")
                        global bill
                        bill =  random.getrandbits(20)
                        print(f"Your Bill Number is: {bill}")
                    print("***********************************************************")
                    return customer_name, customer_phone, customer_total_car
                elif selct == 2 :
                    cars_minue()
                elif selct == 3 :
                    print("\n***********************************************************")
                    print("\nThanks For Using Our Application\nHave a Nice Day.\n")
                    print("***********************************************************")
                    break
            break
        else:
            print("*** WRONG Vehicle ID ***")
            ID = int(input("Please enter Vehicle_id you would like to rent:\n"))

def main():
    global cars_id, model_name, cars_price, cars_day
    global model_name
    model_name = []
    cars_id = []
    cars_price = []
    cars_day = []
    user_choice = main_menue()
    if user_choice == 1:
        cars_minue()
        customer_ID = random.getrandbits(30)
        ourCustomer = Customer(customer_ID,customer_name,customer_phone)
        ourCustomer.create_account(len(cars_id), bill)
        for key, value in enumerate(cars_id):
            rental_car = RentalCar(value)
            rental_car.rental(customer_ID)
    if user_choice == 2:
        bill_number = int(input("Please Enter your bill number:\n"))
        m.execute(f"select  customer_name from carrent.customer where bill = {bill_number}")
        cust_name = m.fetchone()[0]
        print(f"Welcome {cust_name}, WE Are Happy To See You Again")
        print(f"Thanks for using our service:")
        m.execute(f"select  num_rented  from carrent.customer where bill = {bill_number}")
        total_rented = m.fetchone()[0]
        m.execute(f"select  bill  from carrent.customer where bill = {bill_number}")
        bill_number = m.fetchone()[0]
        print(f"You are Rented {total_rented} car|s, your bill # is({bill_number})")
        user_selection = int(input("Please Confirm:\n(1) Commit Retur.\n(2) Cancel.\n"))
        if user_selection == 1:
            m.execute(f"select  customer_id  from carrent.customer where bill = {bill_number}")
            customer_id = m.fetchone()[0]
            for i in range(total_rented):
                car_ID = int(input("Please, Enter Car ID:\n"))
                RentalCar(car_ID)
                RentalCar.return_car(customer_id, car_ID)
                print("Done, Successfuly Returned")
        else:
            print("Thank you.")
    elif user_choice == 3:
        print('\nThankyou for use our services\n')
 
    
if __name__ == "__main__":
    main()



