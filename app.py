import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="hostelm"
)
cursor = conn.cursor()

#-------------------------------------------------------------------------------------------------------------------------

st.title("Hostel Management")

role = st.sidebar.selectbox("Select Role", ["","Admin", "Student"])

#-------------------------------------------------------------------------------------------------------------------------

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'student_logged_in' not in st.session_state:
    st.session_state.student_logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "login"
if 'admin_id' not in st.session_state:
    st.session_state.admin_id = ""
if 'register_number' not in st.session_state:
    st.session_state.register_number = ""

def navigate_to_signup():
    st.session_state.page = "signup"

def navigate_to_menu():
    st.session_state.page = "menu"

def login_user(reg_no, password):
    cursor.execute("SELECT * FROM signup WHERE reg_no = %s AND password = %s", (reg_no, password))
    user = cursor.fetchone()
    if user:
        st.success("Login successful!")
        st.session_state.register_number = reg_no
        navigate_to_menu()
    else:
        st.error("Invalid credentials or user does not exist. Please sign up first.")

def signup_user(email, reg_no, password):
    cursor.execute("SELECT * FROM signup WHERE reg_no = %s", (reg_no,))
    existing_user = cursor.fetchone()
    if existing_user:
        st.error("User already exists! Please try logging in.")
    else:
        query_signup = "INSERT INTO signup (email_id, reg_no, password) VALUES (%s, %s, %s)"
        cursor.execute(query_signup, (email, reg_no, password))
        query_login = "INSERT INTO login (reg_no, password) VALUES (%s, %s)"
        cursor.execute(query_login, (reg_no, password))
        
        conn.commit()
        st.success("Signup successful! Please login.")
        st.session_state.register_number = reg_no

#-------------------------------------------------------------------------------------------------------------------------





