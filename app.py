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



@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

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

    

port = 8080

if __name__ == "__main__":
    app.run(port=port)