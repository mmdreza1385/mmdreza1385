from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import json, os

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

DATA_FILE = "data.json"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123456"  # حتماً قبل از انتشار تغییر دهید

DEFAULT_DATA = {
    "name": "سیدمحمدرضا طباطبائی",
    "title": "برنامه‌نویس، توسعه‌دهنده وب و خبرنگار",
    "bio": "کارت ویزیت هوشمند شخصی",
    "phone": "09120000000",
    "email": "example@example.com",
    "website": "https://example.com",
    "socials": [
        {"name": "Telegram", "icon": "✈️", "url": "https://t.me/username", "enabled": True},
        {"name": "Instagram", "icon": "📸", "url": "https://instagram.com/username", "enabled": True},
        {"name": "WhatsApp", "icon": "💬", "url": "https://wa.me/989120000000", "enabled": True},
        {"name": "GitHub", "icon": "💻", "url": "https://github.com/username", "enabled": True},
        {"name": "LinkedIn", "icon": "🔗", "url": "https://linkedin.com/in/username", "enabled": True}
    ]
}

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper

@app.route("/")
def index():
    return render_template("index.html", data=load_data())

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))
        flash("نام کاربری یا رمز عبور اشتباه است.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    data = load_data()

    if request.method == "POST":
        data["name"] = request.form.get("name", "")
        data["title"] = request.form.get("title", "")
        data["bio"] = request.form.get("bio", "")
        data["phone"] = request.form.get("phone", "")
        data["email"] = request.form.get("email", "")
        data["website"] = request.form.get("website", "")

        names = request.form.getlist("social_name")
        icons = request.form.getlist("social_icon")
        urls = request.form.getlist("social_url")
        enabled = request.form.getlist("social_enabled")

        data["socials"] = []
        for i in range(len(names)):
            data["socials"].append({
                "name": names[i],
                "icon": icons[i],
                "url": urls[i],
                "enabled": str(i) in enabled
            })

        save_data(data)
        flash("اطلاعات کارت با موفقیت ذخیره شد.", "success")
        return redirect(url_for("admin"))

    return render_template("admin.html", data=data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
