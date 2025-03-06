# **************************** SQL ***************************

# CREATE DATABASE activa_rental_system;
#
# USE activa_rental_system;
#
# CREATE TABLE customers (
#     c_id INT AUTO_INCREMENT PRIMARY KEY,
#     c_name VARCHAR(50),
#     phone_no BIGINT,
#     address VARCHAR(100),
#     aadhar_no VARCHAR(12) UNIQUE,
#     driving_license VARCHAR(20)
# );

# CREATE TABLE rentals (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     customer_id INT,
#     no_of_activa INT,
#     days INT,
#     bill DECIMAL(10 , 2 ),
#     status ENUM('Pending', 'Returned') DEFAULT 'Pending',
#     FOREIGN KEY (customer_id)
#         REFERENCES customers (c_id)
# );

# ************************** PYTHON CODE **************************************

# ACTIVA RENTAL SYSTEM

import mysql.connector as mys

def connect_db():
    return mys.connect(
        username = "root",
        password = "1234",
        host = "localhost",
        database = "activa_rental_system"
    )


# Main Function
def main():
    print("******Welcome to Cyber Success Activa Rental House! ******")
    print("\nNo. of Activa Available: 20")
    while True:
        print("\n1. Rent\n2. Return\n3. Owner Access\n4. Exit")
        choice = input("Choose an Option: ")
        if choice == "1":
            rent_activa()
        elif choice == "2":
            return_activa()
        elif choice == "3":
            owner_access()
        elif choice == "4":
            print("Thank You For Visiting !!!")
            break
        else:
            print("Invalid choice. Please try again....")

# RentActiva function
def rent_activa():
    print("*****Welcome to Rent *****")
    print("T&C: \n1. Aadhar Card is Mandatory.\n2. Driving Licence is Mandatory.\n3. One Activa for One Day: 500/- ")

    confirm= input("Confirm (y/n): ").lower()
    if confirm != 'y':
        return

    no_of_activa = int(input("Enter No of Activas: "))
    if no_of_activa <= 0:
        print("Invalid number of Activas..")
        return

    conn = connect_db()
    cur = conn.cursor()

    name = input("Enter your Name: ")
    phone = int(input("Enter your Phone no.: "))
    address = input("Enter your Address: ")
    aadhar = int(input("Enter your Aadhar no.: "))
    licence = input("Enter your Driving Licence no.: ")
    days = int(input("Enter your number of days for booking: "))
    bill = no_of_activa * days * 500
    print(f"Total Bill is: {bill}")

    final_confirm = input("Confirm (y/n): ").lower()
    if final_confirm == 'y':
        try:
            cur.execute("Insert INTO customers (c_name,phone_no,address,aadhar_no,driving_license) VALUES(%s, %s, %s, %s, %s)",
                        (name,phone,address,aadhar,licence))
            customer_id = cur.lastrowid

            cur.execute("INSERT INTO rentals (customer_id, no_of_activa,days,bill) VALUES(%s, %s, %s, %s)",
                        (customer_id, no_of_activa,days,bill))
            conn.commit()
            print("****** Successfully Booking ******")


            with open(f"{name}_bill.text","w") as bill_file:
                bill_file.write(f"Name: {name}\nPhone: {phone}\nTotal Bill: {bill}\n")
                print("Bill Saved To text file..")

        except:
            print("ERROR!!")
            conn.rollback()
    else:
        print("Booking Cancelled..")

    cur.close()
    conn.close()


# Return Activa Function
def return_activa():
    print("****** Welcome to Return ******")
    aadhar = input("Enter your Aadhar No: ")

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT c_id FROM customers WHERE aadhar_no = %s",(aadhar,))
    result = cur.fetchone()

    if result:
        customer_id = result[0]
        cur.execute("select no_of_activa from rentals where customer_id = %s AND status = 'Pending'",(customer_id,))
        rental = cur.fetchone()

        if rental:
            no_of_activa_rented = rental[0]
            no_of_return = int(input("No of Activa Return: "))

            if 0 < no_of_return <= no_of_activa_rented:
                cur.execute("UPDATE rentals SET status = 'Returned' WHERE customer_id = %s",(customer_id,))
                conn.commit()
                print("***** Successfully Returned *****")
            else:
                print("Invalid Return Quantity!!")
        else:
            print("No Pending Rentals Found...")
    else:
        print("No Record Found for this Aadhar No.!!!")

    cur.close()
    conn.close()




# Owner Access Function
def owner_access():
    secure_code = input("Enter Owner Secure Code: ")

    if secure_code != "1234":
        print("Invalid Code.....")
        return

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""SELECT customers.c_name, customers.phone_no,customers.address, customers.aadhar_no, customers.driving_license,
    rentals.no_of_activa,rentals.days,rentals.status
    FROM customers
    JOIN rentals ON customers.c_id= rentals.customer_id""")

    for(name, phone,address,aadhar,licence,no_of_activa,days,status) in cur:
        print(f"\nName: {name}\nPhone: {phone}\nAddress: {address}\nAadhar No: {aadhar}\nDriving License: {licence}")
        print(f"No of Activa Booking: {no_of_activa}\nNo of Day Booking: {days}\nStatus: {status}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()