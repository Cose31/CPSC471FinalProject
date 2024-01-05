import os
import hashlib
import base64
import mysql.connector
from mysql.connector import Error
from database import create_server_connection
from flask import flash
from .models import User
from datetime import timedelta


def verify_password(entered_password, stored_password):
    stored_password_bytes = base64.b64decode(stored_password.encode('utf-8'))
    salt = stored_password_bytes[:16]
    stored_hashed_password = stored_password_bytes[16:]

    entered_hashed_password = hashlib.pbkdf2_hmac('sha256', entered_password.encode('utf-8'), salt, 100000)

    return entered_hashed_password == stored_hashed_password

def userLogin(userID, password):

    connection = funcImplementation()
    #Retrieving Role Type (Nurse, Doctor, Admin) - query 1
    cursor = connection.cursor()
    query = "SELECT UserID, U_Role FROM USER WHERE UserID = %s"
    cursor.execute(query, (userID,))
    result = cursor.fetchone()

    if result:
        stored_user_id, U_Role = result
        user = User(stored_user_id, U_Role)
    else:
        user = None

    #Checking if password is correct - query 2
    query2 = "SELECT UserID, U_Password FROM USER WHERE UserID = %s"
    cursor.execute(query2, (userID,))
    result2 = cursor.fetchone()

    # Check if user_id exists in the database
    if result2:
        stored_user_id2, hashed_password = result2
        # Verify the entered password against the stored hashed password
        if verify_password(password, hashed_password):
            login_success = True  # Successful login
        else:
            flash('Incorrect password, try again.', category='error')
            login_success = False
    else:
        flash('User does not exist.', category='error')
        login_success = False
        user = None

    # Close the database connection
    cursor.close()
    connection.close()
    return login_success, user

def search_view_patient_general_info(name, dob):
    connection = funcImplementation()
    PName = name
    Date_of_birth = dob
    cursor = connection.cursor()

    # Update the query with correct column names
    query = "SELECT Patient_no, PName, Email, Emergency_Contact, Date_of_birth FROM PATIENT WHERE PName = %s AND Date_of_birth = %s"
    cursor.execute(query, (PName, Date_of_birth))

    result = cursor.fetchall()

    if result:
        for row in result:
            print("Patient_no:", row[0], "PName:", row[1], "Email:", row[2], "Emergency_Contact:", row[3],
                    "Date_of_birth:", row[4])
    else:
        print("No matching patient found.")

    cursor.close()
    connection.close()
    return result

# Function to check if a doctor already exists in DB
def doctor_exists(connection, userID):
    cursor = connection.cursor()
    query = """
            SELECT * FROM DOCTOR WHERE D_UserID = %s
            """
    uid = [userID]
    cursor.execute(query, uid)
    result = cursor.fetchall()
    if (result == []):
        return False
    else:
        return True

# Function to check if a patient already exists in DB
def patient_exists(connection, patient_no):
    cursor = connection.cursor()
    query = """
            SELECT * FROM PATIENT WHERE Patient_No = %s
            """
    pn = [patient_no]
    cursor.execute(query, pn)
    result = cursor.fetchall()
    if (result == []):
        return False
    else:
        return True

# Function to check if a test already exists in DB
def test_exists(connection, testName):
    cursor = connection.cursor()
    query = """
            SELECT TestName FROM TEST WHERE TestName = %s
            """

    tn = [testName]
    cursor.execute(query, tn)
    result = cursor.fetchall()

    if (result == []):
        return False
    else:
        return True

# Function to check if a medicine already exists in DB
def medicine_exists(connection, drugNo):
    cursor = connection.cursor()
    query = """
            SELECT * FROM MEDICINE WHERE Drug_No = %s
            """
    dn = [drugNo]
    cursor.execute(query, dn)
    result = cursor.fetchall()
    if (result == []):
        return False
    else:
        return True

