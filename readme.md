# 🛒 API فروشگاه امیر

یه API حرفه‌ای فروشگاهی با **Django REST Framework** با احراز هویت **JWT**، سبد خرید، سفارش‌ها، و مستندات **Swagger**.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Django](https://img.shields.io/badge/Django-6.1-green?logo=django)
![DRF](https://img.shields.io/badge/DRF-3.18-red?logo=django)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🌐 دموی آنلاین

- **API:** [https://amirho3n.pythonanywhere.com/](https://amirho3n.pythonanywhere.com/)
- **مستندات (Swagger):** [https://amirho3n.pythonanywhere.com/api/docs/](https://amirho3n.pythonanywhere.com/api/docs/)
- **مستندات (ReDoc):** [https://amirho3n.pythonanywhere.com/api/redoc/](https://amirho3n.pythonanywhere.com/api/redoc/)

---

## ✨ ویژگی‌ها

- 🔐 **احراز هویت با JWT** (Access + Refresh + Blacklist)
- 👤 **مدیریت کاربران** (ثبت‌نام، پروفایل، تغییر رمز)
- 🛍️ **مدیریت محصولات** (CRUD + فیلتر + جستجو + مرتب‌سازی)
- 🏷️ **دسته‌بندی محصولات**
- 🛒 **سبد خرید** (افزودن، حذف، ویرایش، خالی کردن)
- 📦 **سفارش‌ها** (Checkout از سبد خرید)
- 📚 **مستندات خودکار** با Swagger و ReDoc
- 🛡️ **امنیت** (JWT, Rate Limiting, CORS, HTTPS)
- 🧪 **۳۰ تست Unit** (مدل‌ها + APIها)
- 📝 **لاگ‌گیری حرفه‌ای** (Rotating File Handler)

---

## 🛠️ تکنولوژی‌ها

| تکنولوژی              | نسخه  | کاربرد            |
| --------------------- | ----- | ----------------- |
| Python                | 3.13  | زبان برنامه‌نویسی |
| Django                | 6.1   | فریم‌ورک وب       |
| Django REST Framework | 3.18  | ساخت API          |
| SimpleJWT             | 5.3+  | احراز هویت        |
| django-filter         | 24+   | فیلتر             |
| drf-spectacular       | 0.27+ | مستندات           |
| django-cors-headers   | 4.3+  | CORS              |
| python-decouple       | 3.8+  | متغیرهای محیطی    |
| Pillow                | 10+   | مدیریت تصاویر     |
| SQLite                | -     | دیتابیس (لوکال)   |

---

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.13+
- Git

### ۱. کلون کردن پروژه

```bash
git clone https://github.com/Amirho3nPouri/project3-shop-api.git
cd project3-shop-api
```

---

# ویندوز

python -m venv venv
venv\Scripts\activate

# لینوکس/مک

python3 -m venv venv
source venv/bin/activate

---

pip install -r requirements.txt

---

SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
برای ساخت secret_key :
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

---
