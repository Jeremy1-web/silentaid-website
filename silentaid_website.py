# ===============================
# SilentAid Website (Flask)
# Fully corrected, Render & Pydroid 3 ready
# ===============================

from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
import os

# -------------------------------
# 1. CREATE FLASK APP
# -------------------------------
app = Flask(__name__)

# -------------------------------
# 2. DATABASE SETUP
# -------------------------------
DB_NAME = "silentaid.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            country TEXT
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS ngos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            country TEXT,
            contact TEXT
        )
    """)
    db.commit()
    db.close()

# Initialize database
init_db()

# -------------------------------
# 3. HTML TEMPLATES (INLINE)
# -------------------------------
HOME_HTML = """
<h1>🚨 SilentAid Official Website</h1>
<p>Global Emergency Help Platform</p>
<a href="/register">Register as User</a><br><br>
<a href="/ngo">Register NGO</a><br><br>
<a href="/admin">Admin Dashboard</a>
"""

REGISTER_HTML = """
<h2>User Registration</h2>
<form method="post">
  Name: <input name="name" required><br><br>
  Email: <input name="email" required><br><br>
  Country: <input name="country" required><br><br>
  <button type="submit">Register</button>
</form>
<a href="/">Back</a>
"""

NGO_HTML = """
<h2>NGO Registration</h2>
<form method="post">
  NGO Name: <input name="name" required><br><br>
  Country: <input name="country" required><br><br>
  Contact: <input name="contact" required><br><br>
  <button type="submit">Register NGO</button>
</form>
<a href="/">Back</a>
"""

ADMIN_HTML = """
<h2>Admin Dashboard</h2>
<h3>Users</h3>
<ul>
{% for u in users %}
<li>{{ u['name'] }} - {{ u['country'] }}</li>
{% endfor %}
</ul>
<h3>NGOs</h3>
<ul>
{% for n in ngos %}
<li>{{ n['name'] }} - {{ n['country'] }}</li>
{% endfor %}
</ul>
<a href="/">Back</a>
"""

# -------------------------------
# 4. ROUTES
# -------------------------------
@app.route("/")
def home():
    return render_template_string(HOME_HTML)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        db = get_db()
        db.execute(
            "INSERT INTO users (name, email, country) VALUES (?, ?, ?)",
            (request.form["name"], request.form["email"], request.form["country"])
        )
        db.commit()
        db.close()
        return redirect(url_for("home"))
    return render_template_string(REGISTER_HTML)

@app.route("/ngo", methods=["GET", "POST"])
def ngo():
    if request.method == "POST":
        db = get_db()
        db.execute(
            "INSERT INTO ngos (name, country, contact) VALUES (?, ?, ?)",
            (request.form["name"], request.form["country"], request.form["contact"])
        )
        db.commit()
        db.close()
        return redirect(url_for("home"))
    return render_template_string(NGO_HTML)

@app.route("/admin")
def admin():
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()
    ngos = db.execute("SELECT * FROM ngos").fetchall()
    db.close()
    return render_template_string(ADMIN_HTML, users=users, ngos=ngos)

# -------------------------------
# 5. RUN SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)