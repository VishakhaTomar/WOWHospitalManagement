from os import error, write
import streamlit as st
import datetime
from configparser import ConfigParser
import logging
import re
import pandas as pd
import hashlib

import base64
import mysql.connector

 

from streamlit.type_util import OptionSequence
#import psycopg2

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'


def query_db(sql: str):
    print(sql)
    # print(f'Running query_db(): {sql}')
    mydb = mysql.connector.connect(user="mail.id", password="password", 
                                host="hostname", port=0000, 
                                database="dbname")

  # Open a cursor to perform database operations
    cur = mydb.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()

    column_names = [desc[0] for desc in cur.description]

    # Make the changes to the database persistent

    # Close communication with the database
    cur.close()
    mydb.close()

    df = pd.DataFrame(data=data, columns=column_names)

    return df

# For procedures
def insert_query_db(sql: str,arg ):
    print(sql)
    print(arg)
    # print(f'Running query_db(): {sql}')
    # print(f'Running query_db(): {sql}')
    mydb = mysql.connector.connect(user="mail.id", password="password", 
                                host="hostname", port=0000, 
                                database="dbname")
                                
  # Open a cursor to perform database operations
    cur = mydb.cursor()


    # Execute a command: this creates a new table
    x=cur.callproc(sql, args=arg)
    print(x)

    # Make the changes to the database persistent
    mydb.commit()

    # Close communication with the database
    cur.close()
    mydb.close()
    return x


# for simple queries


def insert_simplequery(sql: str):
    print(sql)
    # print(f'Running query_db(): {sql}')

    # Connect to an existing database
    conn = mysql.connector.connect(user="mail.id", password="password", 
                                host="hostname", port=0000, 
                                database="dbname")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()
    return

@st.cache

def make_hashes(password):  #make hashes of the password
	return hashlib.sha256(str.encode(password)).hexdigest()  


def check_hashes(password, hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

def add_userdata(username, hashedpassword,type):
	insert_query_db(
	    f'INSERT INTO usertable(username,userpassword,usertype) VALUES ( \'{username}\',\'{hashedpassword}\',\'{type}\');')
	return

def login_user(username, hashedpassword):
    return query_db(f'SELECT count(1) as found FROM usertable WHERE username =\'{username}\' AND userpassword = \'{hashedpassword}\';')['found'].loc[0]


def login_usertype(username, hashedpassword):
    return query_db(f'SELECT usertype FROM usertable WHERE username =\'{username}\' AND userpassword = \'{hashedpassword}\';')


def searchid(table,key):
    list=query_db(f'select * from {table};')
    temp = list[f'{key}'].tolist()
    temp.insert(0,' ')
    return temp

def searchrecord(sql,table,key,id):
    list=query_db(f'{sql}')
    record=pd.DataFrame()
    record=query_db(f'Select {key} from {table} where treatmentid={id};')
    if record.empty:
        record=pd.DataFrame( {key:[' ']})
        print(record[key][0])
        temp=list[f'{key}'].tolist()
        temp.insert(0,record[key][0])
    else:
        print(record)
        temp=list[f'{key}'].tolist()
        

    return temp

def dma(action,id,procedure:str,args):
    if action=="Add":
        if st.button("Create"):
            result=insert_query_db(f'{procedure}',(args))
            print(result)
            if result:
                st.write("Added")
                return result
                 
    elif action=="Modify":
        if st.button('Modify'):
            result=insert_query_db(f'{procedure}',(args))
            print(result)
            if result:
                st.write("Modified")
                return result
    
    elif action=="Delete": 
        st.write(f'The {id} will be deleted, are you sure you want to delete?')
        if st.button(f"Yes!{action}"):
            result=insert_query_db(f'{procedure}',(args))
            print(result)
            if result:
                st.write("Deleted")
                return result



########## Data Warehouse ##########


def query_db_dw(sql: str):
    print(sql)
    # print(f'Running query_db(): {sql}')
    mydb = mysql.connector.connect(user="mail.id", password="password", 
                                host="hostname", port=0000, 
                                database="dbname")

  # Open a cursor to perform database operations
    cur = mydb.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()

    column_names = [desc[0] for desc in cur.description]

    # Make the changes to the database persistent

    # Close communication with the database
    cur.close()
    mydb.close()

    df = pd.DataFrame(data=data, columns=column_names)

    return df


def insert_query_db_dw(sql: str,arg ):
    print(sql)
    print(arg)
    # print(f'Running query_db(): {sql}')
    # print(f'Running query_db(): {sql}')
    mydb = mysql.connector.connect(user="mail.id", password="password", 
                                host="hostname", port=0000, 
                                database="dbname")
                                
  # Open a cursor to perform database operations
    cur = mydb.cursor()

    # Open a cursor to perform database operations
    cur = mydb.cursor()

    # Execute a command: this creates a new table
    x=cur.callproc(sql, args=arg)
    print(x)

    # Make the changes to the database persistent
    mydb.commit()

    # Close communication with the database
    cur.close()
    mydb.close()
    return x
