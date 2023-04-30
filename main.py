import re
import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "0000",
    database = "agency"
)

mycursor=mydb.cursor()
# mycursor.execute("select * from login")
# for i in mycursor:
#     print(i)



def emailvalidator(s):
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(pat,s):
        return True
    else:
        return False

print("\nWelcome to Air Pronto\n")
print("1.   Login")
print("2.   Sign In\n")

global user
        
while True:
    choice1=int(input("Enter your Choice: "))
    print("\n")
    if choice1==1:
        print("Please Login Here")
        name=input("\nEnter Your Name: ")
        email=input("Enter Your Email: ")
        emailvalidator(email)
        if emailvalidator(email)==True:
            print("Your Email has been Verified.\n")
            password=input("Enter Your Password: ")
            print("\nYour Password has been Successfully Set.\n")
            sql="INSERT INTO Login (Name,Email,Password,Permission) VALUES (%s, %s, %s, %s)"
            val=(name,email,password,"user")
            mycursor.execute(sql,val)
            mydb.commit()            
            user=1
            break
        break
    
    elif choice1==2:
        print("Please SIGN IN Here")
        Email01=input("Enter Your Email: ")
        Password01=input("Enter Your Password: ")
        print("\n")
        sql="select * from Login where Email=%s and Password=%s"
        val=(Email01,Password01)
        mycursor.execute(sql,val)
        myresult = mycursor.fetchall()
        
        for x in myresult:
            if x[1]==Email01 and x[2]==Password01:
                if x[3]=="admin":
                    #print("Welcome ADMIN to AIR PRONTO")
                    user=0
                    break
                elif x[3]=="user":
                    #print("Welcome USER to AIR PRONTO.")
                    user=1
                else:
                    print("Enter ")
            else:
                print("Your Email is not registered.")
        break
    
    else:
        print("Please Select Validate Option.\n")
        
    
# Will check the name and email from database and varify the user (customer or employee) 


if user==1:
    print("AIR PRONTO WELCOMES YOU...\n")
    while True:
        print("1.   View Flight")
        print("2.   Book Ticket")
        print("3.   Search Flight")
        print("4.   Create Enquiry")
        print("5.   View Enquiry")
        print("6.   Exit")

        choice03=int(input("\nEnter your choice: "))
        if choice03==1:
            print("Flight Schedule: \n")
            mycursor.execute("select Flight_ID,Flight_Name,Airplane_Model,Source,Destination,Date,Takeoff_Time,Landing_Time,Price from airline")
            from_db=[]    
            for i in mycursor:
                i=i
                from_db.append(i)
        
            columns=["Flight Id","  Flight Name","  Airplane Model","   Source","  Destination","  Date","  Takeoff Time","  Landing Time","  Price"]
            df = pd.DataFrame(from_db, columns=columns)
        
            print(df) 
            print("\n")

        elif choice03==2:
            print("Book Flights Ticket: ")
            # noofticket,sourec,destination,date,price,
            # passenger name,age,phoneno(OTP),gender
            #seatno, transiction no
            sou=input("Enter Source: ")
            des=input("Enter Destination: ")
            print("\n")
            sql="select Flight_ID,Flight_Name,Airplane_Model,Source,Destination,Date,Takeoff_Time,Landing_Time,Price from airline where Source=%s and Destination=%s"
            val=(sou,des)
            mycursor.execute(sql,val)
            from_db=[]    
            for i in mycursor:
                i=i
                from_db.append(i)
        
            columns=["Flight Id","  Flight Name","  Airplane Model","   Source","  Destination","  Date","  Takeoff Time","  Landing Time","  Price"]
            df = pd.DataFrame(from_db, columns=columns)
        
            print(df)
            print("\n")
            
            date=input("Enter date (yyyy-mm-dd): ")
            nt=int(input("Enter Ticket Count: "))
            print("\n")
            
            counter=0
            while counter<nt:
                PassName=[]
                Age=[]
                Gender=[]
                phone=[]
                Passname=input(f"Enter Passenger {counter+1} Name: ")
                PassName.append(Passname)
                PAge=input("Enter Age: ")
                Age.append(PAge)
                PGender=input(f"Enter Gender: ")
                Gender.append(PGender)
                mobile=int(input("Enter phone no: "))
                phone.append(mobile)
                counter+=1
                print("\n")
                sql="insert into Booking (Name,Age,Gender,Source,Destination,Date,Phone) values (%s, %s, %s, %s, %s, %s, %s)"
                val=(Passname,PAge,PGender,sou,des,date,mobile)
                mycursor.execute(sql,val)
                mydb.commit() 
            
            sql="select price from airline where Source=%s and Destination=%s"
            val=(sou,des)
            mycursor.execute(sql,val)
            for i in mycursor:
                print("Total Price of Ticket = ",int(i[0])*nt,"\n")
                
                # ii=int(i)*nt 
                # print("Total Price of Ticket = ",ii,"\n")
                
        elif choice03==3:
            print("Here You Can Search for all Flights")
            sou=input("Enter Your Source: ")
            des=input("Enter Your Destination: ")
            print("Searched Flight: \n")
            sql="select Flight_ID,Flight_Name,Airplane_Model,Source,Destination,Date,Takeoff_Time,Landing_Time,Price from airline where Source=%s and Destination=%s"
            val=(sou,des)
            mycursor.execute(sql,val)
            from_db=[]    
            for i in mycursor:
                i=i
                from_db.append(i)
        
            columns=["Flight Id","  Flight Name","  Airplane Model","   Source","  Destination","  Date","  Takeoff Time","  Landing Time","  Price"]
            df = pd.DataFrame(from_db, columns=columns)
        
            print(df) 
            print("\n")

        elif choice03==4:
            print("\nHere You Can type your Enquiry\n")
            Name=input("Enter Your Name: ")
            Enq=input("Enter Your Enquiry: ")
            sql="INSERT INTO Enquiry (Name,Enq,Status) VALUES (%s, %s, %s)"
            val=(Name,Enq,"pending")
            mycursor.execute(sql,val)
            mydb.commit()     
            print("\nYour Enquiry has been Submitted.\n")
            
        elif choice03==5:
            name001=input("Enter Your Name: ")
            sql00="select * from enquiry where Name = %s"
            val00=(name001,)
            mycursor.execute(sql00,val00)
            from_db=[]    
            for i in mycursor:
                i=i
                from_db.append(i)
        
            columns=["Name","   Enquiry","   Status"]
            df = pd.DataFrame(from_db, columns=columns)
        
            print(df) 
            print("\n")

        elif choice03==6:
            print("Thank You for visiting us")
            break 
        
        else:
            print("Select proper option.")


