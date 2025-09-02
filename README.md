# innovators-arena-project
# Lost & Found Platform
A web-based Lost &amp; Found platform built with Flask lets users post lost or found items along with images. It also provides admin tools to manage the listings.


## Features
-  Add lost or found items with:
  - Title
  - Description
  - Location
  - Contact information
  - Optional image upload
-  Uploaded images are displayed alongside items
-  Admin login/logout system
  - Admins can delete items directly from the homepage
-  Secure storage using SQLite database
-  Responsive and clean design

---

## 🛠 Tech Stack
- **Backend:** Python (Flask)  
- **Database:** SQLite  
- **Frontend:** HTML, CSS (Jinja2 templating)  
- **File Uploads:** Stored in `static/uploads/`  
- **Session Management:** Flask-Session  

---

## ▶️ How to Run the Project Locally

### 1️⃣ Clone the Repository
`bash
git clone https://github.com/your-username/lostfound-platform.git
cd lostfound-platform`

### 2️⃣ Create & Activate a Virtual Environment
`python -m venv venv`
#### Windows ####
`venv\Scripts\activate`
#### Mac/Linux ####
`source venv/bin/activate`

### 3️⃣ Install Dependencies
`pip install -r requirements.txt`

### 4️⃣ Initialize the Database
`python init_db.py`

### 5️⃣ Run the Flask App
#### Mac/Linux ####
`export FLASK_APP=app.py
flask run`

#### Windows
`set FLASK_APP=app.py
flask run`





