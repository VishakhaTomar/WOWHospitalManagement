
from email.policy import default
from os import error, write
from termios import TIOCM_LE
from xml.etree.ElementInclude import include
from numpy import empty
import streamlit as st
import datetime
from configparser import ConfigParser
import logging
import re
import pandas as pd
import hashlib
import base64
import mysql.connector
import functions
import dw_postgres

#.streamlit/config.toml
#primaryColor="#040404"
#secondaryBackgroundColor="#43aab5"
#textColor="#0e0e0e"


#streamlit/config.toml


def main():
    today=datetime.date.today()  #using variable for system date in all the code

    # st.markdown(page_bg_img, unsafe_allow_html=True)
    st.title("WE Offer Wellness (WOW)")
    st.header("Your Health Our Responsibility")

    st.sidebar.subheader("Login Section")
    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password", type='password')
    if st.sidebar.checkbox("Login"):  #also change password option 
            hashed_pswd = functions.make_hashes(password)
            result = functions.login_user(username, functions.check_hashes(password, hashed_pswd))
            print(result)
            if result:
                st.write("Logged In as {}".format(username))
                userType = functions.login_usertype(username, functions.check_hashes(password, hashed_pswd))
                user = userType['usertype'].loc[0]
                if user =='A':
                    print("Welcome Admin")
                    temp = ['Add employee account','Modify/Delete employee account','Backup']  #admin will add frontdesk account,
                                                                                #backoffice acount
                    choice = st.selectbox('Menu', temp)
                    if choice =='Backup':
                        st.write("Select button for backup")
                        coldw=st.columns(2)
                        with coldw[0]:
                            dw_postgres.stage()
                        with coldw[1]:
                            dw_postgres.dw()
                    if choice == 'Add employee account':
                        with st.form("employee_account_form"):
                            new_user = st.text_input("Username")
                            new_password = st.text_input("Password", type='password')
                            user_type =st.text_input("Account type(A for admin,B for Backoffice,F for frontdesk)")    #[A for admin,B for Backoffice,F for frontdesk]
                            submitted1 = st.form_submit_button('Create')
                        if submitted1:
                            hashed_pswd = functions.make_hashes(new_password)
                            result=functions.insert_query_db('add_usertable', (new_user,hashed_pswd,user_type,"A",0, 0))   #Add procedure for insert in user table
                            print(result)
                            if result:
                                st.success("User created")
                    
                    if choice =='Modify/Delete employee account':
                        accountlist=functions.query_db(f'select * from usertable;')
                        temp = accountlist['USERNAME'].tolist()
                        temp.insert(0,' ')
                        searchusername=st.selectbox("Choose the account",temp)
                        
                        if searchusername != ' ':
                            option=st.radio('Choose:',('Modify','Delete'),args=None)

                        
                            if option=='Modify':
                                userid=accountlist.loc[accountlist['USERNAME']== searchusername,'ID'].iloc[0]
                                new_user=st.text_input("Username")
                                new_password=st.text_input("New Password", type='password')
                                user_type=st.text_input("Account type(A for admin,B for Backoffice,F for frontdesk)")
                                print(userid,new_user,new_password,user_type)

                                if st.button('Submit'):
                                    hashed_pswd = functions.make_hashes(new_password)
                                    result=functions.insert_query_db('add_usertable', (new_user,hashed_pswd,user_type,'U', int(userid),0))
                                    print(result)
                                    if result:
                                        st.success("Modified")

                            if option=='Delete':
                                
                                userid=accountlist.loc[accountlist['USERNAME']== searchusername,'ID'].iloc[0]
                                st.write(f'The {userid} will be deleted, are you sure you want to delete?')
                                if st.button("Yes!Delete"):
                                    result=functions.insert_query_db('add_usertable', ('x','x','x','D', int(userid),0))
                                    print(result)
                                    if result:
                                        st.success("Deleted")
                        
                
                if user=='B': #backoffice login
                    temp=['Hospital', 'Doctor','Insurance Plan','Disease information','Rooms', 'Department', 'Lab/Drugs/Surgery']
                    choice =st.selectbox('Menu',temp)
                    if choice =="Hospital":
                        chose=st.selectbox("Action",['Add','Modify/Delete'])
                        if chose=="Add":
                            hospitalname=st.text_input("Hospital Name")
                            st.write("Address")
                            col11 = st.columns(3)
                            col12=st.columns(3)
                            col13=st.columns(3)
                            
                            with col11[0]:
                                plotno = st.text_input('Plot no', max_chars=30)
                            with col11[1]:
                                street = st.text_input('Street', max_chars=30)                            
                            with col11[2]:
                                city = st.text_input('City', max_chars=30)
                            with col12[0]:
                                state = st.text_input('State', max_chars=30)                                            
                            with col12[1]:
                                zipcode = st.text_input('Zipcode', max_chars=10)                                   
                            with col12[2]:
                                speciality= st.text_input('Speciality', max_chars=10)   
                            with col13[0]:
                                ecc_hotline = st.number_input('Ecc-Hotline', min_value=999999999, max_value=9999999999)
                            with col13[1]:
                                phone = st.number_input('Phone no', min_value=999999999, max_value=9999999999)
                            with col13[2]:
                                adminPhone = st.number_input('Administration phone No', min_value=999999999, max_value=9999999999)
                            functions.dma("Add","x",'add_hospital', (hospitalname,plotno,street,city,state,zipcode,speciality,ecc_hotline,phone,adminPhone, "A",0, 0))
                       
                        if chose=="Modify/Delete":
                            hospitallist=functions.searchid('hospital','hid')
                            searchhospital=st.selectbox("Choose the hospital you want to modify",hospitallist)
                            if searchhospital !=' ':
                                option=st.radio('Options',['Modify','Delete'] )
                                if option=="Modify":
                                    hospitalname=st.text_input("Hospital Name")
                                    col11 = st.columns(3)
                                    col12=st.columns(3)
                                    col13=st.columns(3)
                                    with col11[0]:
                                        plotno = st.text_input('Plot no', max_chars=30)
                                    with col11[1]:
                                        street = st.text_input('Street', max_chars=30)                            
                                    with col11[2]:
                                        city = st.text_input('City', max_chars=30)
                                    with col12[0]:
                                        state = st.text_input('State', max_chars=30)                                            
                                    with col12[1]:
                                        zipcode = st.text_input('Zipcode', max_chars=10)                                   
                                    with col12[2]:
                                        speciality= st.text_input('Speciality', max_chars=10)   
                                    with col13[0]:
                                        ecc_hotline = st.number_input('Ecc-Hotline', min_value=999999999, max_value=9999999999)
                                    with col13[1]:
                                        phone = st.number_input('Phone no', min_value=999999999, max_value=9999999999)
                                    with col13[2]:
                                        adminPhone = st.number_input('Administration phone No', min_value=999999999, max_value=9999999999)
                                    functions.dma("Modify","x",'add_hospital', (hospitalname,plotno,street,city,state,zipcode,speciality,ecc_hotline,phone,adminPhone, "M",int(searchhospital), 0))

                                if option=="Delete": 
                                    functions.dma("Delete",searchhospital,'add_hospital', ('x','x','x','x','x','x',0,0,0,'D', int(searchhospital),0))

                    if choice =="Doctor":
                        chose=st.selectbox("Action",['Add Doctor Personal Information','Modify/Delete Doctor Personal Information','Add doctor schedule','Modify/Delete Doctor Schedule'])
                        if chose=="Add Doctor Personal Information":
                            col21 = st.columns(2)
                            col22=st.columns(3)
                            col23=st.columns(3)
                            col24=st.columns(3)
                            with col21[0]:
                                firstname = st.text_input('First Name', max_chars=30)
                            with col21[1]:
                                lastname = st.text_input('Last Name', max_chars=30)
                            with col22[0]:
                                houseno = st.text_input('House No', max_chars=30)
                            with col22[1]:
                                docstreet = st.text_input('Street', max_chars=30)
                            with col22[2]:
                                doccity = st.text_input('City', max_chars=30)
                            with col23[0]:
                                docstate = st.text_input('State', max_chars=30)                                            
                            with col23[1]:
                                doczipcode = st.text_input('Zipcode', max_chars=10)                                   
                            with col23[2]:
                                offphone = st.number_input('Office Phone No', min_value=999999999, max_value=9999999999)
                            with col24[0]:
                                perphone = st.number_input('Personal Phone no', min_value=999999999, max_value=9999999999)
                            with col24[1]:
                                eccPhone = st.number_input('Emergency phone No', min_value=999999999, max_value=9999999999)
                            with col24[2]:
                                eccname= st.text_input('Emergency contact Name', max_chars=30)                                
                            docspeciality= st.text_input('Speciality', max_chars=10)                            
                            functions.dma("Add","x",'add_doctor', (firstname,lastname,houseno,docstreet,doccity,docstate,doczipcode,offphone,perphone,eccPhone,eccname,docspeciality,"A",0, 0))
                        
                        if chose=="Modify/Delete Doctor Personal Information":
                            doctorid= functions.searchid('doctor','did')
                            searchdoctor=st.selectbox("Choose the Doctor ID",doctorid)
                            if searchdoctor !=' ':
                                docname=functions.query_db(f'select firstname,lastname from doctor where did={searchdoctor}').loc[0]
                                st.write("Doctor name: " + str(docname['firstname']) +" "+ str(docname['lastname']))
                                option=st.radio('Options',['Modify','Delete'] )
                                if option=="Modify":
                                    col21=st.columns(2)
                                    col22=st.columns(3)
                                    col23=st.columns(3)
                                    col24=st.columns(3)
                                    with col21[0]:
                                        firstname = st.text_input('First Name', max_chars=30)
                                    with col21[1]:
                                        lastname = st.text_input('Last Name', max_chars=30)
                                    with col22[0]:
                                        houseno = st.text_input('House No', max_chars=30)
                                    with col22[1]:
                                        docstreet = st.text_input('Street', max_chars=30)
                                    with col22[2]:
                                        doccity = st.text_input('City', max_chars=30)
                                    with col23[0]:
                                        docstate = st.text_input('State', max_chars=30)                                            
                                    with col23[1]:
                                        doczipcode = st.text_input('Zipcode', max_chars=10)                                   
                                    with col23[2]:
                                        offphone = st.number_input('Office Phone No', min_value=999999999, max_value=9999999999)
                                    with col24[0]:
                                        perphone = st.number_input('Personal Phone no', min_value=999999999, max_value=9999999999)
                                    with col24[1]:
                                        eccPhone = st.number_input('Emergency phone No', min_value=999999999, max_value=9999999999)
                                    with col24[2]:
                                        eccname= st.text_input('Emergency contact Name', max_chars=30)                                        
                                    docspeciality= st.text_input('Speciality', max_chars=10)                                    
                                    functions.dma("Modify","x",'add_doctor', (firstname,lastname,houseno,docstreet,doccity,docstate,doczipcode,offphone,perphone,eccPhone,eccname,docspeciality,"M",searchdoctor, 0))
                                if option=="Delete": 
                                    functions.dma("Delete",searchdoctor,'add_doctor',('x','x','x','x','x','x','x',0,0,0,'x','x',"D",searchdoctor,0))


                        if chose=="Add doctor schedule":
                            coldoc=st.columns(3)
                            coldoc2=st.columns(3)
                            coldoc3=st.columns(3)
                            doctorid= functions.searchid('doctor','did')
                            hospitallist=functions.searchid('hospital','hid')
                            with coldoc[0]:
                                searchdoctor=st.selectbox("Choose the Doctor ID",doctorid)
                            with coldoc[1]:
                                hospitalid=st.selectbox("Choose the hospital ID ",hospitallist)
                            with coldoc[2]:
                                doctype=st.selectbox("Doctor work status",['Full Time','Consulting'])
                            hiredate=today
                            fulsalary=0
                            contractstartdate=today
                            contractno='x'
                            contractenddate=today
                            hours=0
                            consalary=0
                            overtimerate=0
                            shift='x'
                            if doctype=="Full Time":
                                chardoctype='F'
                                colft=st.columns(2)
                                with colft[0]:
                                    hiredate=st.date_input('Hire date', max_value=today)
                                with colft[1]:
                                    fulsalary=st.number_input('Salary per hour', max_value=99999.99)
                            if doctype=="Consulting":
                                chardoctype='C'
                                with coldoc2[0]:
                                    contractstartdate=st.date_input('Contract start date', max_value=today)
                                with coldoc2[1]:
                                    contractno=st.text_input('Contract no', max_chars=30)
                                with coldoc2[2]:
                                    contractenddate=st.date_input('Contract start date', min_value=today)
                                with coldoc3[0]:
                                    hours=st.number_input('Visiting hours ', max_value=24.00)
                                with coldoc3[1]:
                                    consalary=st.number_input('Salary per hour', max_value=99999.99)
                                with coldoc3[2]:
                                    overtimerate=st.number_input('Overtime Salary per hour', max_value=99999.99)
                                shift=st.text_input('Shift day',max_chars=7)
                            functions.dma("Add","x",'add_doctorhospital', (chardoctype,searchdoctor,hospitalid,hiredate,fulsalary,contractstartdate,contractno,contractenddate,hours,consalary,overtimerate,shift,"A", 0))
                    
                        if chose=="Modify/Delete Doctor Schedule":
                            coldoc=st.columns(2)
                            
                            doctorid= functions.searchid('doctor','did')
                            hospitallist=functions.searchid('hospital','hid') 
                            with coldoc[0]:
                                searchdoctor=st.selectbox("Choose the Doctor ID",doctorid)
                            with coldoc[1]:
                                hospitalid=st.selectbox("Choose the hospital ID ",hospitallist)
                            if searchdoctor !=' ' and hospitalid !=' ' :
                                option=st.radio('Options',['Modify','Delete'] )
                                if option=="Modify":
                                    doctype=st.selectbox("Doctor work status",['Full Time','Consulting'])
                                    hiredate=today
                                    fulsalary=0
                                    contractstartdate=today
                                    contractno='x'
                                    contractenddate=today
                                    hours=0
                                    consalary=0
                                    overtimerate=0
                                    shift='x'
                                    if doctype=="Full Time":
                                        chardoctype='F'
                                        colft=st.columns(2)
                                        with colft[0]:
                                            hiredate=st.date_input('Hire date', max_value=today)
                                        with colft[1]:
                                            fulsalary=st.number_input('Salary per hour', max_value=99999.99)
                                    if doctype=="Consulting":
                                        chardoctype='C'
                                        coldoc2=st.columns(3)
                                        coldoc3=st.columns(3)
                                        with coldoc2[0]:
                                            contractstartdate=st.date_input('Contract start date', max_value=today)
                                        with coldoc2[1]:
                                            contractno=st.text_input('Contract no', max_chars=30)
                                        with coldoc2[2]:
                                            contractenddate=st.date_input('Contract start date', min_value=today)
                                        with coldoc3[0]:
                                            hours=st.number_input('Visiting hours ', max_value=24.00)
                                        with coldoc3[1]:
                                            consalary=st.number_input('Salary per hour', max_value=99999.99)
                                        with coldoc3[2]:
                                            overtimerate=st.number_input('Overtime Salary per hour', max_value=99999.99)
                                        shift=st.text_input('Shift day',max_chars=30)
                                    functions.dma("Modify","x",'add_doctorhospital', (chardoctype,searchdoctor,hospitalid,hiredate,fulsalary,contractstartdate,contractno,contractenddate,hours,consalary,overtimerate,shift,"M", 0))
                                if option=="Delete":
                                    functions.dma("Delete",searchdoctor,'add_doctorhospital', ('C',searchdoctor,hospitalid,today,0,today,'x',today,0,0,0,'x',"D", 0))

                        #First form Add doctor detail
                        # Second form add doctor type detail, get hospital id from select command, add details

                    if choice =="Rooms" :
                        #Chose hostpital id from the select command then add details
                        temp=functions.searchid('hospital','hid')
                        searchhospital=st.selectbox("Choose the hospital you want to modify",temp)
                        if searchhospital !=' ':
                            col41 = st.columns(2)
                            col42=st.columns(2)
                            with col41[0]:
                                RoomNo = st.text_input('Room no', max_chars=30)
                            with col41[1]:
                                Floor = st.text_input('Floor', max_chars=30)                            
                            with col42[0]:
                                Building = st.text_input('Building', max_chars=30)
                            with col42[1]:
                                Cost = st.number_input('Cost per night', max_value=10000.0)

                            functions.dma("Add","x",'add_rooms', (RoomNo,Floor,Building,Cost,'Y',"A",int(searchhospital), 0))                                            
   
                    
                    if choice =="Department":
                        #Chose hostpital id from the select command then add details
                        temp=functions.searchid('hospital','hid')
                        searchhospital=st.selectbox("Choose the hospital for adding the department",temp)
                        if searchhospital !=" ":
                            col51 = st.columns(2)
                            col52=st.columns(2)
                            with col51[0]:
                                deptname= st.text_input('Department name', max_chars=30) 
                            with col51[1]:
                                deptphoneno= st.number_input('Department phone No', min_value=999999999, max_value=9999999999)
                            with col52[0]:
                                deptbuilding= st.text_input('Department building name', max_chars=30)
                            with col52[1]: 
                                deptfloor= st.text_input('Department floor', max_chars=30)
                            functions.dma("Add","x",'add_department', (deptname,deptphoneno,deptbuilding,deptfloor,"A",int(searchhospital),0, 0))
                   
                    if choice =="Insurance Plan":
                        chose=st.selectbox("Action",['Add','Modify/Delete'])
                        if chose=="Add":
                            st.write("Add Insuance information")
                            col71 = st.columns(2)
                            col72=st.columns(2)
                            with col71[0]:
                                insurancename= st.text_input('insurance name', max_chars=30) 
                            with col71[1]:
                                insuranceprovider= st.text_input('insurance provider Name')
                            with col72[0]:
                                inPatientCoverage= st.number_input('in-Patient Coverage', min_value=0.0, max_value=99.99) 
                            with col72[1]:
                                outPatientCoverage= st.number_input('out-Patient Coverage', min_value=0.0, max_value=99.99)
                            functions.dma("Add","x",'add_insurance', (insurancename,insuranceprovider,inPatientCoverage,outPatientCoverage,"A",0, 0))
                           
                        if chose=="Modify/Delete":
                            insuranceID=functions.searchid('insurance_plan','planid')
                            searchInsrncplan=st.selectbox("Choose the Plan ID",insuranceID)
                            if searchInsrncplan != ' ':
                                st.write(functions.query_db(f"select insurancename from insurance_plan where planid=\'{searchInsrncplan}\'")['insurancename'].loc[0])
                                option=st.radio('Choose:',('Modify','Delete'),args=None)
                                if option=='Modify':
                                    col71 = st.columns(2)
                                    col72=st.columns(2)
                                    with col71[0]:
                                        insurancename= st.text_input('insurance name', max_chars=30) 
                                    with col71[1]:
                                        insuranceprovider= st.text_input('insurance provider Name')
                                    with col72[0]:
                                        inPatientCoverage= st.number_input('in-Patient Coverage', min_value=0.0, max_value=99.99) 
                                    with col72[1]:
                                        outPatientCoverage= st.number_input('out-Patient Coverage', min_value=0.0, max_value=99.99)
                                    functions.dma("Modify","x",'add_insurance', (insurancename,insuranceprovider,inPatientCoverage,outPatientCoverage,"M",int(searchInsrncplan), 0))
                                
                                if option=='Delete':
                                    functions.dma("Delete",searchInsrncplan,'add_insurance', ('x','x','x','x','D', int(searchInsrncplan),0))

                                    
                    if choice =="Disease information":
                        col61 = st.columns(2)
                        col62 = st.columns(2)
                        with col61[0]:
                            icdcodes= st.text_input('ICD Code for the disease', max_chars=30) 
                        with col61[1]:
                            diseasename= st.text_input('Name of the disease') 
                        with col62[0]:
                            description= st.text_input('Discription of the disease') 
                        with col62[1]:
                            diseasetype= st.text_input(' Disease Type(Seasonal/chronic/viral/genetic..etc)', max_chars=30)

                        functions.dma("Add","x",'add_disease', (icdcodes,diseasename,description,diseasetype,"A", 0))

                    if choice=="Lab/Drugs/Surgery":
                        labbutton=st.selectbox('Choose Action',['Lab Information','Drugs Information','Surgery Information'])
                        if labbutton=="Lab Information":
                            chose=st.selectbox("Action",['Add','Modify/Delete'])
                            if chose=="Add":
                                col8=st.columns(3)
                                with col8[0]:
                                    labname= st.text_input('Lab name', max_chars=30) 
                                with col8[1]:
                                    labcost= st.number_input('Lab cost', min_value=0.0, max_value=99.99)
                                with col8[2]:
                                    labsample=st.text_input('Kind of sample require in Lab', max_chars=30) 
                                functions.dma("Add","x",'add_lds', ('L',labname,labcost,labsample,'x',0,'x','x',0,'A',0,0))

                            if chose=="Modify/Delete":
                                Lablist=functions.query_db(f'select * from lab;')
                                labtempid=functions.searchid('lab','labname')
                                searchlab=st.selectbox("Choose the Lab",labtempid)
                                if searchlab != ' ':
                                    labid=Lablist.loc[Lablist['labname']== searchlab,'labid'].iloc[0]
                                    if searchlab != ' ':
                                        option=st.radio('Choose:',('Modify','Delete'),args=None)
                                        if option=='Modify':
                                            col8=st.columns(3)
                                            with col8[0]:
                                                labname= st.text_input('Lab name', max_chars=30) 
                                            with col8[1]:
                                                labcost= st.number_input('Lab cost', min_value=0.0, max_value=99.99)
                                            with col8[2]:
                                                labsample=st.text_input('Kind of sample require in Lab', max_chars=30) 
                                            functions.dma("Modify","x",'add_lds', ('L',labname,labcost,labsample,'x',0,'x','x',0,'M',int(labid),0))
                                        if option=='Delete':
                                            functions.dma("Delete",searchlab,'add_lds', ('L','x',0,'x','x',0,'x','x',0,'D',int(labid),0))

                        if labbutton=="Drugs Information":
                            chose=st.selectbox("Action",['Add','Modify/Delete'])
                            if chose=="Add":
                                col9=st.columns(2)
                                with col9[0]:
                                    prescriptionname= st.text_input('prescription name', max_chars=30) 
                                with col9[1]:
                                    drugcost= st.number_input('Drug cost per dose', min_value=0.0, max_value=99.99)                    
                                functions.dma("Add","x",'add_lds', ('D','x',0,'x',prescriptionname,drugcost,'x','x',0,'A',0,0))
                            if chose=="Modify/Delete":
                                st.write("Hold tight!!Feature coming up soon")

                        if labbutton=="Surgery Information":
                            chose=st.selectbox("Action",['Add','Modify/Delete'])
                            if chose=="Add":
                                col10=st.columns(3)
                                with col10[0]:
                                    surgeryname= st.text_input('Surgery name', max_chars=30) 
                                with col10[1]:
                                    surgerydescription=st.text_input('Description', max_chars=30)
                                with col10[2]:
                                    surgerycost= st.number_input('Surgery Cost', min_value=0.0, max_value=9999.99)                    
                                functions.dma("Add","x",'add_lds', ('S','x',0,'x','x',0,surgeryname,surgerydescription,surgerycost,'A',0,0))
                            if chose=="Modify/Delete":
                                st.write("Hold tight!!Feature coming up soon")


                
                if user=='F': #fornt desk login
                    temp=['New patient', 'Existing Patient']
                    choice =st.selectbox('Menu',temp)
                    if choice =='New patient':
                        st.write("Enter Patient Detail")
                        col1 = st.columns(2)
                        col2=st.columns(3)
                        col3=st.columns(3)
                        col4=st.columns(3)
                        col5=st.columns(3)
                        with col1[0]:
                            fname = st.text_input('First name', max_chars=30)
                        with col1[1]:
                            lname = st.text_input('Last name', max_chars=30)                           
                        with col2[0]:
                            pthousenum = st.text_input('House Number', max_chars=30)                           
                        with col2[1]:
                            ptstreet = st.text_input('street Number', max_chars=30)                           
                        with col2[2]:
                            ptcity = st.text_input('City', max_chars=30)                           
                        with col3[0]:
                            ptstate = st.text_input('State', max_chars=30)
                        with col3[1]:
                            ptzipcode = st.text_input('Zipcode', max_chars=10)
                        with col3[2]:
                            ptcontact_number = st.number_input('contact number', min_value=999999999, max_value=9999999999)
                        with col4[0]:
                            ptdob = st.date_input('Date of Birth', max_value=today)
                        with col4[1]:
                            ptRace = st.selectbox('Race', ['Asian','American','South Asian','African'])#add from an application
                        with col4[2]:
                            Maritial_Status = st.selectbox('Maritial Status', ['Married','Single','Divored','Widowed'])#add from an application
                        with col5[0]:
                            ptgender = st.selectbox('Gender', ['M', 'F','O'])
                        with col5[1]:
                            blood_group = st.selectbox('Blood Group', ['A+','A-','B+','B-','AB+','AB-','O+','O-'])
                        with col5[2]:
                            plan_name=st.selectbox("Insurance plan",functions.searchid('insurance_plan','insurancename'))
                        result=functions.dma("Add","x",'add_patient',('P',fname,lname,pthousenum,ptstreet,ptcity,ptstate,ptzipcode,ptcontact_number,ptdob,ptRace,Maritial_Status,ptgender,blood_group,plan_name,'A',0,0))
                        if result:
                            patid=functions.query_db(f'select MAX(PID) as patid from patients')['patid'].loc[0]
                            st.write("Patient ID is "+ str(patid))
                            st.write("Enter Emergency Contact")

                            if st.button(f'Add Ecc Contact'):
                                with st.form("Ecc_form"):
                                    EccCol1=st.columns(2)
                                    with EccCol1[0]:
                                        eccfname = st.text_input('Enter your First name', max_chars=30)
                                    with EccCol1[1]:
                                        ecclname = st.text_input('Enter your Last name', max_chars=30)
                                    EccCol2=st.columns(3)
                                    with EccCol2[0]:
                                        ecchousenum = st.text_input('House Number', max_chars=30)
                                    with EccCol2[1]:
                                        eccstreet = st.text_input('street Number', max_chars=30)
                                    with EccCol2[2]:
                                        ecccity = st.text_input('City', max_chars=30)
                                    EccCol3=st.columns(3)
                                    with EccCol3[0]:
                                        eccstate = st.text_input('State', max_chars=30)
                                    with EccCol3[1]:
                                        ecczipcode = st.text_input('Zipcode', max_chars=10)
                                    with EccCol3[2]:
                                        ecccontact_number = st.number_input('contact number', min_value=999999999, max_value=9999999999)
                                    relationship = st.text_input('Enter your your relationship to the person', max_chars=30)
                                    submitted3=functions.dma("Add","x",'add_patient',('E',eccfname,ecclname,ecchousenum,eccstreet,ecccity,eccstate,ecczipcode,ecccontact_number,today,relationship,'Maritial_Status','x','x',0,'A',patid,0))
                                    if submitted3:
                                        st.write("Added Emergency Contact")



                    if choice=='Existing Patient' :
                        patientID=st.selectbox("Patient ID",functions.query_db('select PID from patients')['PID'].tolist())
                        if st.checkbox('Search'): 
                            checkid=functions.query_db(f'select count(1) as found from patients where pid={patientID}')['found'].loc[0]
                            if checkid:
                                patdetail=functions.query_db(f'select * from patients where pid={patientID}')
                                colpat=st.columns(2)
                                with colpat[0]:
                                    st.write("Patient Name:"+str(patdetail['firstname'].loc[0])+" "+ str(patdetail['lastname'].loc[0]))
                                with colpat[1]:
                                    st.write("DOB:"+str(patdetail['dob'].loc[0]))
                                #userid=accountlist.loc[accountlist['USERNAME']== searchusername,'ID'].iloc[0]
                            
                                expatlist=['Make new Registration','Book Appointments','CheckIn Appointments','Update existing Registration','Invoice']
                                choice1=st.selectbox('Choose',expatlist)
                                if choice1== "Make new Registration":
                                    reg_date=st.date_input("Registration Date")
                                    print(reg_date)
                                    hospitalid=st.selectbox('Hospital ID',functions.searchid('hospital','hid'))
                                    pattype= st.selectbox("Patinet Type", ['Out-patient', 'In-Patient'])
                                    discharge_date=today
                                    followup=today
                                    roomNo=0
                                    if pattype=="Out-patient":
                                        patient_type='O'
                                    else:
                                        patient_type='I'
                                    if pattype=="Out-patient":
                                        followup=st.date_input('Follow-up date', min_value=today)                                    
                                    if pattype=="In-Patient":
                                        roomNo=st.selectbox('Room No',functions.query_db(f'select roomno from rooms where hid={hospitalid}')['roomno'].tolist())
                                        discharge_date=st.date_input('Discharge Date')
                                    result=functions.dma("Add",'x','pat_registration',(patientID,reg_date,hospitalid,patient_type,followup,roomNo,discharge_date,'A',0))
                                    if result:
                                        st.success(f"Your regsitration successfull for {patientID} on date {reg_date}.For future reference use Patient ID and registration date for accessing this registration")    

                                if choice1=="Book Appointments":
                                    hospitalid=st.selectbox('Hospital ID',functions.searchid('hospital','hid'))
                                    tempspecialitylist= functions.query_db(f'select distinct speciality from doctor')['speciality'].tolist()
                                    tempspecialitylist.insert(0,' ')
                                    speciality=st.selectbox('Specialilty', tempspecialitylist)                                
                                    #speciality=st.selectbox('Specialilty', functions.searchid('doctor','speciality'))
                                    #SQL for finding the doctors who are full time on the selected hospital and with the selected speciality
                                    if st.checkbox('find'):
                                        aptid=0
                                        fulltime=functions.query_db(f'select a.firstname, a.lastname from doctor a join full_time b on a.did=b.did where b.hid={hospitalid} and a.speciality=\'{speciality}\';')
                                        Consultant=functions.query_db(f'select a.firstname, a.lastname, b.shift , b.hours from doctor a join consulting b on a.did=b.did where b.hid={hospitalid} and a.speciality=\'{speciality}\';')
                                        shifts=Consultant['shift'].loc[0]
                                        shiftday=()
                                        if '1' in shifts:
                                            shiftday.append('Monday')
                                        if '2' in shifts:
                                            shiftday.append('Tuesday')
                                        if '3' in shifts:
                                            shiftday.append('Wednesday')
                                        if '4' in shifts:
                                            shiftday.append('Thursday')
                                        if '5' in shifts:
                                            shiftday.append('Friday')
                                        if '6' in shifts:
                                            shiftday.append('Saturday')
                                        if '7' in shifts:
                                            shiftday.append('Sunday')
                                        shift=','.join(shiftday)
                                        Consultant.pop('shift')
                                        Consultant['shift']=[shift]
                                    #SQL : select shift from consulting where speciality ={speciality} and HID={HID}
                                        st.write("Full time Doctors:")
                                        st.table(fulltime)  #displaying full time doctors
                                        st.write("Visiting Doctors and Schedule:")
                                        st.table(Consultant ) #displaying visiting doctors, so acc to schedule date can be chosen
                                        apptDate = st.date_input('Next Appointment date',min_value=today)

                                    #SQL: Insert into pat_appointment(PID,NextvisitDateSchedued) values(PID,apptDate);
                                        if st.button("Book"):
                                            result=functions.insert_query_db('appointments',('B',patientID,apptDate,'A',aptid,0))
                                            print(result)
                                            if result:
                                                st.success("Appointment is booked, The appointment ID is "+ str(functions.query_db(f'select MAX(appointmentid) as aptid from pat_appointment')['aptid'].loc[0]))

                                                #display max that is the appointment ID 

                                if choice1 =="CheckIn Appointments":
                                    # AppointmentID =st.selectbox("Appointment ID",functions.searchid('pat_appointment','appointmentid'))
                                    AppointmentID= st.selectbox("Appointment ID",functions.query_db(f"select appointmentid from pat_appointment where PID={patientID}")['appointmentid'].tolist())
                                    if AppointmentID !=' ':
                                        if st.button("Check-In"):
                                            status = functions.query_db(f'select visitdatecheckin as found from pat_appointment where appointmentid= {AppointmentID}')['found'].loc[0]
                                            if status =='N':
                                                functions.insert_query_db('appointments',('C',0,today,'A',AppointmentID,0))
                                                st.success("You are checked-in!")
                                            else:
                                                st.write("You are already checked-in!")
                               
                                if choice1=="Update existing Registration":
                                    tempreglist=functions.query_db(f'select reg_date from patient_reg where pid={patientID}')['reg_date'].tolist()
                                    tempreglist.insert(0,' ')
                                    treg_date=st.selectbox("Registration Date",tempreglist) #search reg date                                    
                                    #treg_date=st.selectbox("Registration Date",functions.searchid('patient_reg','reg_date')) #search reg date
                                    
                                    if treg_date != ' ':
                                        checktreactmentid=functions.query_db(f'select count(1) as found from treatment where pid={patientID} and reg_date=\'{treg_date}\'')['found'].loc[0]  #search if any treatment record exists
                                        if checktreactmentid:   #if record exists
                                            treatmentlist=functions.query_db(f'select treatmentid from treatment where pid={patientID} and reg_date=\'{treg_date}\'')['treatmentid'].tolist()
                                            treatmentlist.insert(0,' ')
                                            treatmentid=st.selectbox("Select treatment ID",treatmentlist)  #listing all the treatmetn ids for the patient and reg date
                                            if treatmentid !=' ':
                                                hospitalid=functions.query_db(f'select hid from treatment where treatmentid = {treatmentid};')['hid'].loc[0]
                                        #display treatments details if any present  #display in the editable columns?
                                                Disease=st.selectbox("Treatment for disease",functions.searchrecord('select icdcode from disease','treatment','icdcode',treatmentid))
                                                typeresult=functions.query_db(f'select treatmenttype from treatment where treatmentid ={treatmentid}')['treatmenttype'].loc[0]
                                                if typeresult=='L':
                                                    indexfortype=1
                                                elif typeresult=='D':
                                                    indexfortype=2
                                                elif typeresult=='S':
                                                    indexfortype=3
                                                else :
                                                    indexfortype=0
                                                trtmnttype=st.selectbox("Treatment Type",[' ','Lab Test','Drug Prescription','Surgery'], index=indexfortype)
                                                treatingdoctor=st.selectbox("Doctor",functions.searchrecord(f'select b.did from hospital_doctor a join doctor b on a.did = b.did where hid = {hospitalid}','treatment','did',treatmentid))
                                                st.write("Doctor Name :", str(functions.searchid('doctor','firstname')[1])+' '+str(functions.searchid('doctor','lastname')[1]))
                                                treatmentdiscription=st.text_input("Doctor's diagnosis",value=functions.query_db(f'select description from treatment where treatmentid ={treatmentid}')['description'].loc[0])
                                                trtmentstroredresult=functions.query_db(f'select treatmentresult from treatment where treatmentid ={treatmentid}')['treatmentresult'].loc[0]
                                                if trtmentstroredresult=='O':
                                                    indexfortreatmentresult=0
                                                elif trtmentstroredresult=='T':
                                                    indexfortreatmentresult=1
                                                elif trtmentstroredresult=='F':
                                                    indexfortreatmentresult=2
                                                elif trtmentstroredresult=='C':
                                                    indexfortreatmentresult=3 
                                                trtmentresult=st.selectbox("Treatment status",['Ongoing','Terminated','Failed','Completed'], index=indexfortreatmentresult)
                                                treatmnt_type = trtmnttype[0]
                                                treatmentresult=trtmentresult[0]
                                                trtmntdate=today
                                                labsurgeryID=0
                                                labsur_result='x'
                                                trtdrugid=0
                                                doses=0
                                                if treatmnt_type=='L':
                                                    trtmntdate=st.date_input("Lab test date", value=functions.query_db(f'select testdate from p_lab where treatmentid ={treatmentid}')['testdate'].loc[0])
                                                    labsurgeryID=st.selectbox("Lab ID",functions.searchrecord('select labid from lab;','p_lab','labid',treatmentid))
                                                    storedresult=functions.query_db(f'select result from p_lab where treatmentid ={treatmentid}')['result'].loc[0]
                                                    if storedresult=='P':
                                                        indexforresult=1
                                                    elif storedresult=='N':
                                                        indexforresult=2
                                                    elif storedresult=='p':
                                                        indexforresult=3
                                                    else :
                                                        indexforresult=0
                                                    labsurresult=st.selectbox("Lab Test Result",['Awaiting','Positive','Negative','Potential'],index=indexforresult)
                                                    labsur_result=labsurresult[0]
                                                elif treatmnt_type=='D':
                                                    trtdrugid=st.selectbox("Drugname",functions.searchrecord('select drupid from drug_prescription;','p_drug_pres','drupid',treatmentid))
                                                    doses=st.number_input("Doses",value=functions.query_db(f'select doses from p_drug_pres where treatmentid ={treatmentid}')['doses'].loc[0])
                                                elif treatmnt_type=='S':
                                                    trtmntdate=st.date_input("Surgery date", value=functions.query_db(f'select SurgeryDate from p_surgery where treatmentid ={treatmentid}')['SurgeryDate'].loc[0])
                                                    labsurgeryID=st.selectbox("Surgery ID",functions.searchrecord('select surgeryid from surgery;','p_surgery','surgeryid',treatmentid))
                                                    storedresult=functions.query_db(f'select result from p_surgery where treatmentid ={treatmentid}')['result'].loc[0]
                                                    if storedresult=='U':
                                                        indexforresult=1
                                                    elif storedresult=='S':
                                                        indexforresult=2
                                                    else :
                                                        indexforresult=0
                                                    labsurresult=st.selectbox("Surgery Result",['Awaiting','Unsuccessful','Successful'],index=indexforresult)
                                                    labsur_result=labsurresult[0]
                                                if st.button("Update Treatment record"):  #button for update treatment record
                                                    result=functions.insert_query_db('add_treatment',(int(patientID), str(treg_date),int(hospitalid),int(treatingdoctor),Disease,treatmentdiscription,treatmnt_type,treatmentresult,trtmntdate,int(labsurgeryID),labsur_result,int(trtdrugid),doses,'U',int(treatmentid),0))
                                                    if result:
                                                        st.success(f"The Treatment {treatmentid} is updated")

                                        else:
                                            st.write("No treatment record added yet")
                                        if st.checkbox("Add Treatment Record"):
                                            hospitalid=functions.query_db(f'select hid from patient_reg where pid={patientID} and reg_date=\'{treg_date}\';')['hid'].loc[0]
                                            Disease=st.selectbox("Treatment for disease",functions.searchid('disease','icdcode'))
                                            trtmnttype=st.selectbox("Treatment Type",[' ','Lab Test','Drug Prescription','Surgery'])
                                            treatingdoctor=st.selectbox("Doctor",functions.query_db(f'select did from hospital_doctor where hid = {hospitalid};')['did'].tolist())
                                            treatmentdiscription=st.text_input("Doctor's diagnosis")
                                            trtmentresult=st.selectbox("Treatment status",[' ','Ongoing','Terminated','Failed','Completed'])
                                            treatmnt_type = trtmnttype[0]
                                            treatmentresult=trtmentresult[0]
                                            trtmntdate=today
                                            labsurgeryID=0
                                            labsur_result='x'
                                            trtdrugid=0
                                            doses=0
                                            if treatmnt_type=='L':
                                                trtmntdate=st.date_input("Lab test date")
                                                labsurgeryname=st.selectbox("Lab Name",functions.searchid('lab','labname'))
                                                if labsurgeryname != " ":
                                                    labsurgeryID=functions.query_db(f'select labid from lab where labname = \'{labsurgeryname}\'')['labid'].loc[0]
                                                labsurresult=st.selectbox("Lab Test Result",[' ','Awaiting','Positive','Negative','Potential'])
                                                labsur_result=labsurresult[0]
                                            elif treatmnt_type=='D':
                                                trtdrugid=st.selectbox("Drug name",functions.searchid('drug_prescription','drupid'))
                                                doses=st.number_input("Doses")
                                            elif treatmnt_type=='S':
                                                trtmntdate=st.date_input("Surgery date")
                                                labsurgeryID=st.selectbox("Surgery ID",functions.searchid('surgery','surgeryid'))
                                                labsurresult=st.selectbox("Surgery Result",[' ','Awaiting','Unsuccessful','Successful'])
                                                labsur_result=labsurresult[0]
                                            if st.button("Add"):
                                                result=functions.insert_query_db('add_treatment',(patientID, str(treg_date),int(hospitalid),treatingdoctor,Disease,treatmentdiscription,treatmnt_type,treatmentresult,trtmntdate,int(labsurgeryID),labsur_result,trtdrugid,doses,'A',0,0))
                                                if result:
                                                    st.success("Treatment record added " + str(functions.query_db(f'select MAX(treatmentid) as treatmentid from treatment')['treatmentid'].loc[0]))
                                if choice1=="Invoice":
                                    tempreglist=functions.query_db(f'select reg_date from patient_reg where pid={patientID}')['reg_date'].tolist()
                                    tempreglist.insert(0,' ')
                                    treg_date=st.selectbox("Registration Date",tempreglist) #search reg date                                    
                                    
                                    #treg_date=st.selectbox("Registration Date",functions.searchid('patient_reg','reg_date')) #search reg date

                                    #if no invoice found, display no invoice
                                    if treg_date !=' ':
                                        if len(functions.query_db(f'select * from invoice where pid={patientID} and reg_date=\'{treg_date}\';'))==0:
                                            st.write("No invoice found")
                                        else: #if invoice found, display invoice
                                            st.write("Invoice--")
                                            invoiceid=functions.query_db(f'select * from invoice where pid={patientID} and reg_date=\'{treg_date}\';')

                                            for l in range(len(invoiceid)):
                                                st.write("********************************************************************")
                                                st.write(f"Invoice ID: {invoiceid['invoiceno'].loc[l]}")
                                                st.write(f"Invoice Date: {invoiceid['InvoiceDate'].loc[l]}")
                                                st.write(f"Patient ID: {invoiceid['pid'].loc[l]}")
                                                st.write(f"Registration Date: {invoiceid['reg_date'].loc[l]}")
                                                st.write(f"Lab cost: ${invoiceid['labcost'].loc[l]}")
                                                st.write(f"Presciption Drug: {invoiceid['prescriptionname'].loc[l]}")
                                                st.write(f"Drug cost: ${invoiceid['drugcost'].loc[l]}")
                                                st.write(f"Surgery cost: ${invoiceid['surgerycost'].loc[l]}")
                                                st.write(f"Room cost: ${invoiceid['roomcost'].loc[l]}")
                                                totalcost=invoiceid['labcost'].loc[l]+invoiceid['drugcost'].loc[l]+invoiceid['surgerycost'].loc[l]+invoiceid['roomcost'].loc[l]
                                                st.write(f"Total cost: ${totalcost}")
                                                st.write(f"Payable by Insurance: ({invoiceid['payablebyinsurance'].loc[l]}%) ${totalcost*(invoiceid['payablebyinsurance'].loc[l]/100)}")
                                                payablebypateint=100-invoiceid['payablebyinsurance'].loc[l]
                                                st.write(f"Payable by Patient: ({payablebypateint}%) ${totalcost*(payablebypateint/100)}")
                                                functions.insert_simplequery(f'update invoice set payablebypatient={payablebypateint} where pid={patientID} and reg_date=\'{treg_date}\';')
                                                functions.insert_simplequery(f'update invoice set totalcost = {totalcost} where pid={patientID} and reg_date=\'{treg_date}\';')
                                                st.write("********************************************************************")
                                            if st.button("Proceed to make Payment"):
                                                st.write("Payment--")
                                                st.write("Payment complete")

    #found=f'#SQL:select count(1) as found from patient where pid = {PID} and reg_date={Reg_Date}'
                                    
                                        
                            else:
                                st.write("Patient ID not found, try again")

                                #when found display side by side patient and insurance company invoice
                                #button to print invoice

            else : 
                st.write('Username or password is incorrect')                   
    if st.sidebar.checkbox('Change Password/Forgot Password'):
        status=functions.query_db(f'select accstatus from usertable where username="{username}"')['accstatus'].loc[0]
        if status=='A':
            st.write("First time login, please change password and add security question")
            newpassword=st.text_input("New Password",type='password' )
            sec_ques=st.text_input("Security Question")
            sec_ans=st.text_input("Security Answer")        
            if st.button("Change"):
                hashedpwd=functions.make_hashes(newpassword)
                if hashedpwd==functions.query_db(f'select USERPASSWORD from usertable where USERNAME=\'{username}\'')['USERPASSWORD'].loc[0]:
                    st.write("New password cannot be the same as old password")
                else:
                    functions.insert_simplequery(f'update usertable set USERPASSWORD=\'{hashedpwd}\', secQuest=\'{sec_ques}\', secans=\'{sec_ans}\', accstatus=\'R\' where USERNAME=\'{username}\'')
                    st.success("Password changed")
        elif status=='R':
            st.write("Authorised user,Please enter your security answer")
            st.write(functions.query_db(f'select secQuest from usertable where USERNAME="{username}"')['secQuest'].loc[0])
            sec_ans=st.text_input("Security Answer")
            if st.checkbox("Check"):
                if sec_ans==functions.query_db(f'select secans from usertable where USERNAME="{username}"')['secans'].loc[0]:
                    newpassword=st.text_input("Enter New Password", type = 'password')
                    hashedpwd=functions.make_hashes(newpassword)
                    if st.button("Update"):
                        if hashedpwd==functions.query_db(f'select USERPASSWORD from usertable where USERNAME="{username}"')['USERPASSWORD'].loc[0]:
                            st.write("New password cannot be the same as old password")
                        else:
                            functions.insert_simplequery(f'update usertable set USERPASSWORD="{hashedpwd}" where USERNAME="{username}"')
                            st.success("Password Updated")
                else:
                    st.write("Security answer is incorrect")
        else:
            st.write("User not found, please contact admin")



main()