if role == "Admin":
    st.write("You have selected: Admin")
    
    login_signup = st.selectbox("Choose", ["Login", "SignUp"])

    if login_signup == "Login":
        if not st.session_state.admin_logged_in:
            st.title("Admin Login")
            admin_id = st.text_input("Admin ID")
            password = st.text_input("Password", type="password")
            login_button = st.button("Login")

            if login_button:
                cursor.execute("SELECT * FROM admin WHERE admin_id = %s AND password = %s", (admin_id, password))
                admin_info = cursor.fetchone()

                if admin_info:
                    st.success("Login successful!")
                    st.session_state.admin_logged_in = True
                    st.session_state.admin_id = admin_id
                else:
                    st.error("Invalid Admin ID or Password")

        if st.session_state.admin_logged_in:
            # Admin Dashboard
            st.title("Admin Dashboard")
            student_search_type = st.selectbox("Search by", ["Register Number", "Name"])
            search_value = st.text_input(f"Enter {student_search_type}")

            if st.button("Search"):
                if student_search_type == "Register Number":
                    query = """
                    SELECT s.reg_no, s.name, s.dept, s.year, s.phone_no, s.hometown, s.gender,
                           g.room_no AS girl_room_no, g.roommates_id AS girl_roommates_id,
                           b.room_no AS boy_room_no, b.block_no AS boy_block_no, b.roommates_id AS boy_roommates_id,
                           m.date AS mess_date, m.token_name, m.price,
                           o.date AS outing_date, o.out_time, o.in_time,
                           c.room_no AS complaint_room_no, c.category, c.complaint,
                           h.out_time AS home_out_time, h.out_date AS home_out_date, h.in_time AS home_in_time, h.in_date AS home_in_date,
                           p.father_name, p.mother_name, p.father_occupation, p.father_no
                    FROM student s
                    LEFT JOIN girls g ON s.reg_no = g.reg_no
                    LEFT JOIN boys b ON s.reg_no = b.reg_no
                    LEFT JOIN mess m ON s.reg_no = m.reg_no
                    LEFT JOIN outing o ON s.reg_no = o.reg_no
                    LEFT JOIN complaints c ON s.reg_no = c.reg_no
                    LEFT JOIN home h ON s.reg_no = h.reg_no
                    LEFT JOIN parent_details p ON s.reg_no = p.reg_no
                    WHERE s.reg_no = %s
                    """
                    cursor.execute(query, (search_value,))
                else:
                    query = """
                    SELECT s.reg_no, s.name, s.dept, s.year, s.phone_no, s.hometown, s.gender,
                           g.room_no AS girl_room_no, g.roommates_id AS girl_roommates_id,
                           b.room_no AS boy_room_no, b.block_no AS boy_block_no, b.roommates_id AS boy_roommates_id,
                           m.date AS mess_date, m.token_name, m.price,
                           o.date AS outing_date, o.out_time, o.in_time,
                           c.room_no AS complaint_room_no, c.category, c.complaint,
                           h.out_time AS home_out_time, h.out_date AS home_out_date, h.in_time AS home_in_time, h.in_date AS home_in_date,
                           p.father_name, p.mother_name, p.father_occupation, p.father_no
                    FROM student s
                    LEFT JOIN girls g ON s.reg_no = g.reg_no
                    LEFT JOIN boys b ON s.reg_no = b.reg_no
                    LEFT JOIN mess m ON s.reg_no = m.reg_no
                    LEFT JOIN outing o ON s.reg_no = o.reg_no
                    LEFT JOIN complaints c ON s.reg_no = c.reg_no
                    LEFT JOIN home h ON s.reg_no = h.reg_no
                    LEFT JOIN parent_details p ON s.reg_no = p.reg_no
                    WHERE s.name = %s
                    """
                    cursor.execute(query, (search_value,))

                results = cursor.fetchall()

                if results:
                    st.write("Student Details:")
                    for row in results:
                        st.write(f"Register Number: {row[0]}")
                        st.write(f"Name: {row[1]}")
                        st.write(f"Department: {row[2]}")
                        st.write(f"Year: {row[3]}")
                        st.write(f"Phone Number: {row[4]}")
                        st.write(f"Hometown: {row[5]}")
                        st.write(f"Gender: {row[6]}")
                        if row[6] == "Female":
                            st.write(f"Room Number: {row[7]}")
                            st.write(f"Roommates ID: {row[8]}")
                        elif row[6] == "Male":
                            st.write(f"Room Number: {row[9]}")
                            st.write(f"Block Number: {row[10]}")
                            st.write(f"Roommates ID: {row[11]}")
                        st.write(f"Mess Date: {row[12]}")
                        st.write(f"Token Name: {row[13]}")
                        st.write(f"Price: {row[14]}")
                        st.write(f"Outing Date: {row[15]}")
                        st.write(f"Out Time: {row[16]}")
                        st.write(f"In Time: {row[17]}")
                        st.write(f"Complaint Room Number: {row[18]}")
                        st.write(f"Category: {row[19]}")
                        st.write(f"Complaint: {row[20]}")
                        st.write(f"Home Out Time: {row[21]}")
                        st.write(f"Home Out Date: {row[22]}")
                        st.write(f"Home In Time: {row[23]}")
                        st.write(f"Home In Date: {row[24]}")
                        st.write(f"Father's Name: {row[25]}")
                        st.write(f"Mother's Name: {row[26]}")
                        st.write(f"Father's Occupation: {row[27]}")
                        st.write(f"Father's Phone Number: {row[28]}")
                        st.write("-----")
                else:
                    st.write("No records found")

    elif login_signup == "SignUp":
        st.title("Admin SignUp")
        admin_id = st.text_input("Admin ID")
        email_id = st.text_input("Email ID")
        password = st.text_input("Password", type="password")
        signup_button = st.button("SignUp")

        if signup_button:
            cursor.execute("SELECT * FROM admin WHERE admin_id = %s", (admin_id,))
            admin_info = cursor.fetchone()

            if admin_info:
                st.error("Admin ID already exists. Please choose a different ID.")
            else:
                query_insert = "INSERT INTO admin (admin_id, email_id, password) VALUES (%s, %s, %s)"
                cursor.execute(query_insert, (admin_id, email_id, password))
                conn.commit()
                st.success("Admin registered successfully! Please login now.")

    


