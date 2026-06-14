################################################
# Backend source code for team: The Cullinan   #
# Project Name: Memora                         #
# By, Rahul. Pagare (Back-end Dev.)            #
################################################

'''
if authenticate => Checks for access.
else => Doesn't check access.
'''


'''
Memora Running Variables
'''

authenticate = True

# Non-flask modules
import string
import pickle
import random
import os
import datetime
import hashlib
import sqlite3
import shutil

# Flask modules
from flask import jsonify
from flask import Flask
from flask import (
    Flask,
    make_response,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

from flask_cors import CORS, cross_origin
#from flask_httpauth import HTTPBasicAuth
#from flask_wtf import CSRFProtect # Server side requests are NOT CSRF protected. How would we give the csrf token each time to the react app?
from api import api 


app = Flask(__name__)
CORS(app)
app.secret_key = "%YTHT34%^$#@The-Cullinan##M$eRmTo%r@a%F$$#WTRv!"
app.register_blueprint(api, url_prefix='/api/')

#csrf = CSRFProtect(app)


try:
    if os.environ['USER'] == "RahulP":
        working_dir = "/home/RahulP/The Cullinan"
    elif os.environ['USER'] == "rahul":
        working_dir = "."
except:
    print('[-] Cannot work with non-linux based systems @app.py.')
    working_dir = "."
    #exit(1)
    print('[+] Bypassed. @api.py')
    

def gen_reg_id():
    return "".join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase)
        for k in range(random.randint(12, 20))) + "".join(
            random.choice(string.digits)
            for x in range(random.randint(30, 60)))



class AllowedUsers:
    def __init__(self):
        self.users = {} # NOTE: format = {id: {username, ban_status}}
        self.version = "map1"

    def register_user(self, reg_id: str, username: str) -> bool:
        self.username = username.strip() # No triailing spaces; beware!
        safe = True
        val_only = []
        for key in self.users:
            val_only.append(self.users[key]['username'])
        if self.username in val_only:
            safe = False

        #if nickname not in self.users.keys():

        if safe:
            self.users[reg_id] = {'username': self.username, 'ban_status': False}
            return True
        else:
            return False

    def remove_user(self, reg_id):
        if reg_id not in self.users.keys():
            return False
        else:
            self.users = self.users.pop(reg_id)
            return True

    def ban_user(self, reg_id):
        if reg_id not in self.users.keys():
            return False
        else:
            self.users[reg_id]['ban_status'] = True
            return True

    def unban_user(self, reg_id):
        if reg_id not in self.users.keys():
            return False
        else:
            self.users[reg_id]['ban_status'] = False
            return True


if not os.path.exists(f'{working_dir}/RegisteredUsers.db'):
    lll = AllowedUsers()
    lll.register_user(gen_reg_id(), 'RahulPagare20')
    lll.register_user(gen_reg_id(), 'Aakira14')
    lll.register_user(gen_reg_id(), 'Kanakk020')
    with open(f'{working_dir}/RegisteredUsers.db', 'wb') as tp:
        pickle.dump(lll, tp)


@app.errorhandler(404)
def page_not_found(err):
    return "<H1>That page wasn't found on our servers.</H1><a href='/'>Click here to go to the home page.</a>"




@app.before_request
def before_req_check():
    global authenticate
    allowed_paths = [
        "/inner/server/login", '/images/the_cullinan_pfp_white.jpg', '/images/the_cullinan_pfp.jpg', '/images/the_cullinan_pfp_black.png', '/inner/stylesheet/style_index.html.css',
        '/api/create_account_st1', '/api/create_account_st2', '/api/check_authentication', '/api/login', '/api/add_profile_image'
        ]#, '/inner/stylesheet/style_index.html.css']

    if authenticate:
        if request.path not in allowed_paths:
            allow = False
            cookies = request.cookies
            if 'Registration' in cookies:
                reg_id = cookies.get('Registration')
            else:
                return render_template('login_ssr.html', error_message="Authentication Mandated.")

            with open(f'{working_dir}/RegisteredUsers.db', 'rb') as tp:
                raw = pickle.load(tp)

            if reg_id in raw.users.keys():
                if raw.users[reg_id]['ban_status']:
                    return '<h1>[!] Account banned!</h1>'
                else:
                    allow = True
            else:
                return render_template('login_ssr.html', error_message="Invalid Cookie")

            if not allow:
                if authenticate:
                    return render_template('login_ssr.html', error_message="Authentication Mandated.")
                else:
                    allow = True
            else:
                pass




