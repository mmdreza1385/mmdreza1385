# کارت ویزیت هوشمند Python

## اجرا در ویندوز

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

سپس:
- کارت: http://127.0.0.1:5000
- پنل مدیریت: http://127.0.0.1:5000/login

ورود پیش‌فرض:
- username: admin
- password: 123456

قبل از انتشار، `ADMIN_PASSWORD` و `app.secret_key` را تغییر دهید.

این نسخه اطلاعات را در `data.json` ذخیره می‌کند و برای شروع ساده است.
