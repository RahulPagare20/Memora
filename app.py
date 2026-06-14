################################################
# Backend source code for team: The Cullinan   #
# Project Name: Memora                         #
# By, Rahul. Pagare (Back-end Dev.)            #
################################################

# Non-flask modules
import os
import sqlite3
import pickle
import time
import shutil

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
from flask_socketio import SocketIO, emit

'''
import eventlet
eventlet.monkey_patch()

from gevent import monkey;
monkey.patch_all()
'''

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
                checks_l = ['/dashboard', '/dashboard/', '/whos-this', '/whos-this/', '/delete_account', '/delete_account/']
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

'''
def delete_acc(params):
    global con, cur
    try:
        cur.execute('DELETE FROM patient WHERE id=?', (params, ))
        con.commit()
    except Exception as err:
        print(str(err))
        return False
'''
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


@app.route('/delete_account')
def deelte_accout_perm():
    user_id = request.cookies['user_id']

    shutil.rmtree(f'{working_dir}/database/{user_id}', ignore_errors=True)
    stat = delete_account_with_hash(user_id, )
    if stat:
        resp = make_response(render_template('redirect_to.html', url_="/"))
        resp.set_cookie('user_id', '', expires=0)
        return resp
    else:
        personal_info_def = {
            'pfp': '',
            'name': '',
            'email_id': '',
            'password': '',
            'phone_number': '',
            'dementia_stage': '',
            'caretaker_phone_number': ''
        }        
        return render_template('dashboard.html', family_members=[], memories=[], personal_info=personal_info_def, error="db error while deleting your account.")
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

    db = get_data(user_id,)[0]
    name = db[1]
    email_id = db[2]
    password = db[3]
    phone_number = db[4]
    dementia_stage = db[5]
    caretaker_phone_number = db[6]
    if caretaker_phone_number == "DNE":
        caretaker_phone_number = "-"
    
    personal_info = {
        'pfp': '',
        'name': name,
        'email_id': email_id,
        'password': password,
        'phone_number': phone_number,
        'dementia_stage': dementia_stage,
        'caretaker_phone_number': caretaker_phone_number
    }

    if not error:
        return render_template('dashboard.html', family_members=family_members, memories=memories, personal_info=personal_info)
    else:
        personal_info_def = {
            'pfp': '',
            'name': '',
            'email_id': '',
            'password': '',
            'phone_number': '',
            'dementia_stage': '',
            'caretaker_phone_number': ''
        }        
        return render_template('dashboard.html', family_members=[], memories=[], personal_info=personal_info_def)

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
    cookies = request.cookies
    id = cookies['user_id']
    return render_template('whos-this.html', user_id=id)

######################################################################################################
# DANGER ABOVE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# DO NOT CHANGE ANYTHING ABOVE THIS LINE
#
# DANGER ABOVE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
######################################################################################################

#############################
# Image Recognition         #
# (face_recognition library)#
#############################

import base64
import time
import pickle
import os

import cv2
import numpy as np
import face_recognition
from flask_socketio import SocketIO, emit

# ── SocketIO setup ────────────────────────────────────────────────────────────
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# ── Cooldown config ───────────────────────────────────────────────────────────
last_log_time = 0
LOG_COOLDOWN_SECONDS = 3.0

# ── Frame scale factor (1/4 size → ~16× fewer pixels to process) ─────────────
FRAME_SCALE = 0.25


# ─────────────────────────────────────────────────────────────────────────────
# Helper: decode a base64 WebSocket frame → OpenCV BGR image
# ─────────────────────────────────────────────────────────────────────────────
def decode_websocket_frame(data: str):
    try:
        encoded_data = data.split(',')[1] if ',' in data else data
        image_bytes  = base64.b64decode(encoded_data)
        nparr        = np.frombuffer(image_bytes, np.uint8)
        frame        = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return frame
    except Exception as e:
        print(f"[decode_websocket_frame] Error: {e}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Helper: load known-face encodings for every family member of a given user.
#
# Directory layout expected (matches your existing code):
#   database/{user_id}/Family Members/{member_id}/family_member.db   ← pickle
#   database/{user_id}/Family Members/{member_id}/<photo file>       ← image
#
# Returns:
#   known_encodings : list[np.ndarray]   – 128-d face encoding per member
#   known_metadata  : list[dict]         – {"id": member_id, "name": str}
# ─────────────────────────────────────────────────────────────────────────────
def load_known_faces(user_id: str):
    known_encodings: list = []
    known_metadata:  list = []

    family_dir = os.path.join(working_dir, "database", user_id, "Family Members")
    if not os.path.exists(family_dir):
        print(f"[load_known_faces] No family directory found for user {user_id}")
        return known_encodings, known_metadata

    for member_id in os.listdir(family_dir):
        member_dir = os.path.join(family_dir, member_id)
        db_path    = os.path.join(member_dir, "family_member.db")

        # ── Load the member's name from the pickle ────────────────────────
        try:
            with open(db_path, "rb") as f:
                db = pickle.load(f)
            member_name = db.member_name
        except Exception as e:
            print(f"[load_known_faces] Could not read {db_path}: {e}")
            continue

        # ── Find the photo file (everything that isn't the pickle) ────────
        try:
            files      = os.listdir(member_dir)
            photo_files = [
                fn for fn in files
                if fn != "family_member.db"
                and fn.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".webp"))
            ]
            if not photo_files:
                #print(f"[load_known_faces] No photo for member {member_id} – skipping")
                continue
            photo_path = os.path.join(member_dir, photo_files[0])
        except Exception as e:
            #print(f"[load_known_faces] Error listing {member_dir}: {e}")
            continue

        # ── Generate face encoding ────────────────────────────────────────
        try:
            img       = face_recognition.load_image_file(photo_path)   # RGB
            encodings = face_recognition.face_encodings(img)
            if not encodings:
                #print(f"[load_known_faces] No face found in photo for {member_name} – skipping")
                continue
            known_encodings.append(encodings[0])
            known_metadata.append({"id": member_id, "name": member_name})
            with open(f'{os.getcwd()}/database/{user_id}/Family Members/{member_id}/family_member.db', 'rb') as file:
                db_raw = pickle.load(file)
            relative_name = db_raw.member_name 
            #print(db_path)
            #print(f"[load_known_faces] Loaded encoding for - ({relative_name})")
        except Exception as e:
            pass
            #print(f"[load_known_faces] Encoding error for {member_id}: {e}")

    #print(f"[load_known_faces] Total known faces loaded: {len(known_encodings)}")
    return known_encodings, known_metadata