@app.route('/inner/server/login', methods=["POST"])
def login_page_server():
    #allowed_usernames = ['RahulPagare20', 'Aakira14', 'Kanak']
    username_raw = request.form['username']
    password_raw = request.form['password']
    username = str(username_raw.strip())
    password = str(password_raw.strip())
    if str(hashlib.md5(password.encode('utf-8')).hexdigest()) != "bba650365acda735619a9ea907cc7285":
        return render_template('login_ssr.html', error_message="Invalid password.")
    else:
        with open(f'{working_dir}/RegisteredUsers.db', 'rb') as tp:
            raw = pickle.load(tp)
        present = False
        user_reg_id = "[!]"
        for key in raw.users.keys():
            if raw.users[key]['username'] == username:
                present = True
                user_reg_id = key
                break

        #if username not in raw.users.keys():
        if not present:
            return render_template('login_ssr.html', error_message="Invalid username.")
        else:
            #resp = make_response(render_template('index.html'))
            resp = make_response(render_template('redirect_to.html', url_='/'))
            resp.set_cookie('Registration', user_reg_id, expires=datetime.datetime.now() +datetime.timedelta(days=30))
            return resp



@app.route('/')
def hello_world():
    #Registration
    cookies = request.cookies
    username = "ADMIN"


    if str(cookies['Registration']) == "ELgLXMLNaCoKy7645586300090355500179894643862957384206":
        username = "Rahul Pagare"
    elif str(cookies['Registration']) == "CYugiwfkspJkkGC80791262675970651296362946670957009848962482":
        username = "Aakira Khot"
    elif str(cookies['Registration']) == "BrmdVkFsRgnArQWbb667298677443133714564152727123853573296743612147061764":
        username = "Kanak Saini"
    else:
        return f"Invalid cookie configuration, Registration: `{cookies['Registration']}`"


    return render_template('home.html', username=username)



def check_users():
    con = sqlite3.connect(f'{working_dir}/database/dementia_users.db',  check_same_thread=False, isolation_level=None);
    cur = con.cursor()    
    cur.execute('SELECT * FROM patient')
    db =  cur.fetchall()
    return db



@app.route('/admin')
def admin():
    cookies = request.cookies

    total_users = check_users()
    total_users = len(total_users)

    with open(f'{working_dir}/database/pickled/st1_cleared.db', 'rb') as file:
        db = pickle.load(file)    

    return render_template('admin.html', active_sessions=[], total_users=total_users, regr=cookies['Registration'],  tot_st1_cleared_users=len(db.users))


@app.route('/admin/stage1_cleared')
def stage1_cleared():
    cookies = request.cookies
    with open(f'{working_dir}/database/pickled/st1_cleared.db', 'rb') as file:
        db = pickle.load(file)
    users_db = []
    for i in db.users:
        regr = i['user_id']
        email_id = i['email_id']
        password = i['password']
        users_db.append({"email_id": email_id,  "regr": regr, "password": password})    
    
    return render_template('stage1_cleared.html', users_db=users_db, nof=len(users_db))

@app.route('/admin/remove_st1', methods=['POST'])
def remove_stage1_cleared_users():
    cookies = request.cookies
    id = request.form['id']
    with open(f'{working_dir}/database/pickled/st1_cleared.db', 'rb') as file:
        db = pickle.load(file)
    users_db = []
    for i in db.users:
        id_temp = i['user_id']
        if id == id_temp:
            db.users.remove(i)
    
    with open(f'{working_dir}/database/pickled/st1_cleared.db', 'wb') as file:
        pickle.dump(db, file)
    
    resp = make_response(render_template('redirect_to.html', url_='/admin/stage1_cleared'))
    return resp
 