if user==0:
    print("AIR PRONTO WELCOMES YOU...")
    while True:
        print("1.   Manage Airline")
        print("2.   Manage Ticket Booking")
        print("3.   Manage Employee")
        print("4.   Manage Enquiry")
        print("5.   Exit\n")
    
        choice02=int(input("Enter your choice: "))
        
        if choice02==1:
            print("\nAIR PRONTO ~ AIRLINE MANAGEMENT\n")
                      
            def add_flight():
                id=input("Enter Flight ID: ")
                name=input("Enter Flight Name: ")
                air_model=input("Enter Airplane Model: ")
                Sou=input("Enter Source: ")
                Des=input("Enter Destination: ")
                Dte=input("Enter Date: ")
                Takeoff=input("Enter Takeoff Time: ")
                Landing=input("Enter Landing Time: ")
                pc=int(input("Enter Passenger Capacity: "))
                sr=int(input("Enter Staff Required: "))
                price=input("Enter Price: ")
                
                sql="INSERT INTO airline (Flight_Id,Flight_Name,Airplane_Model,Source,Destination,Date,Takeoff_Time,Landing_Time,Passenger_Capacity,Staff_Reqquired,Price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val=(id,name,air_model,Sou,Des,Dte,Takeoff,Landing,pc,sr,price)
                mycursor.execute(sql,val)
                mydb.commit() 
                
                print("\nNew Flight has been added.\n\n")
            
            def delete_flight():
                id=input("Enter Flight ID: ")
                name=input("Enter Flight Name: ")
                air_model=input("Enter Airplane Model: ")
                Sou=input("Enter Source: ")
                Des=input("Enter Destination: ")
                
                sql="delete from airline where Flight_ID=%s and Flight_Name=%s and Airplane_Model=%s and Source=%s and Destination=%s"
                val=(id,name,air_model,Sou,Des)
                mycursor.execute(sql,val)
                mydb.commit()
                
                print("\nFlight has been Deleted\n")
                
            def update_flight():
                print("Please Provide Flight Details :")
                id=input("Enter Flight ID: ")
                name=input("Enter Flight Name: ")
                model=input("Enter Airplane Model: ")
                print("\n")
                print("Please Select what do you want to update: ")
                print("1.   Flight_ID")
                print("2.   Flight_Name")
                print("3.   Airplane_Model")
                print("4.   Source")
                print("5.   Destination")
                print("6.   Date")
                print("7.   Takeoff_Time")
                print("8.   Landing_Time")
                print("9.   Passenger_Capacity")
                print("10.  Staff_Required")
                print("11.  Price\n")    
                
                cho=input("Enter Your Section (Names_only): ")
                print("\n")
                if cho!="Takeoff_Time" or "Landing_Time":
                    change=input("Enter Change: ")
                    print("\n")
                else:
                    change=int(input("Enter Change: "))
                    print("\n")
                        
                sql=f"UPDATE airline SET {cho} = %s where Flight_ID=%s and Flight_Name=%s and Airplane_Model=%s" 
                val=(change,id,name,model)
                mycursor.execute(sql,val)
                mydb.commit()
                print("Flights Updated..\n")
                
                # Program will start from here--
           
            mycursor.execute("select * from airline")
            from_db=[]    
            for i in mycursor:
                i=i
                from_db.append(i)
        
            columns=["Flight Id","  Flight Name","  Airplane Model","   Source","  Destination","  Date","  Takeoff Time","  Landing Time"," Passengers Capacity"," Staff Required","  Price"]
            df = pd.DataFrame(from_db, columns=columns)
        
            print(df)    
            print("\n")        
            print("To Manage Airline Select Appropriate Option: \n")
            
                
            while True:
                print("1.   Add Flight")
                print("2.   Delete Flight")
                print("3.   Update Flight")
                print("4.   Exit\n")   
                opt01=int(input("Enter your choice: "))
                print("\n")
                if opt01==1:
                    add_flight()
                elif opt01==2:
                    delete_flight()
                elif opt01==3:
                    update_flight() 
                elif opt01==4:
                    print("Changes has been Saved...\n")
                    break
                else:    
                    print("Select valid option\n")
    
        
        elif choice02==2:
            print("\nAIR PRONTO ~ TICKET BOOKING")
            
            def add_passenger():
                pname=input("Enter Passenger Name: ")
                age=int(input("Enter Age: "))
                gen=input("Enter Gender: ")
                Sou=input("Enter Source: ")
                Des=input("Enter Destination: ")
                Dte=input("Enter Date: ")
                pho=input("Enter Phone Number: ")
                               
                sql="INSERT INTO Booking (Name,Age,Gender,Source,Destination,Date,Phone) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val=(pname,age,gen,Sou,Des,Dte,pho)
                mycursor.execute(sql,val)
                mydb.commit() 
                
                print("\nNew Passenger has been added.\n\n")
            
            def delete_passenger():
                pname=input("Enter Passenger Name: ")
                age=int(input("Enter Age: "))
                gen=input("Enter Gender: ")
                Sou=input("Enter Source: ")
                Des=input("Enter Destination: ")
                Dte=input("Enter Date: ")
                pho=input("Enter Phone Number: ")
                
                sql="delete from Booking where Name=%s and Age=%s and Gender=%s and Source=%s and Destination=%s and Date=%s and Phone=%s"
                val=(pname,age,gen,Sou,Des,Dte,pho)
                mycursor.execute(sql,val)
                mydb.commit()
                
                print("\nPassenger's Details has been Deleted\n")
                
            def update_passenger():
                pname=input("Enter Passenger Name: ")
                age=int(input("Enter Age: "))
                gen=input("Enter Gender: ")
                Sou=input("Enter Source: ")
                Des=input("Enter Destination: ")
                Dte=input("Enter Date: ")
                pho=input("Enter Phone Number: ")
                print("\n")
                print("Please Select what do you want to update: ")
                print("1.   Passenger_Name")
                print("2.   Age")
                print("3.   Gender")
                print("4.   Source")
                print("5.   Destination")
                print("6.   Date")
                print("7.   Phone\n")    
                
                cho=input("Enter Your Section (Names_only): ")
                print("\n")
                if cho!="Age":
                    change=input("Enter Change: ")
                    print("\n")
                else:
                    change=int(input("Enter Change: "))
                    print("\n")
                        
                sql=f"UPDATE Booking SET {cho} = %s where Name=%s and Age=%s and Gender=%s and Phone=%s" 
                val=(change,pname,age,gen,pho)
                mycursor.execute(sql,val)
                mydb.commit()
                print("Passenger's Details Updated..\n")
                
               # Program will start from here--
               
            mycursor.execute("select * from Booking")
            from_db=[]    
            for i in mycursor:
                i=i
                from_db.append(i)
        
            columns=["Passenger Name","  Age","  Gender","   Source","  Destination","  Date","  Phone"]
            df = pd.DataFrame(from_db, columns=columns)
        
            print(df)    
            print("\n") 
           
            
            print("To Manage Passengers Select Appropriate Option: \n")
            
                
            while True:
                print("1.   Add Passenger Details")
                print("2.   Delete Passenger Details")
                print("3.   Update Passenger Details")
                print("4.   Exit\n")   
                opt01=int(input("Enter your choice: "))
                print("\n")
                if opt01==1:
                    add_passenger()
                elif opt01==2:
                    delete_passenger()
                elif opt01==3:
                    update_passenger() 
                elif opt01==4:
                    print("Changes has been Saved...\n")
                    break
                else:    
                    print("Select valid option\n")
            
       
        elif choice02==3:
            print("AIR PRONTO ~ EMPLOYEE MANAGEMENT\n")
            
            def add_employee():
                id=input("Enter Employee ID: ")
                name=input("Enter Employee Name: ")
                eml=input("Enter Email: ")
                gen=input("Enter Gender: ")
                Desig=input("Enter Designation: ")
                slry=input("Enter Salary: ")
                pms=input("Enter Permission: ")
                
                sql="INSERT INTO Employee (Emp_Id,Emp_Name,Email,Gender,Designation,Salary,Permission) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val=(id,name,eml,gen,Desig,slry,pms)
                mycursor.execute(sql,val)
                mydb.commit() 
                
                print("\nNew Employee has been added.\n\n")
            
            def delete_employee():
                id=input("Enter Employee ID: ")
                name=input("Enter Employee Name: ")
                eml=input("Enter Email: ")
                gen=input("Enter Gender: ")
                Desig=input("Enter Designation: ")
                
                sql="delete from Employee where Emp_ID=%s and Emp_Name=%s and Designation=%s"
                val=(id,name,Desig)
                mycursor.execute(sql,val)
                mydb.commit()
                
                print("\nEmployee's Details has been Deleted\n")
                
            def update_employee():
                id=input("Enter Employee ID: ")
                name=input("Enter Employee Name: ")
                eml=input("Enter Email: ")
                gen=input("Enter Gender: ")
                Desig=input("Enter Designation: ")
                print("\n")
                print("Please Select what do you want to update: ")
                print("1.   Emp_ID")
                print("2.   Emp_Name")
                print("3.   Email")
                print("4.   Gender")
                print("5.   Designation")
                print("6.   Salary")
                print("7.   Permission\n")    
                
                cho=input("Enter Your Section (Names_only): ")
                print("\n")
                
                change=input("Enter Change: ")
                print("\n")
                        
                sql=f"UPDATE Employee SET {cho} = %s where Emp_ID=%s and Emp_Name=%s and Designation=%s" 
                val=(change,id,name,Desig)
                mycursor.execute(sql,val)
                mydb.commit()
                print("Employee's Details Updated..\n")
                
                # Program will start from here--
           
            mycursor.execute("select * from Employee")
            from_db=[]    
            for i in mycursor:
                i=i
                from_db.append(i)
        
            columns=["Employee Id","  Employee Name","  Email","   Gender","  Designation","  Salary","  Permission"]
            df = pd.DataFrame(from_db, columns=columns)
        
            print(df)    
            print("\n")        
            print("To Manage Employee Select Appropriate Option: \n")
            
                
            while True:
                print("1.   Add Employee")
                print("2.   Delete Employee's Details")
                print("3.   Update Employee's Details")
                print("4.   Exit\n")   
                opt01=int(input("Enter your choice: "))
                print("\n")
                if opt01==1:
                    add_employee()
                elif opt01==2:
                    delete_employee()
                elif opt01==3:
                    update_employee() 
                elif opt01==4:
                    print("Changes has been Saved...\n")
                    break
                else:    
                    print("Select valid option\n")
            
        elif choice02==4:
            
            def update_enquiry():
                name=input("Enter Name: ")
                print("\n")
                print("Please Select what do you want to update: ")
                print("1.   Name")
                print("2.   Enquiry")
                print("3.   Status\n")
                
                cho=input("Enter Your Section (Names_only): ")
                print("\n")
                
                change=input("Enter Change: ")
                print("\n")
                        
                sql=f"UPDATE enquiry SET {cho} = %s where name=%s" 
                val=(change,name,)
                mycursor.execute(sql,val)
                mydb.commit()
                print("Enquiry Updated..\n")
                
            def delete_enquiry():
                name=input("Enter Name: ")
                
                sql="delete from enquiry where name=%s"
                val=(name,)
                mycursor.execute(sql,val)
                mydb.commit()
                
                print("\nEnquiry has been Deleted\n")
                
                 # Program will start from here--
                
            print("\nAIR PRONTO ~ Enquiry Section\n")
                
            mycursor.execute("select Name,Enq from enquiry")
            from_db=[]    
            for i in mycursor:
                i=i
                from_db.append(i)
        
            columns=["Name","   Enquiry"]
            df = pd.DataFrame(from_db, columns=columns)
            print(df)    
            print("\n")        
            print("To Manage Enquiry Select Appropriate Option: \n")
            
            while True:
                print("1.   Update Status")
                print("2.   Delete Enquiry")
                print("3.   Exit\n")
                choice=int(input("Enter Your Choice: "))
                if choice==1:
                    update_enquiry()
                elif choice==2:
                    delete_enquiry()
                elif choice==3:
                    print("All Changes have been saved...\n")
                    break
                else:
                    print("Select valid option\n")    
            
        elif choice02==5:
            print("\nThankyou, Visit Again...\n")
            break 
        
        else:
            print("Select Apporpriate Option") 