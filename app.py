################################################
# Backend source code for team: The Cullinan   #
# Project Name: Memora                         #
# By, Rahul. Pagare (Back-end Dev.)            #
################################################

# Non-flask modules
import os
import sqlite3
import pickle

# Flask modules
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
from flask_wtf import CSRFProtect

# Customized imports 
from api import api

app = Flask(__name__)
app.secret_key = "&@*)#%Ra%&hul_s46h6@7rin^%k1.0@%s5hr##ink^$#prot&o&&ty(@$p))(*e1$#^&point0!$%$^$"
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.register_blueprint(api, url_prefix='/api/')
csrf = CSRFProtect(app)

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


con = sqlite3.connect(f'{working_dir}/database/dementia_users.db',  check_same_thread=False, isolation_level=None)
cur = con.cursor()

def get_data(params):
    global con, cur
    try:
        cur.execute('SELECT * FROM patient WHERE id=?', (params, ))
        return cur.fetchall()
    except Exception:
        return False


@app.before_request
def check_authentication():
    cookies = request.cookies
    if request.path.strip()[:4] != "/api" and request.path.strip()[0:7] != "/static":
        if 'user_id' in cookies:
            temp = get_data(cookies['user_id'])
            if temp != []:
                checks_l = ['/dashboard', '/dashboard/', '/whos-this', '/whos-this/']
                if request.path.strip() not in checks_l:
                    if  "/inner/server/" not in request.path.strip():
                        resp = make_response(render_template('redirect_to.html', url_=f"/dashboard"))
                        return resp
                
            else:
                with open(f"{working_dir}/database/pickled/st1_cleared.db", "rb") as file:
                    db = pickle.load(file)                    

                matched = False
                for i in db.users:
                    if i['user_id'] == cookies['user_id']:
                        matched = True
                        break
                
                if not matched:
                    checks = ['/', '', '/login', '/login/']
                    if request.path.strip() not in checks:            
                        resp = make_response(render_template('redirect_to.html', url_="/"))
                        print('shitting here')
                        resp.set_cookie('user_id', '', expires=0)
                        return resp
        else:
            checks_l = ['/dashboard', '/dashboard/']
            if request.path.strip() in checks_l:
                    resp = make_response(render_template('redirect_to.html', url_="/"))
                    return resp            
            
@app.route('/')
def index():   
    
    return render_template('landing.html')

@app.route('/register')
def register_page():
    cookies = request.cookies
    if 'user_id' not in cookies:
        return render_template('register.html')
    
    with open(f"{working_dir}/database/pickled/st1_cleared.db", "rb") as file:
        db = pickle.load(file)
    
    temp = get_data(cookies['user_id']) # Important nuance here! First we check if account actually exists then we check if stage 1 is cleared or not, because stage 1 accounts are deleted once stage 2 (personalization) is cleared.
    if temp == []:
        match = False
        for i in db.users:
            if i['user_id'] == cookies['user_id']:
                match = True
                break
        
        if not match:
            return render_template('register.html')        
        else:
            resp = make_response(render_template('redirect_to.html', url_=f"/personalize"))
            return resp
        #return render_template('register.html')
    
    else:
        # redirect_to dashboard
        resp = make_response(render_template('redirect_to.html', url_=f"/dashboard"))
        return resp




@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/personalize')
def personalize():
    cookies = request.cookies
    if 'user_id' not in cookies:
        resp = make_response(render_template('redirect_to.html', url_=f"/register"))
        return resp
    
    with open(f"{working_dir}/database/pickled/st1_cleared.db", "rb") as file:
        db = pickle.load(file)
    
    for i in db.users:
        if i['user_id'] == cookies['user_id']:
            return render_template('personalize.html', user_id=i['user_id'])
    
    resp = make_response(render_template('redirect_to.html', url_="/"))
    resp.set_cookie('user_id', '', expires=0)

    return resp

@app.route('/dashboard')
def dashboard_ssr():
    global working_dir
    cookies = request.cookies
    user_id = cookies['user_id']
    error = None

    # Checking family members
    try:
        all_ids = os.listdir(f'{working_dir}/database/{user_id}/Family Members')
        #all_ids.remove('ban_status.db')
    except:
        all_ids = []
        #os.mkdir(f'{working_dir}/database/{user_id}/Family Members')
        #error = "Error retrieving family members."


    family_members = []
    for id in all_ids:
        with open(f'{working_dir}/database/{user_id}/Family Members/{id}/family_member.db', 'rb') as file:
            db = pickle.load(file)
        
        if db.member_relation == "other":
            relation_temp = db.member_other_relation
        else:
            relation_temp = db.member_relation
    

        family_members.append({
            'member_pfp': f'/inner/server/get-profile-pic/{id}',
        'member_name': db.member_name,
        'member_relation': relation_temp,
        })
        if db.member_notes != "":
            family_members[-1]['member_notes'] = db.member_notes
        if db.member_birthdate != "":
            family_members[-1]['member_birthdate'] = db.member_birthdate
        

    #return family_members
    #photo_pfp = f'{working_dir}/database/{user_id}/{id}/{db[0]}'

    # Memories
    memories = []
    if os.path.exists(f'{working_dir}/database/{user_id}/Memories'):
        all_ids = os.listdir(f'{working_dir}/database/{user_id}/Memories')
        posn = 'left' # While starting out, initially

        for id in all_ids:
            with open(f'{working_dir}/database/{user_id}/Memories/{id}/memories.db', 'rb') as file:
                db = pickle.load(file)
            memories.append({
                'title': db.title,
                'description': db.description,
                'date': db.date,
                'category': db.category,
                'posn': posn
            })
            if posn == 'left':
                posn = 'right'
            elif posn == 'right':
                posn = 'left'

    if not error:
        return render_template('dashboard.html', family_members=family_members, memories=memories)
    else:
        return render_template('dashboard.html', family_members=[], memories=[])

@app.route('/inner/server/get-profile-pic/<id>')
def get_profile_pic_user(id):
    cookies = request.cookies
    user_id = cookies['user_id']
    if os.path.exists(f'{working_dir}/database/{user_id}/Family Members/{id}'):
        try:
            db = os.listdir(f'{working_dir}/database/{user_id}/Family Members/{id}')
            db.remove('family_member.db')
            return send_file(f'{working_dir}/database/{user_id}/Family Members/{id}/{db[0]}')
        except Exception as err:
            return f"Mission failed: Photo of family member with given id: {id} cannot be retrieved. Error: {str(err)}"
    else:
        return f"Mission failed: Family member with given id: {id} wasn't found.s"

@app.route('/whos-this')
def whos_this_ssr():
    return render_template('whos-this.html')

port = 8080

if __name__ == "__main__":
    app.run(port=port)