@app.route('/admin/accounts')
def admin_accounts():
    cookies = request.cookies
    with open(f'{working_dir}/RegisteredUsers.db', 'rb') as file:
        db = pickle.load(file)
    users_db = []
    for i in db.users:
        regr = i
        temp = db.users[i]
        username = temp['username'] + " [ADMIN]"
        ban_status = temp['ban_status']
        users_db.append({"username": username,  "regr": regr, "ban_status": ban_status})
    

    db = check_users()
    for user in db:
        regr = user[0]
        username = user[1]
        email_id = user[2]
        password = user[3]
        phone_number = user[4]
        dementia_stage = user[5]
        caretaker_phone_number = user[6]
        ban_status = 'undefined'
        print(username)
        with open(f'{working_dir}/database/{regr}/ban_status.db', 'rb') as file:
            raw_ban_status = pickle.load(file)
            ban_status = raw_ban_status.banned
        users_db.append({
            "username": username,  
            "regr": regr,
            'email_id': email_id,
            'password': password,
            'phone_number': phone_number,
            'dementia_stage': dementia_stage,
            'caretaker_phone_number': caretaker_phone_number,
            "ban_status": ban_status})
    
    
    with open(f'{working_dir}/database/pickled/st1_cleared.db', 'rb') as file:
        db = pickle.load(file)
    

        

    return render_template('admin_accounts.html', users_db=users_db, tot_nof_users=len(users_db))



def delete_account_with_hash(params):
    try:
        con = sqlite3.connect(f'{working_dir}/database/dementia_users.db',  check_same_thread=False, isolation_level=None);
        cur = con.cursor()         
        cur.execute('DELETE FROM patient WHERE id=?', (params, ))
        con.commit()
        return f'Deleted account with hash `{params}` successfully.'
    except Exception as err:
        print(f'func delete_accout_with_hash err: {str(err)}')
        return False


@app.route('/admin/terminate_account', methods=['POST'])
def delete_account():
    id_raw = request.form['id']

    stat = delete_account_with_hash(id_raw, )
    shutil.rmtree(f'{working_dir}/database/{id_raw}', ignore_errors=True)
    
    
    resp = make_response(render_template('redirect_to.html', url_='/admin/accounts'))
    return resp
    
@app.route('/admin/ban_account', methods=['POST'])
def ban_account():
    id_raw = request.form['id']
    with open(f'{working_dir}/database/{id_raw}/ban_status.db', 'rb') as file:
        raw_ban_status = pickle.load(file)
        raw_ban_status.banned = True
    with open(f'{working_dir}/database/{id_raw}/ban_status.db', 'wb') as file:
        pickle.dump(raw_ban_status, file)
    
    resp = make_response(render_template('redirect_to.html', url_='/admin/accounts'))
    return resp

@app.route('/admin/unban_account', methods=['POST'])
def unban_account():
    id_raw = request.form['id']
    with open(f'{working_dir}/database/{id_raw}/ban_status.db', 'rb') as file:
        raw_ban_status = pickle.load(file)
        raw_ban_status.banned = False
    with open(f'{working_dir}/database/{id_raw}/ban_status.db', 'wb') as file:
        pickle.dump(raw_ban_status, file)

    resp = make_response(render_template('redirect_to.html', url_='/admin/accounts'))
    return resp


@app.route('/team')
def team_flex():
    return render_template('index.html')


@app.route('/inner/stylesheet/style_index.html.css')
def style_index():
    global cwd, project_dir
    return send_file(
        f'{working_dir}/stylesheets/style_index.html.css')

@app.route('/images/the_cullinan_pfp.jpg')
def cullinan_pr_jpg():
    global cwd, project_dir
    return send_file(
        f'{working_dir}/images/the_cullinan_pfp.jpg')


@app.route('/images/the_cullinan_pfp_white.jpg')
def cullinan_pr_white_jpg():
    global cwd, project_dir
    return send_file(
        f'{working_dir}/images/the_cullinan_pfp_white.jpg')

@app.route('/images/the_cullinan_pfp_black.png')
def cullinan_pr_black_png():
    global cwd, project_dir
    return send_file(
        f'{working_dir}/images/the_cullinan_pfp_black.png')



@app.route('/images/aakira_pfp.png')
def aakira_pfp_png():
    global cwd, project_dir
    return send_file(
        f'{working_dir}/images/aakira_pfp.png')

@app.route('/images/kanak_pfp.png')
def kanak_pfp_png():
    global cwd, project_dir
    return send_file(
        f'{working_dir}/images/kanak_pfp.png')

@app.route('/images/rahul_pfp.png')
def rahul_pfp_png():
    global cwd, project_dir
    return send_file(
        f'{working_dir}/images/rahul_pfp.png')


port = 9999

if __name__ == '__main__':
    print('\n[+] Memora (C), 2026\nMade by Rahul Pagare\n')
    app.run(host="0.0.0.0", port=port)