# ─────────────────────────────────────────────────────────────────────────────
# SocketIO event: 'image'
#
# Expected payload  – base64 frame string (same as before).
# The client should also pass the user_id so we know whose family to load.
# Two options:
#   A) Read it from the SocketIO auth / query-string (cleanest).
#   B) Accept it as part of the data dict: {"frame": "...", "user_id": "..."}.
#
# We use option B here to stay consistent with your existing cookie approach
# without requiring session middleware changes.  If you prefer cookies, swap
# the user_id extraction line for:
#   user_id = request.cookies.get('user_id')
# ─────────────────────────────────────────────────────────────────────────────
@socketio.on('image')
def handle_image(data):
    global last_log_time

    # --- ADD THIS TEMPORARILY ---
    #print(f"[DEBUG] data type: {type(data)}, keys: {data.keys() if isinstance(data, dict) else 'raw string'}")
    # ----------------------------

    # ── 1. Unpack the payload ─────────────────────────────────────────────
    if isinstance(data, dict):
        raw_frame = data.get("frame", "")
        user_id   = data.get("user_id", "")
    else:
        # Backwards-compat: plain base64 string (user_id from query string)
        raw_frame = data
        user_id   = request.args.get("user_id", "")

    if not user_id:
        emit('face_detected', {'status': 'error', 'message': 'user_id missing'},  broadcast=True)
        return

    # ── 2. Decode the incoming frame ──────────────────────────────────────
    frame_bgr = decode_websocket_frame(raw_frame)
    if frame_bgr is None:
        emit('face_detected', {'status': 'error', 'message': 'bad frame'},  broadcast=True)
        return

    # ── 3. Dynamically load this user's known faces ───────────────────────
    #    For production you'd cache these (e.g. in a dict keyed by user_id)
    #    and invalidate when a new family member is added.  Kept simple here.
    known_encodings, known_metadata = load_known_faces(user_id)

    # ── 4. Scale down for speed, convert BGR → RGB (face_recognition needs RGB)
    small_frame = cv2.resize(frame_bgr, (0, 0), fx=FRAME_SCALE, fy=FRAME_SCALE)
    rgb_small   = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # ── 5. Detect + encode faces in the downscaled frame ─────────────────
    face_locations  = face_recognition.face_locations(rgb_small, model="hog")   # "cnn" is more accurate but slower
    face_encodings  = face_recognition.face_encodings(rgb_small, face_locations)

    recognized_faces = []

    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):

        # Scale bounding box back up to original frame coordinates
        scale = int(1 / FRAME_SCALE)
        box = {
            "top":    top    * scale,
            "right":  right  * scale,
            "bottom": bottom * scale,
            "left":   left   * scale,
        }

        if not known_encodings:
            # No family members registered yet – still report the bounding box
            recognized_faces.append({**box, "id": None, "name": "Unknown"})
            continue

        # ── Compare against every known face ──────────────────────────────
        matches      = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.55)
        face_dists   = face_recognition.face_distance(known_encodings, face_encoding)
        best_idx     = int(np.argmin(face_dists))

        if matches[best_idx]:
            meta = known_metadata[best_idx]
            recognized_faces.append({
                **box,
                "id":   meta["id"],
                "name": meta["name"],
            })
        else:
            recognized_faces.append({**box, "id": None, "name": "Unknown"})

    # ── 6. Cooldown gate – only emit & log when the cooldown has elapsed ──
    current_time = time.time()
    if recognized_faces and (current_time - last_log_time > LOG_COOLDOWN_SECONDS):
        last_log_time = current_time

        matched = [f for f in recognized_faces if f["id"] is not None]
        if matched:
            names = ", ".join(f["name"] for f in matched)
            print(f"[ALERT] Recognized: {names}")

        
        
        print(f'Face detected: {str(recognized_faces)}')
        emit('face_detected', {
            'status': 'detected',
            'faces':  recognized_faces,
        },  broadcast=True)
    elif not recognized_faces:
        # Always emit a 'none' so the frontend can clear its overlay
        print(f'Face detected, but no faces recognized')
        emit('face_detected', {'status': 'none', 'faces': []},  broadcast=True)


# ─────────────────────────────────────────────────────────────────────────────
port = 8080

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=port, log_output=True)
    #app.run(host="0.0.0.0", port=port)
