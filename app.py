################################################
# Backend source code for team: The Cullinan   #
# Project Name: Memora                         #
# By, Rahul. Pagare (Back-end Dev.)            #
################################################

# Non-flask modules
import os

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


@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')



@app.route('/static/style.css')
def style_css():
    return render_template('/static/style.css')

@app.route('/static/script.js')
def script():    
    return render_template('/static/script.js')


port = 8080

if __name__ == "__main__":
    app.run(port=port)