# Memora

> *"When memories fade, relationships shouldn't."*

Memora is an clever web-based AI software tool, and an companion, designed to help Dementia patients (and people suffering from Alzehimer's disease) live a normal life without worrying about their declining memory and its subsequent consequences.

---

## Problem we noticed

Dementia affects over **55 million people worldwide**. These patients have declining memory loss. This results in them forgetting even the basics and essential things, unfortunately, that can include humans as well. They forget their loved ones - their parents, brothers, sisters, cousins, etc. Memora wishes to bridge that gap

- Anxiety and fear in the patient
- Emotional distress for loved ones
- Unsafe situations when caregivers are not recognized
- Social FOMO (Fear of missing out)

Memora addresses this with a calm, non-intrusive, real-time identification experience. Our goal is simple - When memories fade, relationships shouldn't.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, Flask-Socketio |
| Templating | Jinja2 |
| Face Detection | OpenCV (`cv2`) |
| Face Recognition | `face_recognition` (dlib-based) |
| Database | SQLite |
| Image Storage | On hosted server |
| Frontend | HTML5, CSS3, JS |

---

## Project Structure

```
memora/
│
├── app.py                  # Flask application entry point and face recognition system built into it
├── api.py                  # Blueprint for the main flask application
├── classes.py              # Stores all custom data types (classes) for pickle
├── requirements.txt        # Python dependencies
│
├── database/
│   ├── user_id/
│       ├── ban_status.db
│       ├── patient_photo.{ext}
│       ├── Family Members/
|           ├── family_member_id/
│               ├── family_member.db
│               ├── photo.{ext}
│       ├── Memories/
|           ├── memory_id/
│               ├── memories.db
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── animations.css
│   │   ├── script.js
│   │   ├── animations.js
│
└── templates/
    ├── base.html           # Base Jinja layout for landing page
    ├── dashboard.html      # Actual dashboard page for authenticated users
    ├── getstarted.html     # A page which helps users decide whether to create or log into an account
    ├── landing.html        # Landing page    
    ├── login.html          # Login page
    ├── personalize.html    # Create stage 2 account (final account)
    ├── register.html       # Create stage 1 account; Sign-up page 
    ├── whos-this.html      # Identifies the person who is in front of the webcam
```

---

## Installation & Setup

### Prerequisites

- Python (3.9+)
- `cmake` (required by dlib) — install via your OS package manager
- Pip should install all modules in requirements.txt without any error. (dlib wheel causes more issues, so beware)
- A device with a working webcam

#### You can visit [Memora](https://rahulp.pythonanywhere.com) if you want to directly try out the app. But for faster response from websocket.io, try running the flask application on your own local server. (pythonanywhere is kinda slow.)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/memora.git -b main
cd memora
```


### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python3 app.py
```
NOTE: Please do not run flask run -p [port]. This is a socketio app and requires socketio.run(app, *kwargs) to be executed by Python interpreter fand not app.run(*kwargs) (flask version).

Visit `http://localhost:8080` or [Memora](https://rahulp.pythonanywhere.com) in your browser.

---

## Key Features

### Live Recognition Screen (Patient View)
- Full-screen (because it should be free of distraction) interface designed for elderly users
- Matched result displayed as a large, readable card on the top right side (a cyberpunk styled card)
- Unknown face → gentle message: *"Face detected, but not recognised"*

### Save Family Members and Memories
- You can add and delete family members that you love, with their photo and name. Their notes/description and birthdate are optional fields. (Edit feature coming soon!)
- You can add, edit and delete memories that you cherish. Title, description, date and category are compulsory fileds to be provided.

### Upcoming Features
- Memory tests, updated memory timeline, reminders, medicine trackers are some upcoming features, stay tuned!

---

## app.py and api.py (blueprint) Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Landing screen if user is logged in, if not, redirects to /dashboard |
| `GET` | `/register` |  Stage 1 account creation page. Sends an email too! |
| `GET` | `/personalize` | Stage 2 account (final) createion page |
| `GET` | `/login` | Displays Login page |
| `GET` | `/whos-this` | Identifies who the person in front of the webcam is |
| `GET` | `/delete_account` | Deletes given account with user_id stored in cookie |
| `GET` | `/inner/server/get-profile-pic/<id>` | Gives profile picture of family member with given id |
| `GET` | `/api/delete_memory/<id>` | Deletes memory with given id |
| `GET` | `/api/get_patient_pic` | Returns patient's profile photo, if at all saved |
| `POST` | `/api/create_account_st1` | Creates stage 1 account |
| `POST` | `/api/create_account_st2` | Creates stage 2 (final) account |
| `POST` | `/api/add_patient_photo` | Saves patient's photo |
| `POST` | `/api/delete_family_member/<id>` | Deletes a family member with given id |
| `POST` | `/api/add_family_member` | Adds a family member |
| `POST` | `/api/add_memory` | Adds a memory |
| `POST` | `/api/login` | Logs in the given user, if credentials are authenticated |
| `POST` | `/api/add_profile_image` | Saves profile photo of user |

---

## requirements.txt

```
Flask
flask-cors
flask-wtf
flask-socketio
face_recognition
numpy
opencv-contrib-python
```
---

## Some Acknowledgements

Built with empathy for the millions of families navigating the challenges of dementia. We made Memora due to a simple reason - When memories fade, relationships shouldn't.

---
# Made by
#### Team Name - The Cullinan
1. [Rahul Pagare](https://www.github.com/RahulPagare20) - Backend developer
2. [Aakira Khot](https://www.github.com/Aakira14) - Frontend developer
##### Built for the 2026 steminate hacks.