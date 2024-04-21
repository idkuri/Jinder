from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
import hashlib
import html
from django.db import transaction
import secrets
import psycopg2
from psycopg2 import sql
import json
from PIL import Image  
from io import BytesIO
import uuid
import os

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
            content VARCHAR NOT NULL,
            file VARCHAR DEFAULT NULL,
            liked VARCHAR[] NOT NULL
        )
    '''
    cursor.execute(create_table_query)
    connector.commit()

cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = %s)", ('chat',))
exists = cursor.fetchone()[0]

if not exists:
    create_table_query = '''
        CREATE TABLE chat (
            id SERIAL PRIMARY KEY,
            username VARCHAR NOT NULL,
            content VARCHAR NOT NULL
        )
    '''
    cursor.execute(create_table_query)
    connector.commit()
cursor.close()


def register_user(request):
    cursor = cursor = connector.cursor()
    try:
        body = json.loads(request.body)
        if html.escape(body['password']) != html.escape(body['confirmPassword']):
            return HttpResponse("Invalid confirm password, Please return to homepage.")
        
        select_query = """
            SELECT * FROM users
            WHERE username = %s
        """
        
        cursor.execute(select_query, (html.escape(body['username']),))
        rows = cursor.fetchall()
        if len(rows) != 0:
            return HttpResponse("Invalid user, Please return to homepage.")
        
        salt = secrets.token_hex(8) 
        hashed_password = hashlib.sha256((html.escape(body['password']) + salt).encode('utf-8')).hexdigest()
        auth_token = secrets.token_hex(8)
        hashed_token = str(hashlib.sha256((auth_token).encode('utf-8')).hexdigest())

        insert_query = """
            INSERT INTO users (username, password, auth_token, account_type, salt)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (html.escape(body['username']), hashed_password, hashed_token, body['accountType'],salt))
        connector.commit()
        
        #username value;password value;confirmpassword value
        response = HttpResponse("User Registration success, Please return to homepage.")
        response.set_cookie('auth_token', auth_token, max_age=3600, httponly=True)
        cursor.close()
        return response # Need add a auth_token cookie to HttpResponse
    
    except psycopg2.Error as error:
        # Rollback the transaction in case of an error
        connector.rollback()
        cursor.close()
        print("Error creating table:", error)

def user_login(request):
    cursor = connector.cursor()
    body = json.loads(request.body)
    # print(body['username'])
    select_query = """
        SELECT * FROM users
        WHERE username = %s
    """
    cursor.execute(select_query, (html.escape(body['username']),))
    rows = cursor.fetchall()
    # print(rows)
    # print(len(rows))
    if len(rows) == 0:
        return HttpResponse("Invalid username, this username is not in server.")
    
    id = rows[0][0]
    hashed_password = rows[0][2]
    auth_token = rows[0][3]
    salt = rows[0][5]

    if hashed_password != hashlib.sha256(html.escape((body["password"]) + salt).encode('utf-8')).hexdigest():
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
    
def postChat(user, message):
    cursor = connector.cursor()
    insert_query = """
            INSERT INTO chat (username, content)
            VALUES (%s, %s)
    """

    cursor.execute(insert_query, (user, html.escape(message)))
    connector.commit()
    cursor.close()

@transaction.atomic
def getChat(request):
    cursor = connector.cursor()
    if 'id' in request.GET:
        select_query = """
            SELECT * FROM posts
            WHERE id = %s
        """
        cursor.execute(select_query, (html.escape(request.GET['id']),))
        row = cursor.fetchone()
        res_json = {'username': row[1],'content': row[2], 'file': row[3]}
        cursor.close()
        return JsonResponse(res_json, status=200)
    else:
        select_query = """
            SELECT * FROM chat
        """
        cursor.execute(select_query)
        rows = cursor.fetchall()
        res_json_list = []
        for row in rows:
            res_json = {'id':row[0],'username': row[1],'content': row[2]}
            res_json_list.append(res_json)
        cursor.close()
        return JsonResponse(res_json_list, safe=False, status=200)


def createPOST(request):
    cursor = connector.cursor()
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
        filename = ""
        username = rows[0][1]
        uploaded_file = None
        try:
            uploaded_file = request.FILES['file']
            file_content = uploaded_file.read()
            filename = html.escape(uploaded_file.name)
            filename = str(uuid.uuid4()) + '_' + filename
            while os.path.exists(os.path.join(settings.MEDIA_ROOT, filename)):
                filename = str(uuid.uuid4()) + '_' + uploaded_file.name

            with open(os.path.join(settings.MEDIA_ROOT, filename), "wb") as destination:
                destination.write(file_content)
            uploaded_file.close()
        except Exception as error:
            print(error)


        insert_query = """
            INSERT INTO posts (username, content, file, liked)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(insert_query, (username, html.escape(request.POST.get('content')), filename, []))
        connector.commit()

        get_last_query = """SELECT * FROM posts ORDER BY id DESC LIMIT 1;"""
        cursor.execute(get_last_query)
        connector.commit()

        inserted_id = cursor.fetchone()[0]
        if uploaded_file != None and len(uploaded_file.name) != 0:
            response_jsonB = {'id':inserted_id, 'username':username, 'content':html.escape(request.POST.get('content')), "file": filename}
        else:
            response_jsonB = {'id':inserted_id, 'username':username, 'content':html.escape(request.POST.get('content'))}
        print(response_jsonB)
        response = JsonResponse(response_jsonB)
        cursor.close()
        return response # Need add a auth_token cookie to HttpResponse

def getPOST(request):
    cursor = connector.cursor()
    # some parameter
    if 'id' in request.GET:
        select_query = """
            SELECT * FROM posts
            WHERE id = %s
        """
        cursor.execute(select_query, (html.escape(request.GET['id']),))
        row = cursor.fetchone()
        res_json = {'username': row[1],'content': row[2], 'file': row[3]}
        cursor.close()
        return JsonResponse(res_json, status=200)
    else:
        select_query = """
            SELECT * FROM posts
        """
        cursor.execute(select_query)
        rows = cursor.fetchall()
        res_json_list = []
        for row in rows:
            res_json = {'id':row[0],'username': row[1],'content': row[2], 'file': row[3]}
            res_json_list.append(res_json)
        cursor.close()
        return JsonResponse(res_json_list, safe=False, status=200)
    
    
def checkLike(request):
    cursor = connector.cursor()
    if 'Cookie' in request.headers:
        auth_token = request.COOKIES.get('auth_token')
        if not auth_token:
            cursor.close()
            return HttpResponse("User not found",status = 404)
        hashed_token = str(hashlib.sha256((auth_token).encode('utf-8')).hexdigest())
        select_query = """
            SELECT * FROM users
            WHERE auth_token = %s
        """
        # print(cursor)
        cursor.execute(select_query, (hashed_token,))
        rows = cursor.fetchall()
        print(rows)
        user_id = rows[0][0]
        if 'id' in request.GET:
            select_query = """
                SELECT * FROM posts
                WHERE id = %s
            """
            cursor.execute(select_query, (html.escape(request.GET['id']),))
            row = cursor.fetchone()
            likes = row[4]
            if str(user_id) in likes:
                res_json = {"liked": True}
                connector.commit()
                return JsonResponse(res_json, safe=False, status=200)
    res_json = {"liked": False}
    connector.commit()
    cursor.close()
    return JsonResponse(res_json, safe=False, status=200)

# #body write like data into post
def like(request):
    cursor = connector.cursor()
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
        user_id = rows[0][0]

        body = json.loads(request.body)

        if 'id' in body:
            select_query = """
                SELECT * FROM posts
                WHERE id = %s
            """
            cursor.execute(select_query, (body['id'],))
            row = cursor.fetchone()
            likes = row[4]
            if str(user_id) in likes:
                likes.remove(str(user_id))
            else:
                likes.append(str(user_id))
            update_query = """ UPDATE posts
            SET liked = %s
            WHERE id = %s"""

            cursor.execute(update_query, (likes, body['id']))
            response = HttpResponse("like updated")
            connector.commit()
            return response 
        
    response = HttpResponse("Not found")
    connector.commit()
    cursor.close()
    return response 
# cursor.close()
# connector.close()