#-------------------------------------------------------------------------------------------------------------------------
    
elif role == "Student":
    if st.session_state.page == "login":
        st.write("You have selected: Student")
        
        # Display login form for students
        st.subheader("Student Login")
        register_number = st.text_input("Register Number", value=st.session_state.register_number)
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")

        if login_button:
            login_user(register_number, password)

        # Use Streamlit components for a clickable link
        if st.button("Don't have an account? Sign up"):
            navigate_to_signup()

    elif st.session_state.page == "signup":
        st.subheader("Student Signup")
        email = st.text_input("Email ID")
        register_number = st.text_input("Register Number")
        password = st.text_input("Password", type="password")
        signup_button = st.button("Sign up")

        if signup_button:
            signup_user(email, register_number, password)

#-------------------------------------------------------------------------------------------------------------------------

if st.session_state.page == "menu":
    st.subheader(f"Hi **{st.session_state.register_number}**!")
    
    selected = option_menu(
        menu_title="Student info",
        options=["Student", "Mess Token", "Boys", "Girls", "Outing", "Complaints", "Home In & Out Time", "Parent Details"],
        default_index=0,
        orientation="horizontal",
    )
    

#-------------------------------------------------------------------------------------------------------------------------

    if selected == "Student":
        opt = st.selectbox("Select ", ["Enter details", "View"])
        
        def enter_or_update_details(reg_no):
            cursor.execute("SELECT * FROM student WHERE reg_no = %s", (reg_no,))
            student_info = cursor.fetchone()
            if student_info:
                st.subheader("Update Student Details")
                name = st.text_input("Name", value=student_info[1])
                dept = st.text_input("Department", value=student_info[2])
                year = st.number_input("Year", value=student_info[3])
                phone_no = st.text_input("Phone Number", value=student_info[4])
                hometown = st.text_input("Hometown", value=student_info[5])
                gender = st.selectbox("Gender", ["Male", "Female"], index=0 if student_info[6] == "Male" else 1)
                update_button = st.button("Update Details")
                if update_button:
                    query_update = "UPDATE student SET name = %s, dept = %s, year = %s, phone_no = %s, hometown = %s, gender = %s WHERE reg_no = %s"
                    cursor.execute(query_update, (name, dept, year, phone_no, hometown, gender, reg_no))
                    conn.commit()
                    st.success("Student details updated successfully!")
            else:
                st.subheader("Enter Student Details")
                name = st.text_input("Name")
                dept = st.text_input("Department")
                year = st.number_input("Year")
                phone_no = st.text_input("Phone Number")
                hometown = st.text_input("Hometown")
                gender = st.selectbox("Gender", ["Male", "Female"], index=0)
                enter_button = st.button("Enter Details")
                if enter_button:
                    query_insert = "INSERT INTO student (reg_no, name, dept, year, phone_no, hometown, gender) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(query_insert, (reg_no, name, dept, year, phone_no, hometown, gender))
                    conn.commit()
                    st.success("Student details entered successfully!")

        def view_student_details(reg_no):
            cursor.execute("SELECT * FROM student WHERE reg_no = %s", (reg_no,))
            student_info = cursor.fetchone()
            if student_info:
                st.subheader("Student Details")
                st.write(f"Name: {student_info[1]}")
                st.write(f"Department: {student_info[2]}")
                st.write(f"Year: {student_info[3]}")
                st.write(f"Phone Number: {student_info[4]}")
                st.write(f"Hometown: {student_info[5]}")
                st.write(f"Gender: {student_info[6]}")
            else:
                st.info("No details entered.")
        
        if opt == "Enter details":
            enter_or_update_details(st.session_state.register_number)
        elif opt == "View":
            view_student_details(st.session_state.register_number)
    
                
