from os import error, write
import streamlit as st
import datetime
from configparser import ConfigParser
import logging
import re
import pandas as pd
import hashlib
import psycopg2
import base64
import mysql.connector
import functions
import numpy as np
import psycopg2.extras as extras

server = 'ap-data-warehouse.postgres.database.azure.com'
username = 'VishakhaTomar@ap-data-warehouse'
password = 'Zaq1@wsx'   
print('starting connection')
def insert_single(insertqery,schema):
    try:
        print(insertqery)
        conn = psycopg2.connect(host=server,port = '5432',dbname=schema,user=username,password=password)
        print(conn)
        cursor = conn.cursor() #create a cursor
        print(cursor)
        cursor.execute(insertqery) #load data 
        conn.commit() #Close the cursor and connection
        cursor.close()
        conn.close()
    except Exception as e:
        print(f'Error: {e}')

def insert_multiple_stage(df, table):
  
    tuples = [tuple(x) for x in df.to_numpy()]
  
    cols = ','.join(list(df.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    
    conn = psycopg2.connect(host=server,port = '5432',dbname='staging',user=username,password=password)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor,query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("the dataframe is inserted")
    cursor.close()
    conn.close()

def insert_multiple_dw(df, table):
  
    tuples = [tuple(x) for x in df.to_numpy()]
  
    cols = ','.join(list(df.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    
    conn = psycopg2.connect(host=server,port = '5432',dbname='dw',user=username,password=password)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("the dataframe is inserted")
    cursor.close()
    conn.close()


def query_stage(query):
    conn = psycopg2.connect(host=server,port = '5432',dbname='staging',user=username,password=password)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    conn.commit()
    cursor.close()
    conn.close()
    df = pd.DataFrame(data=data, columns=column_names)
    return df

    
oltplist= ['hospital','hdepartment','doctor','hospital_doctor','full_time','consulting','rooms','patients','patient_reg','inPatient','outPatient','treatment','p_drug_pres','p_lab','p_surgery','invoice']
stagelist= ['STG_hospital','STG_hdepartment','STG_doctor','STG_hospital_doctor','STG_full_time','STG_consulting','STG_rooms','STG_patients','STG_patient_reg','STG_inPatient','STG_outPatient','STG_treatment','STG_p_drug_pres','STG_p_lab','STG_p_surgery','STG_invoice']

# insertstagetable=f'Insert into {stagelist[0]} values (?,?,?,?,?,?,?,?,?,?,?,?)'

if st.button('Backup'):
    for i,j in zip(oltplist,stagelist):
        print(i,j)
        truncatestage=f'TRUNCATE TABLE {i};'
        result=insert_single(truncatestage,'staging')
        print(result)

        insertoltptable=functions.query_db(f'select * from {i} where tbl_last_date> (select lastupdatetime from backuptime);')
        result=insert_multiple_stage(insertoltptable, j)
        print(result)

    updatetime=functions.insert_query_db(f'update backuptime set lastupdatetime= sysdate() where id =1;')
    print(updatetime)

# insertoltptable=functions.query_db(f'select * from hospital_doctor;')
# result=execute_values(0,insertoltptable, 'STG_hospital_doctor')
# print(result)

# insertoltptable=functions.query_db(f'select * from inPatient where tbl_last_date< (select lastupdatetime from backuptime);')
# result=insert_multiple_stage(insertoltptable, 'STG_inPatient')
# print(result)

# insertoltptable=functions.query_db(f'select * from outPatient where tbl_last_date< (select lastupdatetime from backuptime);')
# result=insert_multiple_stage(insertoltptable, 'STG_outPatient')
# print(result)

if st.button('Push to DW'):        
    hospital_query_ft=query_stage(f'''select d.hid, b.hname,b.city, b.state,b.zipcode,b.speciality,a.did as dptid , a.dname , a.buildingname,a.floor,c.roomno,c.cost,
                                d.did, e.firstname, e.lastname, e.speciality as docspeciality, d.type as doctype,f.hiredate, f.salary as full_salary
                                from 
                                stg_hdepartment a, stg_hospital b,stg_rooms c,stg_hospital_doctor d,stg_doctor e ,stg_full_time f
                                where 
                                    a.hid = b.hid and
                                    c.hid = b.hid and
                                    d.hid = b.hid and
                                    f.hid = d.hid and
                                    e.did= d.did and
                                    d.did = f.did ''')
    result1 = insert_multiple_dw(hospital_query_ft, 'dw_hospital')
    print(result1)
    hospital_query_con=query_stage(f'''select d.hid,b.city, b.state,b.zipcode,b.speciality,a.did as dptid , a.dname , a.buildingname,a.floor,c.roomno,c.cost,
                                    d.did, e.firstname, e.lastname, e.speciality as docspeciality, d.type as doctype, g.contractdate, g.contractenddate, g.hours, g.salary as con_salary, g.overtimerate,
                                    g.shift
                                    from
                                    stg_hdepartment a, stg_hospital b,stg_rooms c,stg_hospital_doctor d,stg_doctor e,stg_consulting g
                                    where 
                                        a.hid = b.hid and
                                        c.hid = b.hid and 
                                        d.hid = b.hid and 
                                        g.hid = d.hid and 
                                        e.did = d.did and 
                                        d.did = g.did  ''')
    result2 = insert_multiple_dw(hospital_query_con, 'dw_hospital')
    print(result2)
    patient_query_in=query_stage(f'''select b.pid,a.firstname,a.lastname,a.city,a.state,a.zipcode,a.dob,a.race, a.maritialstatus, a.gender, a.bloodgroup, a.planid, b.reg_date,b.hid, d.icdcode,b.patient_type,c.dischargedate, c.roomno, d.treatmentid,d.treatmenttype, d.treatmentresult, d.did, e.invoiceno,e.InvoiceDate,e.labcost,e.drugcost, e.surgerycost,e.roomcost, e.totalcost, e.payablebypatient, e.payablebyinsurance
                                    from 
                                    stg_patients a, stg_patient_reg b, stg_inpatient c, stg_treatment d, stg_invoice e
                                    where   b.pid=a.pid and
                                            b.reg_date=c.reg_date and
                                            b.pid=c.pid and
                                            b.pid=d.pid and
                                            b.reg_date=d.reg_date and
                                            b.pid=e.pid and
                                            b.reg_date=e.reg_date''')
    result3 = insert_multiple_dw(patient_query_in, 'dw_patient')
    print(result3)
    patient_query_out=query_stage(f'''select b.pid,a.firstname,a.lastname,a.city,a.state,a.zipcode,a.dob,a.race, a.maritialstatus, a.gender, a.bloodgroup, a.planid, b.reg_date,b.hid, d.icdcode,b.patient_type, d.treatmentid,d.treatmenttype, d.treatmentresult, d.did, e.invoiceno,e.InvoiceDate,e.labcost,e.drugcost, e.surgerycost,e.roomcost, e.totalcost, e.payablebypatient, e.payablebyinsurance
                                    from 
                                    stg_patients a, stg_patient_reg b, stg_outpatient c, stg_treatment d, stg_invoice e
                                    where   b.pid=a.pid and
                                            b.reg_date=c.reg_date and
                                            b.pid=c.pid and
                                            b.pid=d.pid and
                                            b.reg_date=d.reg_date and
                                            b.pid=e.pid and
                                            b.reg_date=e.reg_date''')
    result4 = insert_multiple_dw(patient_query_out, 'dw_patient')
    print(result3)


patient_query_in=query_stage(f'''select b.pid,a.firstname,a.lastname,a.city,a.state,a.zipcode,a.dob,a.race, a.maritialstatus, a.gender, a.bloodgroup, a.planid, b.reg_date,b.hid, d.icdcode,b.patient_type,c.dischargedate, c.roomno, d.treatmentid,d.treatmenttype, d.treatmentresult, d.did, e.invoiceno,e.InvoiceDate,e.labcost,e.drugcost, e.surgerycost,e.roomcost, e.totalcost, e.payablebypatient, e.payablebyinsurance
from 
stg_patients a, stg_patient_reg b, stg_inpatient c, stg_treatment d, stg_invoice e
where   b.pid=a.pid and
        b.reg_date=c.reg_date and
        b.pid=c.pid and
        b.pid=d.pid and
        b.reg_date=d.reg_date and
        b.pid=e.pid and
        b.reg_date=e.reg_date''')
result3 = insert_multiple_dw(patient_query_in, 'dw_patients')
print(result3)
patient_query_out=query_stage(f'''select b.pid,a.firstname,a.lastname,a.city,a.state,a.zipcode,a.dob,a.race, a.maritialstatus, a.gender, a.bloodgroup, a.planid, b.reg_date,b.hid, d.icdcode,b.patient_type, d.treatmentid,d.treatmenttype, d.treatmentresult, d.did, e.invoiceno,e.InvoiceDate,e.labcost,e.drugcost, e.surgerycost,e.roomcost, e.totalcost, e.payablebypatient, e.payablebyinsurance
from 
stg_patients a, stg_patient_reg b, stg_outpatient c, stg_treatment d, stg_invoice e
where   b.pid=a.pid and
        b.reg_date=c.reg_date and
        b.pid=c.pid and
        b.pid=d.pid and
        b.reg_date=d.reg_date and
        b.pid=e.pid and
        b.reg_date=e.reg_date''')
result4 = insert_multiple_dw(patient_query_out, 'dw_patients')
print(result4)
