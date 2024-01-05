from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from website.funcs import *

views = Blueprint('views', __name__)

#Formatter to allow the display of the DateTime object from database on screen
@views.app_template_filter('format_seconds_as_time')
def format_seconds_as_time(seconds):
    if seconds is None or not isinstance(seconds, (int, float)):
        return type(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

#login page
@views.route('/')
@login_required
def home():
    return redirect(url_for('auth.login'))

#Admin Page
@views.route('/Admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user:
        #Just some sanity checking for debugging purposes
        #print("User ID:", current_user.id)
        #print("User Role:", current_user.role)
        
        #Choosing a page dependent on current user role
        if current_user.role == 'Nurse':
            return redirect(url_for('views.nurse'))
        elif current_user.role == 'Doctor':
            return redirect(url_for('views.doctor'))
        elif current_user.role == 'Admin':
            if request.method == 'POST':
                action = request.form['action']
                if action == 'search_view_patient_general_info':
                    Pname = request.form['Patient_Name']
                    Dob = request.form['DateOfBirth']

                    result = search_view_patient_general_info(Pname, Dob)
                    session['patient_info_results'] = result
                    return redirect('/GeneralView')
                
                if action == 'view-appointment':
                    result = view_all_appointments()
                    session['appointments'] = result
                    return redirect('/Appt')
                
                if action == "update-patient-info":
                    update_patient_info(request.form['AdminID'],request.form['Admin_Password'],request.form['Patient_Number'],request.form['New_Name'],
                                        request.form['New_Email'],request.form['New_Emerg'],request.form['New_DOB'])
                
                if action == "update-patient-insurance":
                    updatePatientInsurance(request.form['AdminID'],request.form['Admin_Password'],request.form['Patient_Number'],
                                           request.form['New_Policy_Number'],request.form['New_Start_Date'],request.form['New_Dental'],
                                           request.form['New_Drug'],request.form['New_Health'])
                
                if action == "make-appointment":
                    make_appointment(request.form['AdminID'],request.form['Admin_Password'], request.form['Patient_Number'], 
                                     request.form['DoctorID'], request.form['Date'], request.form['Time'],)
                    
                if action == "delete-appointment":
                    delete_appointment(request.form['AdminID'],request.form['Admin_Password'],request.form['Appointment_Number'])

                if action == "reschedule-appointment":
                    reschedule_appointment(request.form['AdminID'], request.form['Admin_Password'], request.form['Appointment_Number'],
                                           request.form['DoctorID'], request.form['New_Date'], request.form.get('New_Time'))
                    
                if action == "assign-nurse-to-patient":
                    assign_nurse_to_patient(request.form['AdminID'], request.form['Admin_Password'], 
                                            request.form['NurseID'], request.form['Patient_Number'])
                    
                if action == "update-doctor-information":
                    update_doctor_information(request.form['AdminID'], request.form['Admin_Password'],
                                              request.form['DoctorID'], request.form['Email'],
                                              request.form['First_Name'], request.form['Last_Name'],
                                              request.form['Department_Number'], request.form['Doctor_Hours'])
                    
                if action == "add-patient-info":
                    addPatientInfo(request.form['AdminID'],request.form['Admin_Password'],request.form['New_Name'], 
                                   request.form['New_Email'],request.form['New_Emerg'],request.form['New_DOB'])


            return render_template("Admin.html")
    else:
        # Handle the case where current_user is None (not logged in)
        return redirect(url_for('auth.login'))

#Doctor Page
@views.route('/Doctor', methods=['GET', 'POST'])
@login_required
def doctor():
    if current_user:
        #Just some sanity checking for debugging purposes
        #print("User ID:", current_user.id)
        #print("User Role:", current_user.role)
        
        #Choosing a page dependent on current user role
        #Nurses cannot access Doctor Dashboard
        if current_user.role == 'Nurse':
            return redirect(url_for('views.nurse'))
        elif current_user.role == 'Doctor':
            if request.method == 'POST':
                data_received = request.form.to_dict()
                print(data_received)
                action = request.form.get('action')
                if action == 'search_view_patient_general_info':
                    Pname = request.form['Patient_Name']
                    Dob = request.form['DateOfBirth']

                    result = search_view_patient_general_info(Pname, Dob)
                    session['patient_info_results'] = result
                    return redirect('/GeneralView')
                
                if action == 'view-appointment':
                    result = view_all_appointments()
                    session['appointments'] = result
                    return redirect('/Appt')
                
                if action == 'add-patient-history':
                    addPatientHistory(request.form['Patient_Number'], request.form['File_Number'],
                                      request.form['Allergy'], request.form['Surgery'],request.form['Medication'])
                if action == 'requests-test':
                    requestTests(request.form['DoctorID'], request.form['Patient_Number'], 
                                request.form['Test_Name'])
                if action == 'gets-test':
                    patientGetsTest(request.form['DoctorID'], request.form['Patient_Number'], 
                                request.form['Test_Name'], request.form['Tester'], request.form['Test_Date'], 
                                request.form['Results'])
                    
                if action == 'prescribe-medicine':
                    prescribeMedicine(request.form['DoctorID'], request.form['Patient_Number'], 
                                request.form['Drug_Number'])
                    
                if action == 'delete-patient-history':
                    delete_patient_history(request.form['DoctorID'],request.form['Doctor_Password'], request.form['Patient_Number'], 
                                request.form['File_Number'], request.form['Allergy'], request.form['Surgery'], 
                                request.form['Medication'])
                    
            return render_template("Doctor.html")
        #Admins cannot access Doctor Dashboard - Redirect
        elif current_user.role == 'Admin':
            return redirect(url_for('views.admin'))
    else:
        # Handle the case where current_user is None (not logged in)
        return redirect(url_for('auth.login'))
    

#Nurse Page
@views.route('/Nurse', methods=['GET', 'POST'])
@login_required
def nurse():
    if current_user:
        #Just some sanity checking for debugging purposes
        #print("User ID:", current_user.id)
        #print("User Role:", current_user.role)
        
        #Choosing a page dependent on current user role
        if current_user.role == 'Nurse':
            if request.method == 'POST':
                action = request.form['action']
                if action == 'search_view_patient_general_info':
                    Pname = request.form['Patient_Name']
                    Dob = request.form['DateOfBirth']

                    result = search_view_patient_general_info(Pname, Dob)
                    session['patient_info_results'] = result
                    return redirect('/GeneralView')
                if action == 'view-appointment':
                    result = view_all_appointments()
                    session['appointments'] = result
                    return redirect('/Appt')
            
            return render_template("Nurse.html")
        #Doctor cannot access Nurse Dashboard - redirect
        elif current_user.role == 'Doctor':
            return redirect(url_for('views.doctor'))
        #Admin cannot access Nurse Dashboard - redirect
        elif current_user.role == 'Admin':
            return redirect(url_for('views.admin'))
    else:
        # Handle the case where current_user is None (not logged in)
        return redirect(url_for('auth.login'))

#Dashboard Page - redirects based on User role
@views.route('/dashboard')
@login_required
def dashboard():
    if current_user:
        #Just some sanity checking for debugging purposes
        print("User ID:", current_user.id)
        print("User Role:", current_user.role)
        
        #Choosing a page dependent on current user role
        if current_user.role == 'Nurse':
            return redirect(url_for('views.nurse'))
        elif current_user.role == 'Doctor':
            return redirect(url_for('views.doctor'))
        elif current_user.role == 'Admin':
            return redirect(url_for('views.admin'))
    else:
        # Handle the case where current_user is None (not logged in)
        return redirect(url_for('auth.login'))
    
#ViewPatientInfoPage
@views.route('/GeneralView')
@login_required
def general():
    patient_info = session.pop('patient_info_results', None)
    return render_template("GeneralView.html", patient_info=patient_info)

#ViewAppointemntPage
@views.route('/Appt')
@login_required
def appt():
    appointments = session.pop('appointments', None)
    return render_template("Appt.html", appointments = appointments)