#-------------------------------------------------------------------------------------------------------------------------
    if selected == "Mess Token":
        o1 = st.selectbox("Select ", ["Enter2", "View2"])


        def enter_mess_details(reg_no):
            cursor.execute("SELECT name FROM student WHERE reg_no = %s", (reg_no,))
            result = cursor.fetchone()
            if result:
                name = result[0]
                st.subheader("Enter Mess Details")
                date = st.date_input("Date")
                token_name = st.text_input("Token Name")
                price = st.number_input("Price", min_value=0.0, format="%.2f")
                submit_button = st.button("Submit")

                if submit_button:
                    query = "INSERT INTO mess (reg_no, name, date, token_name, price) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(query, (reg_no, name, date, token_name, price))
                    conn.commit()
                    st.success("Details submitted successfully!")
            else:
                st.error("Student details not found. Please ensure your profile is complete.")


        def view_mess_details(reg_no):
            cursor.execute("SELECT reg_no, name, date, token_name, price FROM mess WHERE reg_no = %s", (reg_no,))
            records = cursor.fetchall()
            if records:
                st.subheader("Mess Token Details")
                for record in records:
                    st.write(f"Date: {record[2]}, Token Name: {record[3]}, Price: {record[4]:.2f}")
            else:
                st.info("No records found.")
                
        def generate_bill(reg_no):
            cursor.execute("SELECT name, date, token_name, price FROM mess WHERE reg_no = %s", (reg_no,))
            records = cursor.fetchall()

            cursor.execute("SELECT SUM(price) FROM mess WHERE reg_no = %s", (reg_no,))
            total_price = cursor.fetchone()[0]

            if records:
                st.subheader("PSG iTech")
                st.write("### Mess Token Bill")
                bill_details = []
                for record in records:
                    date, token_name, price = record[1], record[2], record[3]
                    bill_details.append(f"Date: {date}, Token Name: {token_name}, Price: {price:.2f}")
                    st.write("\n".join(bill_details))
                    st.write(f"**Total Price: {total_price:.2f}**")
            else:
                st.info("No records found to generate the bill.")
                
        
        if o1 == "Enter2":
            enter_mess_details(st.session_state.register_number)
        elif o1 == "View2":
            view_mess_details(st.session_state.register_number)
            
        generate_bill_button = st.button("Generate Bill")
        if generate_bill_button:
            generate_bill(st.session_state.register_number)
#-------------------------------------------------------------------------------------------------------------------------
    if selected == "Outing":
        o3 = st.selectbox("Select ", ["Enter3", "View3"])
        
    
        def enter_outing_details(reg_no):
            cursor.execute("SELECT name FROM student WHERE reg_no = %s", (reg_no,))
            result = cursor.fetchone()
            if result:
                name = result[0]
                st.subheader("Enter Outing Details")
                date = st.date_input("Date")
                out_time = st.time_input("Out Time")
                in_time = st.time_input("In Time")
                submit_button = st.button("Submit")

                if submit_button:
                    query = "INSERT INTO outing (reg_no, name, date, out_time, in_time) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(query, (reg_no, name, date, out_time, in_time))
                    conn.commit()
                    st.success("Details submitted successfully!")
            else:
                st.error("Student details not found. Please ensure your profile is complete.")
            
        def view_outing_details(reg_no):
            cursor.execute("SELECT reg_no, name, date, out_time, in_time FROM outing WHERE reg_no = %s", (reg_no,))
            records = cursor.fetchall()
            if records:
                st.subheader("Outing Details")
                for record in records:
                    st.write(f"Date: {record[2]}, Out Time: {record[3]}, In Time: {record[4]}")
            else:
                st.info("No records found.")
          
        if o3 == "Enter3":
            enter_outing_details(st.session_state.register_number)
        elif o3 == "View3":
            view_outing_details(st.session_state.register_number)