# Function to check if an appointment already exists in DB
def appointment_exists(connection, appt_no):
    cursor = connection.cursor()
    query = """
            SELECT * FROM APPOINTMENT WHERE Apt_No = %s
            """
    apt = [appt_no]
    cursor.execute(query, apt)
    result = cursor.fetchall()
    if (result == []):
        return False
    else:
        return True

# Function to add a new patient's general information to DB
def addPatientInfo(AID, APW, PName, Pemail, emerg, PDOB):
    connection = funcImplementation()
    cursor = connection.cursor()

    admin_user_id = AID
    admin_password = APW

    # Check if the user is an admin and verify the password
    if not is_admin(connection, admin_user_id, admin_password):
        print("Authentication failed. Only admins are allowed to update patient information.")
        connection.close() 
        return
    
    # Retrieve the highest current Patient_No and increment it for the new patient
    query_for_patient_no = "SELECT MAX(Patient_No) FROM PATIENT"
    cursor.execute(query_for_patient_no)
    result = cursor.fetchone()
    new_patient_no = 1  # Default starting number if no patients exist
    if result[0] is not None:
        new_patient_no = result[0] + 1

    pname = PName
    email = Pemail
    emergency = emerg
    dob = PDOB

    query = """
                INSERT INTO PATIENT (Patient_No, PName, Email, Emergency_Contact, Date_of_birth)
                VALUES (%s, %s, %s, %s, %s)
                """
    try:
        cursor.execute(query, (new_patient_no, pname, email, emergency, dob))
        connection.commit()
        print(f"New patient added successfully with Patient Number: {new_patient_no}")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        cursor.close()

# Function to add new patient's history to DB
def addPatientHistory(Patient_No, file_No, allergy_in, surgery_in, medication_in):
    connection = funcImplementation()
    patient_no = Patient_No

    cursor = connection.cursor()
    query1 = """
            INSERT INTO PATIENT_HISTORY (File_No, Patient_No)
            VALUES (%s, %s)
            """
    query2 = """
            INSERT INTO PATIENT_HISTORY_ALLERGIES (File_No, Patient_No, Allergies)
            VALUES (%s, %s, %s)
            """
    query3 = """
            INSERT INTO PATIENT_HISTORY_SURGERIES (File_No, Patient_No, Surgeries)
            VALUES (%s, %s, %s)
            """
    query4 = """
            INSERT INTO PATIENT_HISTORY_MEDICATIONS (File_No, Patient_No, Medications)
            VALUES (%s, %s, %s)
            """
    if patient_exists(connection, patient_no):
        try:
            file_no = file_No
            allergies = allergy_in
            surgeries = surgery_in
            medications = medication_in
            cursor.execute(query1, (file_no, patient_no))
            if allergies is not None:
                cursor.execute(query2, (file_no, patient_no, allergies))
            if surgeries is not None:
                cursor.execute(query3, (file_no, patient_no, surgeries))
            if medications is not None:
                cursor.execute(query4, (file_no, patient_no, medications))
            connection.commit()
            print("Patient history added successfully")
        except Error as err:
            print(f"Error: '{err}'")
    else:
        print("Patient does not exists in the system. First create the patient")

    cursor.close()

