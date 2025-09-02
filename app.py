from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from werkzeug.utils import secure_filename
import sqlite3
import os
import uuid

app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "supersecretkey"
Session(app)


# Upload folder
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Database setup
def init_db():
    conn = sqlite3.connect("lostfound.db")
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        location TEXT NOT NULL,
        type TEXT NOT NULL,
        contact TEXT NOT NULL,
        image TEXT
    )
    ''')
    conn.commit()
    conn.close()

init_db()


# Homepage
@app.route("/")
def home():
    conn = sqlite3.connect("lostfound.db")
    c = conn.cursor()
    c.execute("SELECT * FROM items ORDER BY id DESC")
    items = c.fetchall()
    conn.close()

    items_list = []
    for row in items:
        items_list.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "location": row[3],
            "type": row[4],
            "contact": row[5],
            "image": row[6]
        })
    return render_template("index.html", items=items_list)


# Add item page
@app.route("/add", methods=["GET", "POST"])
def additem():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        location = request.form["location"]
        type_ = request.form["type"]
        contact = request.form["contact"]

        # Handle image upload
        file = request.files.get("image")
        filename = None
        if file and file.filename != "":
            original_name = secure_filename(file.filename)
            unique_id = str(uuid.uuid4().hex)
            filename = f"{unique_id}_{original_name}"
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        # Insert into database
        conn = sqlite3.connect("lostfound.db")
        c = conn.cursor()
        c.execute('''
            INSERT INTO items (title, description, location, type, contact, image)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, description, location, type_, contact, filename))
        conn.commit()
        conn.close()

        flash("Item added successfully!", "success")
        return redirect(url_for("home"))

    return render_template("additem.html")


# Admin credentials
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "password123")


# Admin login page
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")
            return render_template("admin_login.html")
    return render_template("admin_login.html")


# Admin logout
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("home"))


# Delete item (admin only)
@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    if not session.get("admin"):
        return "Unauthorized", 403

    # Delete image file if exists
    conn = sqlite3.connect("lostfound.db")
    c = conn.cursor()
    c.execute("SELECT image FROM items WHERE id=?", (item_id,))
    row = c.fetchone()
    if row and row[0]:
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, row[0]))
        except FileNotFoundError:
            pass

    # Delete from database
    c.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    conn.close()

    flash("Item deleted successfully.", "info")
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)