#-------------------------------------------------------------------------------------------------------------------------
    if selected == "Home In & Out Time":
        o4 = st.selectbox("Select ", ["Enter4", "View4"])
        
        def enter_home_details(reg_no):
            cursor.execute("SELECT name FROM student WHERE reg_no = %s", (reg_no,))
            result = cursor.fetchone()
            if result:
                name = result[0]
                st.subheader("Enter Home In & Out Time Details")
                out_date = st.date_input("Out Date")
                out_time = st.time_input("Out Time")
                in_date = st.date_input("In Date")
                in_time = st.time_input("In Time")
                submit_button = st.button("Submit")

                if submit_button:
                    query = "INSERT INTO home (reg_no, name, out_date, out_time, in_date, in_time) VALUES (%s, %s, %s, %s, %s, %s)"
                    cursor.execute(query, (reg_no, name, out_date, out_time, in_date, in_time))
                    conn.commit()
                    st.success("Details submitted successfully!")
            else:
                st.error("Student details not found. Please ensure your profile is complete.")
            
            
        def view_home_details(reg_no):
            cursor.execute("SELECT reg_no, name, out_date, out_time, in_date, in_time FROM home WHERE reg_no = %s", (reg_no,))
            records = cursor.fetchall()
            if records:
                st.subheader("Home In & Out Time Details")
                for record in records:
                    st.write(f"Out Date: {record[2]}, Out Time: {record[3]}, In Date: {record[4]}, In Time: {record[5]}")
            else:
                st.info("No records found.")
            
        if o4 == "Enter4":
            enter_home_details(st.session_state.register_number)
        elif o4 == "View4":
            view_home_details(st.session_state.register_number)
        
        
