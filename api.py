from flask import Blueprint, render_template, request, make_response
from flask import jsonify, send_file
import sqlite3
import os
import random
import string
import datetime
import pickle

from send_email import send_email
from classes import *

first_launch = True

api = Blueprint('api', __name__, template_folder='templates')
try:
    if os.environ['USER'] == "RahulP":
        working_dir = "/home/RahulP/The Cullinan"
    elif os.environ['USER'] == "rahul":
        working_dir = "."
except:
    print('[-] Cannot work with non-linux based systems  @api.py')
    working_dir = "."
    #exit(1)
    print('[+] Bypassed. @api.py')


if not os.path.exists(f"{working_dir}/database/pickled/st1_cleared.db"):
    with open(f"{working_dir}/database/pickled/st1_cleared.db", "wb") as file:
        st1_brand_new = st1_cleared()
        pickle.dump(st1_brand_new, file)

con = sqlite3.connect(f'{working_dir}/database/dementia_users.db',  check_same_thread=False, isolation_level=None)
cur = con.cursor()

if os.path.exists(f"{working_dir}/database/dementia_users.db"):
    try:
        con = sqlite3.connect(f'{working_dir}/database/dementia_users.db',  check_same_thread=False, isolation_level=None)
        cur = con.cursor()
        if first_launch:
            cur.execute('CREATE TABLE patient (id text, name text, email_id text, password text, phone_number text, dementia_stage text, caretaker_phone_number text)')
            con.commit()  
    except Exception as error:
        print(f'[-] Cannot create table in {working_dir}/database/dementia_users.db')
        print(f'[-] Error: {error}')


def create_profiles_for_user(id: str):
    
    try:
        con = sqlite3.connect(f'{working_dir}/database/{id}/profiles.db',  check_same_thread=False, isolation_level=None)
        cur = con.cursor()
        if first_launch:
            cur.execute('CREATE TABLE connection (id text, name text, top_three_memories text, audio_clip_status text')
            con.commit()  
        return True
    except:
        print(f'[-] Cannot connect to the {working_dir}/database/{id}/profiles.db')
        return False



def get_id():
    return "".join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase +
                      string.digits) for l in range(random.randint(50, 80)))


def create_user(id, name, email_id, password, phone_number, dementia_stage, caretaker_phone_number):
    try:
        con = sqlite3.connect(f'{working_dir}/database/dementia_users.db', check_same_thread=False, isolation_level=None)
        cur = con.cursor()
        cur.execute('INSERT INTO patient VALUES (?, ?, ?, ?, ?, ?, ?)', (id, name, email_id, password, phone_number, dementia_stage, caretaker_phone_number))
        con.commit()
        return True
    except Exception as error:
        print(f'[-] func create_user error: {error}')
        return False



def get_data(params):
    global con, cur
    try:
        cur.execute('SELECT * FROM patient WHERE id=?', (params, ))
        return cur.fetchall()
    except Exception:
        return False


def get_data_from_password(params):
    global con, cur
    try:
        cur.execute('SELECT * FROM patient WHERE password=?', (params, ))
        return cur.fetchall()
    except Exception:
        return False


# Web routes and views

@api.route('/create_account_st1', methods=['POST'])
def create_account_st1():
    id = get_id()
    extraneous = False
    #brand_new = request.get_json()
    brand_new = request.form

    password_usr = brand_new['password'].strip()
    email_id_usr = brand_new['email_id'].strip()

    db = get_data_from_password(password_usr, )
    for user in db:
        if user[2] == email_id_usr:
            #return jsonify({'status': 'Failed', "justification": "Another user with the given credentials already exist."})
            return render_template('register.html', error="Another user with the given credentials already exist.")


    if "email_id" not in brand_new.keys():
        #return jsonify({'status': 'Failed', "justification": "Email ID was not provided."})
        return render_template('register.html', error="Email ID was not provided.")
    
    if "password" not in brand_new.keys():
        #return jsonify({'status': 'Failed', "justification": "Password was not provided."})
        return render_template('register.html', error="Password was not provided.")
    
    if len(list(brand_new.keys())) > 2:
        extraneous = True
    
    with open(f"{working_dir}/database/pickled/st1_cleared.db", "rb") as file:
        db = pickle.load(file)
        db.add_waiting_user(id, email_id_usr, password_usr)
        '''
        db.users.append({
            'user_id': id,
            'email_id': email_id_usr,
            'password': password_usr
        })
        '''

    with open(f"{working_dir}/database/pickled/st1_cleared.db", "wb") as file:
        pickle.dump(db, file)
    

    stat = False
    #stat = send_email(email_id_usr, "Memora", f"Account has been successfully created! Your user id is: {id}")
    print('[!] Email is not being sent.')

    #return jsonify({"status": "Account successfully created! (Stage 1)", "user_id": id, "extraneous_complexity": extraneous, 'email_stat': stat})
    #return "ACCOUNT SUCCESFULLY CREATED! Awaiting Aakira's /templates/dashboard.html"
    resp = make_response(render_template('redirect_to.html', url_=f"/personalize"))
    resp.set_cookie('user_id', id, expires=datetime.datetime.now() + datetime.timedelta(days=30))
    print('setting cookie user_id as', str(id))
    return resp
    #return render_template('personalize.html')




