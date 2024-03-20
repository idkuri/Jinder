from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
import hashlib
import secrets
import psycopg2
from psycopg2 import sql
import json
# Create your views here.
dbsettings = settings.DATABASES['default']
# print("Flag " + str(dbsettings))
connector = psycopg2.connect(
    dbname=dbsettings['NAME'],
    user=dbsettings['USER'],
    password=dbsettings['PASSWORD'],
    host=dbsettings['HOST'],
    port=dbsettings['PORT']
)
cursor = connector.cursor()

cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = %s)", ('users',))
exists = cursor.fetchone()[0]

if not exists:
    create_table_query = '''
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR UNIQUE NOT NULL,
            password VARCHAR NOT NULL,
            auth_token VARCHAR,
            account_type VARCHAR NOT NULL,
            salt VARCHAR NOT NULL
        )
    '''
    cursor.execute(create_table_query)
    connector.commit()

def register_user(request):
    try:
        body = json.loads(request.body)
        if body['password'] != body['confirmPassword']:
            return HttpResponse("Invalid confirm password, Please return to homepage.")
        
        select_query = """
            SELECT * FROM users
            WHERE username = %s
        """
        
        cursor.execute(select_query, (body['username'],))
        rows = cursor.fetchall()
        if len(rows) != 0:
            return HttpResponse("Invalid user, Please return to homepage.")
        
        salt = secrets.token_hex(8) 
        hashed_password = hashlib.sha256((body['password'] + salt).encode('utf-8')).hexdigest()
        auth_token = secrets.token_hex(8)
        hashed_token = str(hashlib.sha256((auth_token).encode('utf-8')).hexdigest())

        insert_query = """
            INSERT INTO users (username, password, auth_token, account_type, salt)
            VALUES (%s, %s, %s, %s, %s)
        """

        print(insert_query)
        cursor.execute(insert_query, (body['username'], hashed_password, hashed_token, body['accountType'],salt))
        connector.commit()
        
        #username value;password value;confirmpassword value
        response = HttpResponse("User Registration success, Please return to homepage.")
        response.set_cookie('auth_token', auth_token)
        return response # Need add a auth_token cookie to HttpResponse
    
    except psycopg2.Error as error:
        # Rollback the transaction in case of an error
        connector.rollback()
        print("Error creating table:", error)

def user_login(request):
    # body = json.loads(request.body)
    # print(body['username'])
    # select_query = """
    #     SELECT * FROM users
    #     WHERE username = %s
    # """
    # cursor.execute(select_query, (body['username'],))
    # rows = cursor.fetchall()
    # print(rows)
    # print(len(rows))
    # if len(rows) == 0:
    #     return HttpResponse("Invalid username, this username is not in server.")
    
    # id = rows[0][0]
    # hashed_password = rows[0][2]
    # auth_token = rows[0][3]
    # salt = rows[0][5]

    # if hashed_password != hashlib.sha256((body["password"] + salt).encode('utf-8')).hexdigest():
    #     response = HttpResponse("Wrong password, Please return to homepage.")
    #     response.set_cookie('auth_token', auth_token)
    #     return response # Need add a auth_token cookie to HttpResponse
    
    # new_auth_token = secrets.token_hex(8)
    # hashed_token = str(hashlib.sha256((new_auth_token).encode('utf-8')).hexdigest())

    # update_query = """ UPDATE vendors
    #             SET auth_token = %s
    #             WHERE id = %s"""
    
    # cursor.execute(update_query, (hashed_token,id,))

    return HttpResponse("User Login")


# cursor.close()
# connector.close()