#-------------------------------------------------------------------------------------------------------------------------

    if selected == "Parent Details":
        o5 = st.selectbox("Select ", ["Enter5", "View5"])

        def enter_parent_details(reg_no):
            cursor.execute("SELECT * FROM parent_details WHERE reg_no = %s", (reg_no,))
            parent_info = cursor.fetchone()
            if parent_info:
                st.subheader("Update Parent Details")
                name = st.text_input("Name", value=parent_info[1])
                father_name = st.text_input("Father's Name", value=parent_info[2])
                mother_name = st.text_input("Mother's Name", value=parent_info[3])
                father_occupation = st.text_input("Father's Occupation", value=parent_info[4])
                father_no = st.text_input("Father's Phone", value=parent_info[5])
                mother_no = st.text_input("Mother's Phone", value=parent_info[6])

                update_button = st.button("Update Details")
                if update_button:
                    query_update = """UPDATE parent_details 
                                      SET name = %s, father_name = %s, mother_name = %s, 
                                          father_occupation = %s, father_no = %s, mother_no = %s 
                                      WHERE reg_no = %s"""
                    cursor.execute(query_update, (name, father_name, mother_name, father_occupation, father_no, mother_no, reg_no))
                    conn.commit()
                    st.success("Parent details updated successfully!")
            else:
                st.subheader("Enter Parent Details")
                name = st.text_input("Name")
                father_name = st.text_input("Father's Name")
                mother_name = st.text_input("Mother's Name")
                father_occupation = st.text_input("Father's Occupation")
                father_no = st.text_input("Father's Phone")
                mother_no = st.text_input("Mother's Phone")

                enter_button = st.button("Enter Details")
                if enter_button:
                    query_insert = """INSERT INTO parent_details 
                                    (reg_no, name, father_name, mother_name, father_occupation, father_no, mother_no) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(query_insert, (reg_no, name, father_name, mother_name, father_occupation, father_no, mother_no))
                    conn.commit()
                    st.success("Parent details entered successfully!")

        def view_parent_details(reg_no):
            cursor.execute("SELECT * FROM parent_details WHERE reg_no = %s", (reg_no,))
            parent_info = cursor.fetchone()
            if parent_info:
                st.subheader("Parent Details")
                st.write(f"Name: {parent_info[1]}")
                st.write(f"Father's Name: {parent_info[2]}")
                st.write(f"Mother's Name: {parent_info[3]}")
                st.write(f"Father's Occupation: {parent_info[4]}")
                st.write(f"Father's Phone: {parent_info[5]}")
                st.write(f"Mother's Phone: {parent_info[6]}")
            else:
                st.info("No details entered or record not found.")

        if o5 == "Enter5":
            enter_parent_details(st.session_state.register_number)
        elif o5 == "View5":
            view_parent_details(st.session_state.register_number)



#-------------------------------------------------------------------------------------------------------------------------

    if selected == "Boys":
        o6 = st.selectbox("Select ", ["Enter6", "View6"])
        
        def check_gender(reg_no):
            cursor.execute("SELECT gender FROM student WHERE reg_no = %s", (reg_no,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None

        def enter_boys_details(reg_no):
            gender = check_gender(reg_no)
            if gender != "Male":
                st.error("You are not authorized to enter or view these records.")
                return

            cursor.execute("SELECT * FROM boys WHERE reg_no = %s", (reg_no,))
            boys_info = cursor.fetchone()
            if boys_info:
                st.subheader("Update Boys Details")
                name = st.text_input("Name", value=boys_info[1])
                room_no = st.text_input("Room Number", value=boys_info[2])
                block_no = st.text_input("Block Number", value=boys_info[3])
                roommates_id = st.text_input("Roommates ID", value=boys_info[4])

                update_button = st.button("Update Details")
                if update_button:
                    query_update = """UPDATE boys 
                                    SET name = %s, room_no = %s, block_no = %s, roommates_id = %s 
                                    WHERE reg_no = %s"""
                    cursor.execute(query_update, (name, room_no, block_no, roommates_id, reg_no))
                    conn.commit()
                    st.success("Boys details updated successfully!")
            else:
                st.subheader("Enter Boys Details")
                name = st.text_input("Name")
                room_no = st.text_input("Room Number")
                block_no = st.text_input("Block Number")
                roommates_id = st.text_input("Roommates ID")

                enter_button = st.button("Enter Details")
                if enter_button:
                    query_insert = """INSERT INTO boys 
                                    (reg_no, name, room_no, block_no, roommates_id) 
                                    VALUES (%s, %s, %s, %s, %s)"""
                    cursor.execute(query_insert, (reg_no, name, room_no, block_no, roommates_id))
                    conn.commit()
                    st.success("Boys details entered successfully!")

        def view_boys_details(reg_no):
            gender = check_gender(reg_no)
            if gender != "Male":
                st.error("You are not authorized to enter or view boys' records.")
                return

            cursor.execute("SELECT * FROM boys WHERE reg_no = %s", (reg_no,))
            boys_info = cursor.fetchone()
            if boys_info:
                st.subheader("Boys Details")
                st.write(f"Name: {boys_info[1]}")
                st.write(f"Room Number: {boys_info[2]}")
                st.write(f"Block Number: {boys_info[3]}")
                st.write(f"Roommates ID: {boys_info[4]}")
            else:
                st.info("No details entered or record not found.")
        
                
        if o6 == "Enter6":
            enter_boys_details(st.session_state.register_number)
        elif o6 == "View6":
            view_boys_details(st.session_state.register_number)

#-------------------------------------------------------------------------------------------------------------------------

    if selected == "Girls":
        o7 = st.selectbox("Select ", ["Enter7", "View7"])
        
        def check_gender(reg_no):
            cursor.execute("SELECT gender FROM student WHERE reg_no = %s", (reg_no,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None

        def enter_girls_details(reg_no):
            gender = check_gender(reg_no)
            if gender != "Female":
                st.error("You are not authorized to enter or view these records.")
                return

            cursor.execute("SELECT * FROM girls WHERE reg_no = %s", (reg_no,))
            girls_info = cursor.fetchone()
            if girls_info:
                st.subheader("Update Girls Details")
                name = st.text_input("Name", value=girls_info[1])
                room_no = st.text_input("Room Number", value=girls_info[2])
                roommates_id = st.text_input("Roommates ID", value=girls_info[3])

                update_button = st.button("Update Details")
                if update_button:
                    query_update = """UPDATE girls 
                                    SET name = %s, room_no = %s, roommates_id = %s 
                                    WHERE reg_no = %s"""
                    cursor.execute(query_update, (name, room_no, roommates_id, reg_no))
                    conn.commit()
                    st.success("Girls details updated successfully!")
            else:
                st.subheader("Enter Girls Details")
                name = st.text_input("Name")
                room_no = st.text_input("Room Number")
                roommates_id = st.text_input("Roommates ID")

                enter_button = st.button("Enter Details")
                if enter_button:
                    query_insert = """INSERT INTO girls 
                                    (reg_no, name, room_no, roommates_id) 
                                    VALUES (%s, %s, %s, %s)"""
                    cursor.execute(query_insert, (reg_no, name, room_no, roommates_id))
                    conn.commit()
                    st.success("Girls details entered successfully!")

        def view_girls_details(reg_no):
            gender = check_gender(reg_no)
            if gender != "Female":
                st.error("You are not authorized to enter or view girls' records.")
                return

            cursor.execute("SELECT * FROM girls WHERE reg_no = %s", (reg_no,))
            girls_info = cursor.fetchone()
            if girls_info:
                st.subheader("Girls Details")
                st.write(f"Name: {girls_info[1]}")
                st.write(f"Room Number: {girls_info[2]}")
                st.write(f"Roommates ID: {girls_info[3]}")
            else:
                st.info("No details entered or record not found.")


        if o7 == "Enter7":
            enter_girls_details(st.session_state.register_number)
        elif o7 == "View7":
            view_girls_details(st.session_state.register_number)

#-------------------------------------------------------------------------------------------------------------------------

    if selected == "Complaints":
        o8 = st.selectbox("Select ", ["Enter8", "View8"])        
        
        def enter_complaint_details(reg_no):
            cursor.execute("SELECT name FROM student WHERE reg_no = %s", (reg_no,))
            student_info = cursor.fetchone()
            if student_info:
                name = student_info[0]
                #room_no = st.text_input("Room Number")
                category = st.selectbox("Category", ["Food", "Civil", "Housekeeping", "Electric", "Other"])
                complaint = st.text_area("Complaint")

                enter_button = st.button("Enter Details")
                if enter_button:
                    query_insert = """INSERT INTO complaints (reg_no, name, category, complaint) 
                                    VALUES ( %s, %s, %s, %s)"""
                    cursor.execute(query_insert, (reg_no, name, category, complaint))
                    conn.commit()
                    st.success("Complaint details entered successfully!")
            else:
                st.error("Student not found. Please check your registration number.")

        def view_complaint_details(reg_no):
            cursor.execute("SELECT * FROM complaints WHERE reg_no = %s", (reg_no,))
            complaint_info = cursor.fetchall()
            if complaint_info:
                st.subheader("Complaints Details")
                st.write(f"Reg No: {complaint_info[0][0]}")
                st.write(f"Name: {complaint_info[0][1]}")
                for complaint in complaint_info:
                    #st.write(f"Room Number: {complaint[2]}")
                    st.write(f"Category: {complaint[3]}")
                    st.write(f"Complaint: {complaint[4]}")
                    st.write("---")
            else:
                st.info("No complaints found for your registration number.")
                
        if o8 == "Enter8":
            enter_complaint_details(st.session_state.register_number)
        elif o8 == "View8":
            view_complaint_details(st.session_state.register_number)


#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
        
        
cursor.close()
conn.close()