# Function to add a new patient's insurance to DB
def addPatientInsurance(patient_No, policy_No, startDateIn, dentalIn, drugIn, healthIn):
    connection = funcImplementation()
    patient_no = patient_No

    cursor = connection.cursor()
    query = """
            INSERT INTO INSURANCE (Policy_No, Patient_No, StartDate, Dental_Coverage, Drug_Coverage, Health_Coverage)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
    if patient_exists(connection, patient_no):
        try:
            policy_no = policy_No
            startDate = startDateIn
            dental = dentalIn
            drug = drugIn
            health = healthIn
            cursor.execute(query, (policy_no, patient_no, startDate, dental, drug, health))
            connection.commit()
            print("Patient insurance added successfully")
        except Error as err:
            print(f"Error: '{err}'")

    else:
        print("Patient does not exists in the system. First create the patient")

    cursor.close()

def requestTests(dID, p_No, tName):
    connection = funcImplementation()
    cursor = connection.cursor()
    dUserId = dID
    query = """
            INSERT INTO REQUESTS (TestName, D_UserID, Patient_No)
            VALUES(%s, %s, %s)
            """
    if doctor_exists(connection, dUserId):
        patient_no = p_No
        if patient_exists(connection, patient_no):
            testName = tName
            if test_exists(connection, testName):
                try:
                    cursor.execute(query, (testName, dUserId, patient_no))
                    connection.commit()
                    print("Test request initiated successfully")
                except Error as err:
                    print(f"Error: '{err}'")

            else:
                print("Test requested does not exist")
        else:
            print("Patient requested does not exist")
    else:
        print("Doctor requesting test does not exist")

    cursor.close()

def patientGetsTest(dID, pNo, testName, tester, testDateIn, results):
    connection = funcImplementation()
    cursor = connection.cursor()
    dUserId = dID  #doctor ID which is getting test for patient
    query = """
            INSERT INTO GETS (TestName, D_UserID, Patient_No, Tester, TestDate, Result)
            VALUES(%s, %s, %s, %s, %s, %s)
            """
    if doctor_exists(connection, dUserId):
        patient_no = pNo
        if patient_exists(connection, patient_no):
            testName = testName
            if test_exists(connection, testName):
                try:
                    tester = tester
                    testDate = testDateIn
                    result = results
                    cursor.execute(query, (testName, dUserId, patient_no, tester, testDate, result))
                    connection.commit()
                    print("Test results successfully added")
                except Error as err:
                    print(f"Error: '{err}'")

            else:
                print("Test name entered does not exist")
        else:
            print("Patient number entered does not exist")
    else:
        print("Doctor trying to add test results does not exist")

    cursor.close()

def prescribeMedicine(dID, pNo, dNo):
    connection = funcImplementation()
    cursor = connection.cursor()
    dUserId = dID
    query = """
            INSERT INTO PRESCRIBES (Drug_No, D_UserID, Patient_No)
            VALUES(%s, %s, %s)
            """

    if doctor_exists(connection, dUserId):
        patient_no = pNo
        if patient_exists(connection, patient_no):
            drugNo = dNo
            if medicine_exists(connection, drugNo):
                try:
                    cursor.execute(query, (drugNo, dUserId, patient_no))
                    connection.commit()
                    print("Medicine prescribed successfully")
                except Error as err:
                    print(f"Error: '{err}'")

            else:
                print("Medicine prescribed does not exist")
        else:
            print("Patient requested does not exist")
    else:
        print("Doctor prescribing medicine does not exist")

    cursor.close()

# def doctor_for_appointment_exists(connection, d_Userid, appt_no):
#     cursor = connection.cursor()
#     try:
#         query = "SELECT D_UserID FROM APPOINTMENT WHERE Apt_No = %s"
#         cursor.execute(query, (appt_no,))
#         result = cursor.fetchone()
#         if result and result[0] == d_Userid:
#             return True
#         return False
#     except Error as err:
#         print(f"Error: '{err}'")
#         return False
#     finally:
#         cursor.close()

# This function checks if it is the ADMIN who has the accses to update the data
def is_admin(connection, user_id, password):
    cursor = connection.cursor()
    try:
        query = "SELECT U_Role, U_Password FROM USER WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result and result[0].lower() == 'admin':
            stored_password = result[1]
            return verify_password(password, stored_password)
        return False
    except Error as err:
        print(f"Error: '{err}'")
        return False
    finally:
        cursor.close()

# This function checks if it is the DOCTOR who has the access to update the data
def is_doctor(connection, user_id, password):
    cursor = connection.cursor()
    try:
        query = "SELECT U_Role, U_Password FROM USER WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result and result[0].lower() == 'doctor':
            stored_password = result[1]
            return verify_password(password, stored_password)
        return False
    except Error as err:
        print(f"Error: '{err}'")
        return False
    finally:
        cursor.close()

# this funtion update a patient's generel info only by an ADMIN
def update_patient_info(AID, APW, pNo, newName, newEmail, newEmerg, newDOB):

    connection = funcImplementation()
    admin_user_id = AID
    admin_password = APW

    # Check if the user is an admin and verify the password
    if not is_admin(connection, admin_user_id, admin_password):
        print("Authentication failed. Only admins are allowed to update patient information.")
        connection.close() 
        return

    patient_no = pNo
    cursor = connection.cursor()

    # Check if patient exists
    if not patient_exists(connection, patient_no):
        print("Patient does not exist in the system.")
        cursor.close()
        connection.close() 
        return

    new_name = newName
    new_email = newEmail
    new_emergency_contact = newEmerg
    new_dob = newDOB

    cursor = connection.cursor()

    update_fields = []
    params = []

    if new_name:
        update_fields.append("PName = %s")
        params.append(new_name)
    if new_email:
        update_fields.append("Email = %s")
        params.append(new_email)
    if new_emergency_contact:
        update_fields.append("Emergency_Contact = %s")
        params.append(new_emergency_contact)
    if new_dob:
        update_fields.append("Date_of_birth = %s")
        params.append(new_dob)

    if not update_fields:
        print("No updates provided.")
        connection.close() 
        return

    update_query = f"UPDATE PATIENT SET {', '.join(update_fields)} WHERE Patient_No = %s"
    params.append(patient_no)

    try:
        cursor.execute(update_query, tuple(params))
        connection.commit()
        print(f"Patient information updated successfully for patient number {patient_no}.")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        cursor.close()
        connection.close() 

# This funtion update patient's insurance information for a specific patient
def updatePatientInsurance(AID, APW, pNo, newPolNo, newStartDate, newDent, newDrug, newHealth):
    
    connection = funcImplementation()
    admin_user_id = AID
    admin_password = APW

   # Check if the user is an admin and verify the password
    if not is_admin(connection, admin_user_id, admin_password):
        print("Authentication failed. Only admins are allowed to update patient insurance.")
        connection.close() 
        return

    patient_no = pNo
    cursor = connection.cursor()

    # Check if patient exists
    if not patient_exists(connection, patient_no):
        print("Patient does not exist in the system.")
        cursor.close()
        connection.close() 
        return

    # Get new insurance details
    new_policy_no = newPolNo
    new_start_date = newStartDate
    new_dental = newDent
    new_drug = newDrug
    new_health = newHealth

    update_fields = []
    params = []

    # Build query dynamically based on provided inputs
    if new_policy_no:
        update_fields.append("Policy_No = %s")
        params.append(new_policy_no)
    if new_start_date:
        update_fields.append("StartDate = %s")
        params.append(new_start_date)
    if new_dental:
        update_fields.append("Dental_Coverage = %s")
        params.append(new_dental)
    if new_drug:
        update_fields.append("Drug_Coverage = %s")
        params.append(new_drug)
    if new_health:
        update_fields.append("Health_Coverage = %s")
        params.append(new_health)

    if not update_fields:
        print("No updates provided.")
        cursor.close()
        connection.close() 
        return

    update_query = f"UPDATE INSURANCE SET {', '.join(update_fields)} WHERE Patient_No = %s"
    params.append(patient_no)

    try:
        cursor.execute(update_query, tuple(params))
        connection.commit()
        print(f"Patient insurance updated successfully for patient number {patient_no}.")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        cursor.close()

#This function delete patient's history only by a doctor
def delete_patient_history(DID, DPW, pNo, fNo, allergyIn, surgeryIn, medicationIn):
    connection = funcImplementation()
    # Prompt for doctor's credentials
    doctor_user_id = DID
    doctor_password = DPW

    # Verify if the user is a doctor
    if not is_doctor(connection, doctor_user_id, doctor_password):
        print("Access denied. Only doctors can delete patient history.")
        return

    patient_no = pNo
    file_no = fNo

    cursor = connection.cursor()

    if patient_exists(connection, patient_no):
        try:
            # Check and delete allergy history if provided
            current_allergy = allergyIn
            if current_allergy:
                delete_allergy_query = """
                    DELETE FROM PATIENT_HISTORY_ALLERGIES 
                    WHERE Patient_No = %s AND File_No = %s AND Allergies = %s
                """
                cursor.execute(delete_allergy_query, (patient_no, file_no, current_allergy))

            # Check and delete surgery history if provided
            current_surgery = surgeryIn
            if current_surgery:
                delete_surgery_query = """
                    DELETE FROM PATIENT_HISTORY_SURGERIES 
                    WHERE Patient_No = %s AND File_No = %s AND Surgeries = %s
                """
                cursor.execute(delete_surgery_query, (patient_no, file_no, current_surgery))

            # Check and delete medication history if provided
            current_medication = medicationIn
            if current_medication:
                delete_medication_query = """
                    DELETE FROM PATIENT_HISTORY_MEDICATIONS 
                    WHERE Patient_No = %s AND File_No = %s AND Medications = %s
                """
                cursor.execute(delete_medication_query, (patient_no, file_no, current_medication))

            connection.commit()
            print("Patient history deleted successfully.")
        except Error as err:
            print(f"Error: '{err}'")
            connection.rollback()
        finally:
            cursor.close()
    else:
        print("Patient does not exist in the system. Please check the patient number and file number.")


# This function gives the whole table of data about appoinments without any input and can be view by all end user
def view_all_appointments():
    connection = funcImplementation()
    cursor = connection.cursor()

    # Query to select all appointments
    query = "SELECT Apt_No, AptTime, AptDate, D_UserID, Patient_No FROM APPOINTMENT"

    cursor.execute(query)
    results = cursor.fetchall()
    results_with_seconds = []

    if results:
        print("List of All Appointments:")
        for row in results:
            print(f"Apt_No: {row[0]}, AptTime: {row[1]}, AptDate: {row[2]}, D_UserID: {row[3]}, Patient_No: {row[4]}")
            
            apt_time = row[1]  # Assuming row[1] contains a timedelta object
            apt_time_seconds = (apt_time).total_seconds()

            results_with_seconds.append({
                'Apt_No': row[0],
                'AptTime': apt_time_seconds,
                'AptDate': row[2],
                'D_UserID': row[3],
                'Patient_No': row[4]
            })
    else:
        print("No appointments found.")

    cursor.close()
    connection.close()
    return results_with_seconds

# This funtion is for making an appoinment for an existing patient by an ADMIN  and
# assuming that Admin has all the data about the doctor and patient that is needed to make the appoinment
# And assuming the the doctor is avialable.
def make_appointment(AID, APW, pNo, dID, dateIn, timeIn):
    connection = funcImplementation()
    admin_user_id = AID
    admin_password = APW

    # Check if the user is an admin
    if not is_admin(connection, admin_user_id, admin_password):
        print("Authentication failed. Only admins can make appointments.")
        connection.close() 
        return

    patient_no = pNo

    # Check if patient exists
    if not patient_exists(connection, patient_no):
        print("Patient does not exist in the system.")
        connection.close() 
        return


    # Retrieve the highest current Apt_No and increment it for the new appointment
    cursor = connection.cursor()
    query_for_apt_no = "SELECT MAX(Apt_No) FROM APPOINTMENT"
    cursor.execute(query_for_apt_no)
    result = cursor.fetchone()
    new_apt_no = 1  # Default starting number if no appointments exist
    if result[0] is not None:
        new_apt_no = result[0] + 1

    d_user_id = dID
    apt_date = dateIn
    apt_time = timeIn

    # Check if the doctor is available at the given time
    if not is_doctor_available(connection, d_user_id, apt_date, apt_time):
        print("Doctor is not available at the specified time.")
        connection.close() 
        return

    # Create the appointment
    try:
        insert_query = "INSERT INTO APPOINTMENT (Apt_No, AptTime, AptDate, D_UserID, Patient_No) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (new_apt_no, apt_time, apt_date, d_user_id, patient_no))
        connection.commit()
        print(f"Appointment successfully created with Appointment Number: {new_apt_no}.")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        cursor.close()
    
    connection.close() 

#This funtion checks if the doctor is avaiable or not
def is_doctor_available(connection, d_user_id, apt_date, apt_time):
    """
    Checks if the doctor is available at the specified date and time.

    Parameters:
    - connection: Database connection object
    - d_user_id: Doctor's UserID
    - apt_date: Date of the appointment (YYYY-MM-DD)
    - apt_time: Time of the appointment (HH:MM)
    """
    cursor = connection.cursor()

    # Query to check if the doctor has an appointment at the given date and time
    query = "SELECT * FROM APPOINTMENT WHERE D_UserID = %s AND AptDate = %s AND AptTime = %s"
    cursor.execute(query, (d_user_id, apt_date, apt_time))

    result = cursor.fetchone()

    cursor.close()
    
    # If result is None, it means no appointment exists for the doctor at that time, so they are available
    return result is None

# This function deletes an appointment by an admin
def delete_appointment(AID, APW, apptNo):
    connection = funcImplementation()
    admin_user_id = AID
    admin_password = APW

    # Check if the user is an admin and verify the password
    if is_admin(connection, admin_user_id, admin_password):
        appt_no = apptNo

        cursor = connection.cursor()
        delete_query = "DELETE FROM APPOINTMENT WHERE Apt_No = %s"

        try:
            cursor.execute(delete_query, (appt_no,))
            connection.commit()  # Commit the transaction

            # Check if the delete was successful
            if cursor.rowcount > 0:
                print("Appointment deleted successfully.")
            else:
                print("No appointment found with the given appointment number.")

        except Error as err:
            print(f"Error during deletion: '{err}'")  # Return an error message stating "Deletion failed."
        finally:
            cursor.close()
    else:
        print(
            "Authentication failed. User is not an admin or incorrect credentials.")  # Error message, user not found or not admin
    connection.close() 

# This function reschedules an appointment by an admin
def reschedule_appointment(AID, APW, apptNo, dID, newDate, newTime):
    connection = funcImplementation()
    admin_user_id = AID
    admin_password = APW
    # Check if the user is an admin and verify the password
    if not is_admin(connection, admin_user_id, admin_password):
        print("Admin Login UserId and Password does not match")
        connection.close() 
        return
    else:
        appt_no = apptNo
        cursor = connection.cursor()
        if not appointment_exists(connection, appt_no):
            print("Appointment does not exist")
            cursor.close()
            connection.close() 
            return
        d_userId = dID
        if not doctor_exists(connection, d_userId):
            print("Doctor does not exist")
            cursor.close()
            connection.close() 
            return
        new_date = newDate
        new_time = newTime

        if is_doctor_available(connection, d_userId, new_date, new_time):
            update_fields = []
            params = []

            if d_userId:
                update_fields.append("D_UserID = %s")
                params.append(d_userId)
            if new_date:
                update_fields.append("AptDate = %s")
                params.append(new_date)
            if new_time:
                update_fields.append("AptTime = %s")
                params.append(new_time)

            if not update_fields:
                print("No updates provided.")
                connection.close() 
                return

            update_query = f"UPDATE APPOINTMENT SET {', '.join(update_fields)} WHERE Apt_No = %s"
            params.append(appt_no)

            try:
                cursor.execute(update_query, tuple(params))
                connection.commit()
                print(f"Appointment rescheduled successfully for appointment number {appt_no}.")
            except Error as err:
                print(f"Error: '{err}'")
            finally:
                cursor.close()

    connection.close() 


# This function assign a nurse to a patient by an Admin if the nurse is taking care less than 5 patients.
# It also checks that if the patient is already being taken care of by a nurse, then it will inform admin that
# the patient "Patient already assigned to nurse with UserID"
def assign_nurse_to_patient(currentUser, currentUserPW, nID, pNo):
    connection = funcImplementation()
    # Check if the user making the request is an admin
    admin_user_id = currentUser
    admin_password = currentUserPW
    if not is_admin(connection, admin_user_id, admin_password):
        print("Error: User not found or not authorized as admin.")
        connection.close() 
        return

    # Get Nurse_UserID and Patient_no from input
    nurse_user_id = nID
    patient_no = pNo

    # Check if the patient is already assigned to a nurse
    cursor = connection.cursor()
    existing_assignment_query = """
        SELECT N_UserID
        FROM TAKE_CARE_OF
        WHERE Patient_No = %s;
    """
    cursor.execute(existing_assignment_query, (patient_no,))
    existing_assignment = cursor.fetchone()

    if existing_assignment:
        print(f"Patient already assigned to nurse with UserID {existing_assignment[0]}.")
        cursor.close()
        connection.close() 
        return

    # Check how many patients the nurse currently has
    patient_count_query = """
        SELECT COUNT(*)
        FROM TAKE_CARE_OF
        WHERE N_UserID = %s;
    """
    cursor.execute(patient_count_query, (nurse_user_id,))
    no_of_patient = cursor.fetchone()[0]

    # If nurse can take another patient, insert new relationship
    if no_of_patient < 5:
        insert_relationship_query = """
            INSERT INTO TAKE_CARE_OF (N_UserID, Patient_No)
            VALUES (%s, %s);
        """
        try:
            cursor.execute(insert_relationship_query, (nurse_user_id, patient_no))
            connection.commit()
            print("Nurse assigned to patient successfully.")
        except Error as err:
            print(f"Error: '{err}'")
    else:
        # Nurse already has 5 patients
        print("This nurse is already assigned to 5 patients and cannot take more.")

    cursor.close()
    connection.close() 

# This function updates doctor information only by an Admin
def update_doctor_information(currentUser, currentUserPW, dID, email, fName, lName, dNO, dHours):
    connection = funcImplementation()

    """
    Interactively updates both general user information and specific doctor information
    if the user is an admin and the target user is a doctor.

    :param connection: Database connection object.
    """
    # Get admin credentials
    admin_user_id = currentUser
    admin_password = currentUserPW

    # Check if the user is an admin
    if not is_admin(connection, admin_user_id, admin_password):
        print("Access denied. Only admins can update doctor information.")
        connection.close() 
        return False

    # Get doctor's user ID
    doctor_user_id = dID

    cursor = connection.cursor()
    try:
        # Check if the user to be updated is a doctor
        query = "SELECT U_Role FROM USER WHERE UserID = %s"
        cursor.execute(query, (doctor_user_id,))
        result = cursor.fetchone()
        if not result or result[0].lower() != 'doctor':
            print("The specified user is not a doctor.")
            cursor.close()
            connection.close() 
            return False

        # Get updated user data
        print("Enter updated general user information:")
        updated_user_data = {
            'Email': email,
            'Fname': fName,
            'Lname': lName
        }

        # Get updated doctor data
        print("Enter updated specific doctor information:")
        updated_doctor_data = {
            'Dno': dNO,
            'DHours': dHours
        }

        # Update the general user data in users_data table
        query = "UPDATE USER SET Email = %s, Fname = %s, Lname = %s WHERE UserID = %s"
        cursor.execute(query, (updated_user_data['Email'], updated_user_data['Fname'], updated_user_data['Lname'], doctor_user_id))

        # Update the specific doctor data in doctors_data table
        query = "UPDATE DOCTOR SET Dno = %s, DHours = %s WHERE D_UserID = %s"
        cursor.execute(query, (updated_doctor_data['Dno'], updated_doctor_data['DHours'], doctor_user_id))

        connection.commit()
        print("Doctor information updated successfully.")
        return True
    except Error as err:
        print(f"Error: '{err}'")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close() 
 
def funcImplementation():
    host = 'localhost'
    user = 'root'
    password = 'bio'
    database = 'HOSPITAL'

    # Create a database connection
    connection = create_server_connection(host, user, password, database)

    return connection