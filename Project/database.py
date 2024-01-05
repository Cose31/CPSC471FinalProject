import os
import mysql.connector
from mysql.connector import Error


def create_server_connection(host_name, user_name, user_password, database_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")  # Create the database if it doesn't exist
        connection.commit()  # Commit the transaction
        connection.close()

        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=database_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

def create_user_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS USER (
            UserID INT AUTO_INCREMENT PRIMARY KEY,
            Email VARCHAR(255) NOT NULL UNIQUE,
            Fname VARCHAR(20) NOT NULL,
            Lname VARCHAR(20) NOT NULL,
            U_Password VARCHAR(255) NOT NULL,
            U_Role VARCHAR(20) NOT NULL
        );
        """
        cursor.execute(create_table_query)
        connection.commit()  # Commit the transaction
        print("User table created successfully")
    except Error as err:
        print(f"Error: '{err}'")


def create_doctor_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS DOCTOR (
            D_UserID INT NOT NULL,
            Dno INT NOT NULL,
            DHours INT NOT NULL,
            PRIMARY KEY (D_UserID),
            FOREIGN KEY (D_UserID) REFERENCES USER (UserID)
                ON UPDATE CASCADE
        );
        """
        cursor.execute(create_table_query)
        connection.commit()  # Commit the transaction
        print("Doctor table created successfully")
    except Error as err:
        print(f"Error: '{err}'")


def create_doctor_specialist_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS DOCTOR_SPECIALIST (
            D_UserID INT NOT NULL,
            Specialist VARCHAR(20) NOT NULL,
            PRIMARY KEY (D_UserID),
            FOREIGN KEY (D_UserID) REFERENCES DOCTOR (D_UserID)
                ON UPDATE CASCADE
        );
        """
        cursor.execute(create_table_query)
        connection.commit()  # Commit the transaction
        print("Doctor Specialist table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_nurse_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS NURSE (
            N_UserID INT NOT NULL,
            PRIMARY KEY (N_UserID),
            FOREIGN KEY (N_UserID) REFERENCES USER (UserID)
                ON UPDATE CASCADE
        );
        """
        cursor.execute(create_table_query)
        connection.commit()  # Commit the transaction
        print("Nurse table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_admin_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS ADMIN (
            A_UserID INT NOT NULL,
            PRIMARY KEY (A_UserID),
            FOREIGN KEY (A_UserID) REFERENCES USER (UserID)
                ON UPDATE CASCADE
        );
        """
        cursor.execute(create_table_query)
        connection.commit()  # Commit the transaction
        print("Admin table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_department_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS DEPARTMENT (
            Dno INT NOT NULL,
            Dname VARCHAR(20) NOT NULL,
            PRIMARY KEY (Dno)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()  # Commit the transaction
        print("Department table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_department_locations_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS DEPARTMENT_LOCATIONS (
            Dno INT NOT NULL,
            DLocation VARCHAR(50) NOT NULL,
            PRIMARY KEY (Dno, Dlocation),
            FOREIGN KEY (Dno) REFERENCES DEPARTMENT (Dno)
                ON UPDATE CASCADE
        );
        """
        cursor.execute(create_table_query)
        connection.commit()  # Commit the transaction
        print("Department Locations table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_patient_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS PATIENT (
            Patient_No INT NOT NULL,
            PName VARCHAR(20) NOT NULL,
            Email VARCHAR(255) NOT NULL,
            Emergency_Contact VARCHAR(10) NOT NULL,
            Date_of_birth DATE NOT NULL,
            PRIMARY KEY (Patient_No)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()  # Commit the transaction
        print("Patient table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_appointment_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS APPOINTMENT (
            Apt_No INT NOT NULL,
            AptTime TIME NOT NULL,
            AptDate DATE NOT NULL,
            D_UserID INT NOT NULL,
            Patient_No INT NOT NULL,
            PRIMARY KEY (Apt_No),
            FOREIGN KEY (D_UserID) REFERENCES DOCTOR (D_UserID)
                ON UPDATE CASCADE,
            FOREIGN KEY (Patient_No) REFERENCES PATIENT (Patient_No)
                ON UPDATE CASCADE
        );
        """
        cursor.execute(create_table_query)
        connection.commit()  # Commit the transaction
        print("Appointment table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_insurance_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS INSURANCE (
            Policy_No INT NOT NULL,
            Patient_No INT NOT NULL,
            StartDate DATE NOT NULL,
            Dental_Coverage VARCHAR(20) NOT NULL,
            Drug_Coverage VARCHAR(20) NOT NULL,
            Health_Coverage VARCHAR(20) NOT NULL,
            PRIMARY KEY (Policy_No, Patient_No),
            FOREIGN KEY (Patient_No) REFERENCES PATIENT (Patient_No)
                ON UPDATE CASCADE
        );
        """
        cursor.execute(create_table_query)
        connection.commit()  # Commit the transaction
        print("Insurance table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_patient_history_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS PATIENT_HISTORY (
            File_No INT NOT NULL,
            Patient_No INT NOT NULL,
            PRIMARY KEY (File_No, Patient_No),
            FOREIGN KEY (Patient_No) REFERENCES PATIENT (Patient_No)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()  # Commit the transaction
        print("Patient History table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_patient_history_allergies_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS PATIENT_HISTORY_ALLERGIES (
            Patient_No INT NOT NULL,
            File_No INT NOT NULL,
            Allergies VARCHAR(100) NOT NULL,
            PRIMARY KEY (Patient_No, File_No, Allergies),
            FOREIGN KEY (Patient_No) REFERENCES PATIENT_HISTORY (Patient_No)
                ON UPDATE CASCADE,
            FOREIGN KEY (File_No) REFERENCES PATIENT_HISTORY (File_No)
                ON UPDATE CASCADE
        );
        """
        cursor.execute(create_table_query)
        connection.commit()  # Commit the transaction
        print("Patient History Allergies table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_patient_history_surgeries_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS PATIENT_HISTORY_SURGERIES (
            Patient_No INT NOT NULL,
            File_No INT NOT NULL,
            Surgeries VARCHAR(100) NOT NULL,
            PRIMARY KEY (Patient_No, File_No, Surgeries),
            FOREIGN KEY (Patient_No) REFERENCES PATIENT_HISTORY (Patient_No)
                ON UPDATE CASCADE,
            FOREIGN KEY (File_No) REFERENCES PATIENT_HISTORY (File_No)
                ON UPDATE CASCADE
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Patient History Surgeries table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_patient_history_medications_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS PATIENT_HISTORY_MEDICATIONS (
            Patient_No INT NOT NULL,
            File_No INT NOT NULL,
            Medications VARCHAR(100) NOT NULL,
            PRIMARY KEY (Patient_No, File_No, Medications),
            FOREIGN KEY (Patient_No) REFERENCES PATIENT_HISTORY (Patient_No)
                ON UPDATE CASCADE,
            FOREIGN KEY (File_No) REFERENCES PATIENT_HISTORY (File_No)
                ON UPDATE CASCADE
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Patient History Medications table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_take_care_of_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS TAKE_CARE_OF (
            N_UserID INT NOT NULL,
            Patient_No INT NOT NULL,
            PRIMARY KEY (N_UserID, Patient_No),
            FOREIGN KEY (N_UserID) REFERENCES NURSE (N_UserID)
                ON UPDATE CASCADE,
            FOREIGN KEY (Patient_No) REFERENCES PATIENT (Patient_No)
                ON UPDATE CASCADE
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Take Care Of table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_works_in_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS WORKS_IN (
            N_UserID INT NOT NULL,
            Dno INT NOT NULL,
            NHours INT NOT NULL,
            PRIMARY KEY (N_UserID, Dno),
            FOREIGN KEY (N_UserID) REFERENCES NURSE (N_UserID)
                ON UPDATE CASCADE,
            FOREIGN KEY (Dno) REFERENCES DEPARTMENT (Dno)
                ON UPDATE CASCADE
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("WORKS_IN table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_test_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS TEST (
            TestName VARCHAR(20) NOT NULL,
            PRIMARY KEY (TestName)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("TEST table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_requests_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS REQUESTS (
            TestName VARCHAR(20) NOT NULL,
            D_UserID INT NOT NULL,
            Patient_No INT NOT NULL,
            PRIMARY KEY (TestName, D_UserID, Patient_No),
            FOREIGN KEY (TestName) REFERENCES TEST (TestName)
                ON UPDATE CASCADE,
            FOREIGN KEY (D_UserID) REFERENCES DOCTOR (D_UserID)
                ON UPDATE CASCADE,
            FOREIGN KEY (Patient_No) REFERENCES PATIENT (Patient_No)
                ON UPDATE CASCADE
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("REQUESTS table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_gets_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS GETS (
            TestName VARCHAR(20) NOT NULL,
            D_UserID INT NOT NULL,
            Patient_No INT NOT NULL,
            Tester VARCHAR(20) NOT NULL,
            TestDate DATE NOT NULL,
            Result VARCHAR(20) NOT NULL,
            PRIMARY KEY (TestName, Patient_No, D_UserID),
            FOREIGN KEY (TestName) REFERENCES TEST (TestName)
                ON UPDATE CASCADE,
            FOREIGN KEY (Patient_No) REFERENCES PATIENT (Patient_No)
                ON UPDATE CASCADE,
            FOREIGN KEY (D_UserID) REFERENCES DOCTOR (D_UserID)
                ON UPDATE CASCADE
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("GETS table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_medicine_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS MEDICINE (
            Drug_No INT NOT NULL,
            Manufacturer VARCHAR(20) NOT NULL,
            Med_Expire_Date DATE NOT NULL,
            Dosage VARCHAR(20) NOT NULL,
            DailyAmount INT NOT NULL,
            TotalDays INT NOT NULL,
            PRIMARY KEY (Drug_No)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("MEDICINE table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_prescribes_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS PRESCRIBES (
            Drug_No INT NOT NULL,
            D_UserID INT NOT NULL,
            Patient_No INT NOT NULL,
            PRIMARY KEY (Drug_No, D_UserID, Patient_No),
            FOREIGN KEY (Drug_No) REFERENCES MEDICINE (Drug_No)
                ON UPDATE CASCADE,
            FOREIGN KEY (D_UserID) REFERENCES DOCTOR (D_UserID)
                ON UPDATE CASCADE,
            FOREIGN KEY (Patient_No) REFERENCES PATIENT (Patient_No)
                ON UPDATE CASCADE
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("PRESCRIBES table created successfully")
    except Error as err:
        print(f"Error: '{err}'")


def setup_database():
    host = "localhost"
    user = "root"
    password = "bio"
    database = 'HOSPITAL'

    connection = create_server_connection(host, user, password, database)

    create_user_table(connection) # Call the create_user_table function to create the User table
    create_doctor_table(connection)# Call the create_doctor_table function to create the DOCTOR table
    create_doctor_specialist_table(connection) # Call the create_doctor_specialist_table function to create the DOCTOR_SPECIALIST table
    create_nurse_table(connection)  # Call the function to create the NURSE table
    create_admin_table(connection)  # Call the function to create the ADMIN table
    create_department_table(connection)  # Call the function to create the DEPARTMENT table
    create_department_locations_table(connection)  # Call the function to create the DEPARTMENT_LOCATIONS table
    create_patient_table(connection)  # Call the function to create the PATIENT table
    create_appointment_table(connection)  # Call the function to create the APPOINTMENT table
    create_insurance_table(connection)  # Call the function to create the INSURANCE table
    create_patient_history_table(connection)  # Call the function to create the PATIENT_HISTORY table
    create_patient_history_allergies_table(connection)  # Call the function to create the PATIENT_HISTORY_ALLERGIES table
    create_patient_history_surgeries_table(connection)  # Call the function to create the PATIENT_HISTORY_SURGERIES table
    create_patient_history_medications_table(connection)  # Call the function to create the PATIENT_HISTORY_MEDICATIONS table
    create_take_care_of_table(connection)  # Call the function to create the TAKE_CARE_OF table
    create_works_in_table(connection)  # Call the function to create the WORKS_IN table
    create_test_table(connection)  # Call the function to create the TEST table
    create_requests_table(connection)  # Call the function to create the REQUESTS table
    create_gets_table(connection)  # Call the function to create the GETS table
    create_medicine_table(connection)  # Call the function to create the MEDICINE table
    create_prescribes_table(connection)  # Call the function to create the PRESCRIBES table

#connection = create_server_connection(host, user, password, database)
# Close the database connection
    connection.close()