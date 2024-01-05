import os
import hashlib
import base64
import mysql.connector
from mysql.connector import Error
from database import create_server_connection

# inserting multiple rows in the user table and also assuming the email of each user is unique, comparing the eamil
# if the same eamil address then do not add the row

def hash_password(password):
    # Generate a random salt
    salt = os.urandom(16)
    # Use the sha256 hash algorithm
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # Concatenate the salt and hashed password, and encode it in base64 for storage
    print(f"Length of hashed password: {len(hashed_password)}")
    return base64.b64encode(salt + hashed_password).decode('utf-8')

def check_user_exists(connection, email):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM USER WHERE Email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result is not None
    except Error as err:
        print(f"Error: '{err}'")
        return False

def insert_users(connection, users_data):
    cursor = connection.cursor()
    query = """
    INSERT INTO USER (Email, Fname, Lname, U_Password, U_Role)
    VALUES (%s, %s, %s, %s, %s)
    """
    for user in users_data:
        if not check_user_exists(connection, user['Email']):
            hashed_password = hash_password(user['U_Password'])
            try:
                cursor.execute(query, (user['Email'], user['Fname'], user['Lname'], hashed_password, user['U_Role']))
            except Error as err:
                print(f"Error: '{err}'")
        else:
            print(f"User with email {user['Email']} already exists")

    connection.commit()
    cursor.close()
    print("All users inserted successfully")