@api.route('/create_account_st2', methods=['POST'])
def create_account_st2():
    # Note, if caretaker does not exist, caretaker_phone_number = "DNE"
    # Bifurcation of code just so that i know where things went wrong, if at they go wrong, which I hope, they don't :)


    cookies = request.cookies
    if 'user_id' not in cookies:
        resp = make_response(render_template('redirect_to.html', url_=f"/register"))
        return resp
    
    with open(f"{working_dir}/database/pickled/st1_cleared.db", "rb") as file:
        db = pickle.load(file)
    
    match = False
    for i in db.users:
        if i['user_id'] == cookies['user_id']:
            match = True
            break
    
    if not match:
        resp = make_response(render_template('redirect_to.html', url_="/"))
        resp.set_cookie('user_id', '', expires=0)

        return resp    

    # STAGE 1 Verification for /api/create_account_st2

    core =  request.form
    if 'user_id' not in core.keys():
        #return jsonify({'status': 'Failed', "justification": "`User ID` was not given."})
        return render_template('personalize.html', error="`User ID` was not given.")
    
    if 'full_name' not in core.keys():
        #return jsonify({'status': 'Failed', "justification": "`Name` was not given."})
        return render_template('personalize.html', error=f"`Name` was not given. {str(core)}")

    if 'phone_number' not in core.keys():
        return render_template('personalize.html', error="`Phone Number` was not given.")

    if 'dementia_stage' not in core.keys():
        return render_template('personalize.html', error="`Dementia Stage` was not given.")

    if 'caretaker_phone_number' not in core.keys():
        return render_template('personalize.html', error="`Caretaker's Phone Number` was not given.")
    

    # STAGE 2 Verification for /api/create_account_st2
    
    id = core['user_id']
    name = core['full_name']
    phone_number = core['phone_number']
    dementia_stage = core['dementia_stage']
    caretaker_phone_number = core['caretaker_phone_number']

    with open(f"{working_dir}/database/pickled/st1_cleared.db", "rb") as file:
        db = pickle.load(file)
        record = db.search_record_by_id(id)
        if not record:
            #return jsonify({'status': 'Failed', "justification": "/api/create_account_st2: Error in STAGE 2 (search_record_by_id)."})
            return render_template('personalize.html', error="/api/create_account_st2: Error in STAGE 2 (search_record_by_id).")                
        email_id = record['email_id']
        password = record['password']
        stat1 = db.delete_waiting_user_by_id(id)
    
    if not stat1:
        #return jsonify({'status': 'Failed', "justification": "/api/create_account_st2: Error in STAGE 2."})
        return render_template('personalize.html', error="/api/create_account_st2: Error in STAGE 2.")

    with open(f"{working_dir}/database/pickled/st1_cleared.db", "wb") as file:
        pickle.dump(db, file)

    os.mkdir(f'{working_dir}/database/{id}')
    with open(f'{working_dir}/database/{id}/ban_status.db', 'wb') as file:
        new_instance = Banned()
        pickle.dump(new_instance, file)
    
    # STAGE 3 Verification for /api/create_account_st2 

    stat2 = create_user(id, name, email_id, password, phone_number, dementia_stage, caretaker_phone_number)



    if not stat2:
        #return jsonify({'status': 'Failed', "justification": "/api/create_account_st2: Error in STAGE 3."})
        return render_template('personalize.html', error="/api/create_account_st2: Error in STAGE 3.")


    #return jsonify({"status": "Account successfully created & initiated! (Stage 2)", "user_id": id})
    resp = make_response(render_template('redirect_to.html', url_=f"/dashboard"))
    return resp


