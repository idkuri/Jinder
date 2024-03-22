from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
import hashlib
from django.db import transaction
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

cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = %s)", ('posts',))
exists = cursor.fetchone()[0]

if not exists:
    create_table_query = '''
        CREATE TABLE posts (
            id SERIAL PRIMARY KEY,
            username VARCHAR NOT NULL,
            content VARCHAR NOT NULL
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

        cursor.execute(insert_query, (body['username'], hashed_password, hashed_token, body['accountType'],salt))
        connector.commit()
        
        #username value;password value;confirmpassword value
        response = HttpResponse("User Registration success, Please return to homepage.")
        response.set_cookie('auth_token', auth_token, max_age=3600, httponly=True)
        return response # Need add a auth_token cookie to HttpResponse
    
    except psycopg2.Error as error:
        # Rollback the transaction in case of an error
        connector.rollback()
        print("Error creating table:", error)

def user_login(request):
    body = json.loads(request.body)
    # print(body['username'])
    select_query = """
        SELECT * FROM users
        WHERE username = %s
    """
    cursor.execute(select_query, (body['username'],))
    rows = cursor.fetchall()
    # print(rows)
    # print(len(rows))
    if len(rows) == 0:
        return HttpResponse("Invalid username, this username is not in server.")
    
    id = rows[0][0]
    hashed_password = rows[0][2]
    auth_token = rows[0][3]
    salt = rows[0][5]

    if hashed_password != hashlib.sha256((body["password"] + salt).encode('utf-8')).hexdigest():
        response = HttpResponse("Wrong password, Please return to homepage.")
        return response # Need add a auth_token cookie to HttpResponse
    
    new_auth_token = secrets.token_hex(8)
    hashed_token = str(hashlib.sha256((new_auth_token).encode('utf-8')).hexdigest())

    update_query = """ UPDATE users
                SET auth_token = %s
                WHERE id = %s"""
    
    cursor.execute(update_query, (hashed_token,id,))
    connector.commit()
    
    response = HttpResponse("User Login")
    response.set_cookie('auth_token', new_auth_token, max_age=3600, httponly=True)
    return response # Need add a auth_token cookie to HttpResponse

# Request will be sent with auth token as cookie
@transaction.atomic
def authenticate(request):
    if 'Cookie' in request.headers:
        # print("hello")
        auth_token = request.COOKIES.get('auth_token')
        if not auth_token:
            return HttpResponse("User not found", status=404)
        hashed_token = str(hashlib.sha256((auth_token).encode('utf-8')).hexdigest())
        select_query = """
            SELECT * FROM users
            WHERE auth_token = %s
        """
        # Assuming `cursor` is defined and is an instance of a database cursor
        with connector.cursor() as cursor:
            cursor.execute(select_query, (hashed_token,))
            rows = cursor.fetchall()
            if len(rows) != 0:
                # print('1')
                # print(rows[0][1])
                return JsonResponse({'username': rows[0][1]}, status=200)
            else:
                print(auth_token)
                return HttpResponse("User not found", status=404)
    else:
        return HttpResponse("User not found", status=404)
        
def logout(request):
    if 'Cookie' in request.headers:
        # print("hello")
        auth_token = request.COOKIES.get('auth_token')
        if not auth_token:
            return HttpResponse("logged out")
        
        response = HttpResponse("logged out")
        response.set_cookie('auth_token', '', max_age=0, httponly=True)
        return response # Need add a auth_token cookie to HttpResponse
            
def createPOST(request):
    if 'Cookie' in request.headers:
        auth_token = request.COOKIES.get('auth_token')
        if not auth_token:
            return HttpResponse("User not found",status = 404)
        hashed_token = str(hashlib.sha256((auth_token).encode('utf-8')).hexdigest())
        select_query = """
            SELECT * FROM users
            WHERE auth_token = %s
        """
        # print(cursor)
        cursor.execute(select_query, (hashed_token,))
        rows = cursor.fetchall()
        connector.commit()

        username = rows[0][1]

        insert_query = """
            INSERT INTO posts (username, content)
            VALUES (%s, %s)
        """
        body = json.loads(request.body)
        cursor.execute(insert_query, (username, body['content']))
        connector.commit()

        get_last_query = """SELECT *FROM posts ORDER BY id DESC LIMIT 1;"""
        cursor.execute(get_last_query)
        connector.commit()

        inserted_id = cursor.fetchone()[0]

        response_jsonB = {'id':inserted_id, 'username':username, 'content':body['content']}
        print(response_jsonB)
        response = JsonResponse(response_jsonB)
        return response # Need add a auth_token cookie to HttpResponse

def getPOST(request):
    # some parameter
    if 'id' in request.GET:
        select_query = """
            SELECT * FROM posts
            WHERE id = %s
        """
        cursor.execute(select_query, (request.GET['id'],))
        row = cursor.fetchone()
        res_json = {'username': row[1],'content': row[2]}
        return JsonResponse(res_json, status=200)
    else:
        select_query = """
            SELECT * FROM posts
        """
        cursor.execute(select_query, (request.GET['id'],))
        rows = cursor.fetchall()
        res_json_list = []
        for row in rows:
            res_json = {'username': row[1],'content': row[2]}
            res_json_list.append(res_json)
        return JsonResponse(res_json_list, safe=False, status=200)
# cursor.close()
# connector.close()