def insert_department(connection, department_data):
    cursor = connection.cursor()
    query = """
        INSERT INTO DEPARTMENT (Dno, Dname)
        VALUES (%s, %s)
        """
    for dept in department_data:
        try:
            cursor.execute(query, (dept['Dno'], dept['Dname']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("All departments inserted successfully")

def insert_department_locations(connection, department_locations_data):
    cursor = connection.cursor()
    query = """
            INSERT INTO DEPARTMENT_LOCATIONS (Dno, Dlocation)
            VALUES (%s, %s)
            """
    for dept in department_locations_data:
        try:
            cursor.execute(query, (dept['Dno'], dept['Dlocation']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("All department locations inserted successfully")

def insert_doctors(connection, doctors_data):
    cursor = connection.cursor()
    query = """
            INSERT INTO DOCTOR (D_UserID, Dno, DHours)
            VALUES (%s, %s, %s)
            """
    for doctor in doctors_data:
        try:
            cursor.execute(query, (doctor['D_UserID'], doctor['Dno'], doctor['DHours']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("All doctors inserted successfully")

def insert_nurses(connection, nurses_data):
    cursor = connection.cursor()
    query = """
            INSERT INTO NURSE (N_UserID)
            VALUES (%s)
            """
    for nurse in nurses_data:
        try:
            cursor.execute(query, (nurse['N_UserID']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("All nurses inserted successfully")

def insert_admin(connection, admin_data):
    cursor = connection.cursor()
    query = """
            INSERT INTO ADMIN (A_UserID)
            VALUES (%s)
            """
    for admin in admin_data:
        try:
            cursor.execute(query, (admin['A_UserID']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("All admins inserted successfully")

def insert_patients(connection, patient_data):
    cursor = connection.cursor()
    query = """
            INSERT INTO PATIENT (Patient_No, PName, Email, Emergency_Contact, Date_of_birth)
            VALUES (%s, %s, %s, %s, %s)
            """
    for patient in patient_data:
        try:
            cursor.execute(query, (patient['Patient_No'], patient['PName'], patient['Email'], patient['Emergency_Contact'], patient['Date_of_birth']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("All patients inserted successfully")

def insert_appointment(connection, appointment_data):
    cursor = connection.cursor()
    query = """
            INSERT INTO APPOINTMENT (Apt_No, AptTime, AptDate, D_UserID, Patient_No)
            VALUES (%s, %s, %s, %s, %s)
            """
    for apt in appointment_data:
        try:
            cursor.execute(query, (apt['Apt_No'], apt['AptTime'], apt['AptDate'], apt['D_UserID'], apt['Patient_No']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("All appointments inserted successfully")

def insert_insurance(connection, insurance_data):
    cursor = connection.cursor()
    query = """
            INSERT INTO INSURANCE (Policy_No, Patient_No, StartDate, Dental_Coverage, Drug_Coverage, Health_Coverage)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
    for insurance in insurance_data:
        try:
            cursor.execute(query, (insurance['Policy_No'], insurance['Patient_No'], insurance['StartDate'],
                                   insurance['Dental_Coverage'], insurance['Drug_Coverage'], insurance['Health_Coverage']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("All insurances inserted successfully")

def insert_patient_history(connection, patient_history):
    cursor = connection.cursor()
    query = """
            INSERT INTO PATIENT_HISTORY (File_No, Patient_No)
            VALUES (%s, %s)
            """
    for ph in patient_history:
        try:
            cursor.execute(query, (ph['File_No'], ph['Patient_No']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("All patient history data inserted successfully")

def insert_patient_history_allergies(connection, patient_history_allergies):
    cursor = connection.cursor()
    query = """
            INSERT INTO PATIENT_HISTORY_ALLERGIES (File_No, Patient_No, Allergies)
            VALUES (%s, %s, %s)
            """
    for pha in patient_history_allergies:
        try:
            cursor.execute(query, (pha['File_No'], pha['Patient_No'], pha['Allergies']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("All patient history allergies data inserted successfully")

def insert_patient_history_surgeries(connection, patient_history_surgeries):
    cursor = connection.cursor()
    query = """
            INSERT INTO PATIENT_HISTORY_SURGERIES (File_No, Patient_No, Surgeries)
            VALUES (%s, %s, %s)
            """
    for phs in patient_history_surgeries:
        try:
            cursor.execute(query, (phs['File_No'], phs['Patient_No'], phs['Surgeries']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("All patient history surgeries data inserted successfully")

def insert_patient_history_medications(connection, patient_history_medications):
    cursor = connection.cursor()
    query = """
            INSERT INTO PATIENT_HISTORY_MEDICATIONS (File_No, Patient_No, Medications)
            VALUES (%s, %s, %s)
            """
    for phm in patient_history_medications:
        try:
            cursor.execute(query, (phm['File_No'], phm['Patient_No'], phm['Medications']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("All patient history medications data inserted successfully")

def insert_take_care_of(connection, take_care_of):
    cursor = connection.cursor()
    query = """
            INSERT INTO TAKE_CARE_OF (N_UserID, Patient_No)
            VALUES (%s, %s)
            """
    for tc in take_care_of:
        try:
            cursor.execute(query, (tc['N_UserID'], tc['Patient_No']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("Take care of data inserted successfully")

def insert_works_in(connection, works_in):
    cursor = connection.cursor()
    query = """
                INSERT INTO WORKS_IN (N_UserID, Dno, NHours)
                VALUES (%s, %s, %s)
                """
    for wi in works_in:
        try:
            cursor.execute(query, (wi['N_UserID'], wi['Dno'], wi['NHours']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("Works in data inserted successfully")

def insert_tests(connection, tests_data):
    cursor = connection.cursor()
    query = """
            INSERT INTO TEST (TestName)
            VALUES (%s)
            """
    for test in tests_data:
        try:
            cursor.execute(query, (test['TestName']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("All tests inserted successfully")

def insert_requests(connection, requests):
    cursor = connection.cursor()
    query = """
            INSERT INTO REQUESTS (TestName, D_UserID, Patient_No)
            VALUES (%s, %s, %s)
            """
    for rq in requests:
        try:
            cursor.execute(query, (rq['TestName'], rq['D_UserID'], rq['Patient_No']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("Request table data inserted successfully")

def insert_gets(connection, gets):
    cursor = connection.cursor()
    query = """
            INSERT INTO GETS (TestName, D_userID, Patient_No, Tester, TestDate, Result)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
    for g in gets:
        try:
            cursor.execute(query, (g['TestName'],g['D_UserID'], g['Patient_No'], g['Tester'], g['TestDate'], g['Result']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("Get table data inserted successfully")

def insert_medicine(connection, medicine):
    cursor = connection.cursor()
    query = """
            INSERT INTO MEDICINE (Drug_No, Manufacturer, Med_Expire_Date, Dosage, DailyAmount, TotalDays)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
    for med in medicine:
        try:
            cursor.execute(query, (med['Drug_No'], med['Manufacturer'], med['Med_Expire_Date'],
                                   med['Dosage'], med['DailyAmount'], med['TotalDays']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("All medicines inserted successfully")

def insert_prescribes(connection, prescribes):
    cursor = connection.cursor()
    query = """
            INSERT INTO PRESCRIBES (Drug_No, D_UserID, Patient_No)
            VALUES (%s, %s, %s)
            """
    for p in prescribes:
        try:
            cursor.execute(query, (p['Drug_No'], p['D_UserID'], p['Patient_No']))
        except Error as err:
            print(f"Error: '{err}'")

    connection.commit()
    cursor.close()
    print("Prescribe table data inserted successfully")


def insert_all_data():
    host = "localhost"
    user = "root"
    password = "bio"
    database = 'HOSPITAL'

    # Create a database connection
    connection = create_server_connection(host, user, password, database)

# Example usage
    users_data = [
        {'Email': 'john.doe@example.com', 'Fname': 'John', 'Lname': 'Doe', 'U_Password': 'password123', 'U_Role': 'Doctor'},
        {'Email': 'jane.doe@example.com', 'Fname': 'Jane', 'Lname': 'Doe', 'U_Password': 'password456', 'U_Role': 'Nurse'},
        {'Email': 'josh.doe@example.com', 'Fname': 'Josh', 'Lname': 'Doe', 'U_Password': 'password439', 'U_Role': 'Admin'},
        {'Email': 'john.deb@example.com', 'Fname': 'John', 'Lname': 'Deb', 'U_Password': 'password139','U_Role': 'Doctor'},
        {'Email': 'Alen.deb@example.com', 'Fname': 'Alen', 'Lname': 'Deb', 'U_Password': 'password234','U_Role': 'Nurse'},
        {'Email': 'Jessie.jacobs@example.com', 'Fname': 'Jessie', 'Lname': 'Jacobs', 'U_Password': 'password439','U_Role': 'Nurse'}
    ]

    department_data = [
        {'Dno': 1, 'Dname': 'Cardiology'},
        {'Dno': 2, 'Dname': 'Neurology'},
        {'Dno': 3, 'Dname': 'General Surgery'},
        {'Dno': 4, 'Dname': 'Radiology'},
        {'Dno': 5, 'Dname': 'Orthopedics'}
    ]

    department_locations_data = [
        {'Dno': 1, 'Dlocation': '3rd Floor Foothills'},
        {'Dno': 1, 'Dlocation': '2nd Floor Children'},
        {'Dno': 2, 'Dlocation': '5th Floor Lougheed'},
        {'Dno': 3, 'Dlocation': '2nd Floor Foothills'},
        {'Dno': 4, 'Dlocation': 'Main Floor Children'},
        {'Dno': 4, 'Dlocation': '6th Floor Foothills'},
        {'Dno': 5, 'Dlocation': '1st Floor Lougheed'}
    ]

    doctors_data = [
        {'D_UserID': 1, 'Dno': 2, 'DHours': 25},
        {'D_UserID': 4, 'Dno': 4, 'DHours': 36}
    ]

    nurses_data = [
        {'N_UserID': [2]},
        {'N_UserID': [5]},
        {'N_UserID': [6]}
    ]

    admin_data = [
        {'A_UserID': [3]}
    ]

    patient_data = [
        {'Patient_No': 123, 'PName': 'Bob Henderson', 'Email': 'bob.henderson@example.com', 'Emergency_Contact': 1234567890, 'Date_of_birth': '2002/09/11'},
        {'Patient_No': 236, 'PName': 'Alice Gibbs', 'Email': 'alice.gibbs@example.com', 'Emergency_Contact': 2465895640, 'Date_of_birth': '2000/07/15'},
        {'Patient_No': 789, 'PName': 'Kenzie Loron', 'Email': 'Kenzie.Loron@example.com', 'Emergency_Contact': 2465895640, 'Date_of_birth': '2000/09/15'}
    ]

    appointment_data = [
        {'Apt_No': 7767, 'AptTime': '12:30', 'AptDate': '2023/12/08', 'D_UserID': 1, 'Patient_No': 123},
        {'Apt_No': 7768, 'AptTime': '8:00', 'AptDate': '2023/12/10', 'D_UserID': 4, 'Patient_No': 236}
    ]

    insurance_data = [
        {'Policy_No': 524414, 'Patient_No': 123, 'StartDate': '2022/06/12', 'Dental_Coverage': '80%',
         'Drug_Coverage': '75%', 'Health_Coverage': '90%'},
        {'Policy_No': 521154, 'Patient_No': 236, 'StartDate': '2021/04/18', 'Dental_Coverage': '90%',
         'Drug_Coverage': '80%', 'Health_Coverage': '60%'}
    ]

    patient_history = [
        {'File_No': 742, 'Patient_No': 123},
        {'File_No': 748, 'Patient_No': 236}
    ]

    patient_history_allergies = [
        {'File_No': 742, 'Patient_No': 123, 'Allergies': 'Peanut'},
        {'File_No': 742, 'Patient_No': 123, 'Allergies': 'Gluten'},
        {'File_No': 748, 'Patient_No': 236, 'Allergies': 'Seafood'},
        {'File_No': 748, 'Patient_No': 236, 'Allergies': 'Dairy'}
    ]

    patient_history_surgeries = [
        {'File_No': 742, 'Patient_No': 123, 'Surgeries': 'Heart'},
        {'File_No': 748, 'Patient_No': 236, 'Surgeries': 'Gall Bladder'}
    ]

    patient_history_medications = [
        {'File_No': 742, 'Patient_No': 123, 'Medications': 'Adderall'},
        {'File_No': 742, 'Patient_No': 123, 'Medications': 'Docusate'},
        {'File_No': 748, 'Patient_No': 236, 'Medications': 'Cefalexin'},
        {'File_No': 748, 'Patient_No': 236, 'Medications': 'Enalapril'}
    ]

    take_care_of = [
        {'N_UserID': 2, 'Patient_No': 123},
        {'N_UserID': 5, 'Patient_No': 236}
    ]

    works_in = [
        {'N_UserID': 2, 'Dno': 3, 'NHours': 45},
        {'N_UserID': 5, 'Dno': 5, 'NHours': 38},
        {'N_UserID': 6, 'Dno': 5, 'NHours': 42},
    ]

    tests_data = [
        {'TestName': ['Glucose']},
        {'TestName': ['Vitamin D']},
        {'TestName': ['Lipid panel']},
        {'TestName': ['Thyroid panel']}
    ]

    requests = [
        {'TestName': 'Glucose', 'D_UserID': 1, 'Patient_No': 123},
        {'TestName': 'Glucose', 'D_UserID': 4, 'Patient_No': 236},
        {'TestName': 'Thyroid panel', 'D_UserID': 1, 'Patient_No': 123},
        {'TestName': 'Lipid panel', 'D_UserID': 4, 'Patient_No': 236}
    ]

    gets = [
        {'TestName': 'Glucose', 'D_UserID': 1, 'Patient_No': 123, 'Tester': 'James', 'TestDate': '2023/10/16', 'Result': 'Normal'},
        {'TestName': 'Thyroid panel', 'D_UserID': 4, 'Patient_No': 123, 'Tester': 'John', 'TestDate': '2023/08/24', 'Result': 'Abnormal'},
        {'TestName': 'Glucose', 'D_UserID': 1, 'Patient_No': 236, 'Tester': 'John', 'TestDate': '2023/09/21', 'Result': 'Abnormal'}
    ]

    medicine = [
        {'Drug_No': 98120, 'Manufacturer': 'Equate', 'Med_Expire_Date': '2025/10/10', 'Dosage': '10mg',
         'DailyAmount': 3, 'TotalDays': 7},
        {'Drug_No': 98125, 'Manufacturer': 'McNeil', 'Med_Expire_Date': '2024/03/10', 'Dosage': '30mg',
         'DailyAmount': 2, 'TotalDays': 5},
        {'Drug_No': 97025, 'Manufacturer': 'Medtech', 'Med_Expire_Date': '2024/12/21', 'Dosage': '20mg',
         'DailyAmount': 3, 'TotalDays': 10}
    ]

    prescribes = [
        {'Drug_No': 98120, 'D_UserID': 1, 'Patient_No': 123},
        {'Drug_No': 97025, 'D_UserID': 4, 'Patient_No': 236},
        {'Drug_No': 98125, 'D_UserID': 4, 'Patient_No': 236}
    ]


    insert_users(connection, users_data)
    insert_department(connection, department_data)
    insert_department_locations(connection, department_locations_data)
    insert_doctors(connection, doctors_data)
    insert_nurses(connection, nurses_data)
    insert_admin(connection, admin_data)
    insert_patients(connection, patient_data)
    insert_appointment(connection, appointment_data)
    insert_insurance(connection, insurance_data)
    insert_patient_history(connection, patient_history)
    insert_patient_history_allergies(connection, patient_history_allergies)
    insert_patient_history_surgeries(connection, patient_history_surgeries)
    insert_patient_history_medications(connection, patient_history_medications)
    insert_take_care_of(connection, take_care_of)
    insert_works_in(connection, works_in)
    insert_tests(connection, tests_data)
    insert_requests(connection, requests)
    insert_gets(connection, gets)
    insert_medicine(connection, medicine)
    insert_prescribes(connection, prescribes)

# here all the data insertion for rest of the table will go.


    connection.close()