@api.route('/add_family_member', methods=['POST'])
def add_family_member_server():
    cookies = request.cookies
    id = cookies['user_id']
    profile_id = get_id()
    file = request.files['member_photo']
    if file.filename == '':
        resp = make_response(render_template('redirect_to.html', url_=f"/dashboard"))
        return resp

    db = request.form
    member_name = db['member_name'].strip()
    member_relation = db['member_relation'].strip()
    member_other_relation = db['member_other_relation'].strip()
    member_notes = db['member_notes'].strip()
    member_birthdate = db['member_birthdate'].strip()

    #return str(db['member_name'].strip())



    ext = file.filename.rsplit('.', 1)[1].lower()

    if file.filename.strip() != '':
        os.mkdir(f'{working_dir}/database/{id}/{profile_id}')
        file.save(f'{working_dir}/database/{id}/{profile_id}/photo.{ext}')
        temp = FamilyMember()
        temp.member_name = member_name
        temp.member_relation = member_relation
        temp.member_other_relation = member_other_relation
        temp.member_notes = member_notes
        temp.member_birthdate = member_birthdate
        temp.edited = True

        with open(f'{working_dir}/database/{id}/{profile_id}/family_member.db', 'wb') as file:
            pickle.dump(temp, file)
    else:
        return make_response(render_template('redirect_to.html', url_=f"/dashboard", error="Invalid file name."))

    return make_response(render_template('redirect_to.html', url_=f"/dashboard"))
    
    #resp = make_response(render_template('redirect_to.html', url_=f"/dashboard"))
    #return resp



@api.route('/check_authentication', methods=['POST'])
def check_authentication_lll():
    #data = request.get_json()
    data = request.form

    if 'user_id' not in data.keys():
        return jsonify({'status': 'Failed', "justification": "`User ID` was not given."})
    
    id = data['user_id']
    stat = get_data(id, )
    if not stat:
        return jsonify({'status': 'Failed', "justification": "User with given id does not exist in our servers."})
    
    return jsonify({'status': 'Success', "justification": "User authenticated successfully."})


@api.route('/login', methods=['POST'])
def login_server():
    #data = request.get_json()
    data = request.form

    if 'email_id' not in data.keys():
        #return jsonify({'status': 'Failed', "justification": "`Email ID` was not given."})
        return render_template('login.html', error="`Email ID` was not given.")

    if 'password' not in data.keys():
        #return jsonify({'status': 'Failed', "justification": "`password` was not given."})
        return render_template('login.html', error="`password` was not given.")
    
    email_id = data['email_id'].strip()
    password = data['password'].strip()

    data = get_data_from_password(password)
    if len(data) > 0:
        data = data[0]
    else:
        #return jsonify({'status': 'Failed', "justification": "Invalid Credentials."})
        return render_template('login.html', error="Invalid Credentials.")

    if not data:
        #return jsonify({'status': 'Failed', "justification": "Invalid Credentials."})
        return render_template('login.html', error="Invalid Credentials.")
    
    if data == []:
        #return jsonify({'status': 'Failed', "justification": "Invalid Credentials."})
        return render_template('login.html', error="Invalid Credentials.")
    
    email_id_real = data[2]
    if email_id == email_id_real:
        #return jsonify({'status': 'Success', "justification": "Welcome back to your account!", "user_id": data[0]})
        resp = make_response(render_template('redirect_to.html', url_=f"/dashboard"))
        resp.set_cookie('user_id', data[0], expires=datetime.datetime.now() + datetime.timedelta(days=30))        

        return resp

    
    return jsonify({'status': 'Failed', "justification": "Invalid Credentials."})
    


@api.route('/add_profile_image', methods=['POST'])
def add_profile_pic():
    if 'image' not in request.files:
        return jsonify({"status": "Failed", "justification": "No image recevied."})
    
    file = request.files['image']

    if file.filename == '':
        return jsonify({"status": "Failed", "justification": "No image recevied."})

    if file:
        filepath = f"{working_dir}/{file.filename}"
        file.save(filepath) 
    
    print(f'SAVED!! {filepath}')

    return jsonify({'status': "Success"})