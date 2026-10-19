# 🌿 PhemaPlant

> **گل برای گل‌های فیما** — فروشگاه آنلاین گیاهان آپارتمانی، گلدان، و لوازم جانبی

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.1-green?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.18-red?logo=django&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-SimpleJWT-black?logo=jsonwebtokens&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Live-success)

---

## 🌐 دموی آنلاین

| بخش                       | لینک                                                                                     |
| ------------------------- | ---------------------------------------------------------------------------------------- |
| **سایت**                  | [amirho3n.pythonanywhere.com](https://amirho3n.pythonanywhere.com/)                      |
| **مستندات API (Swagger)** | [amirho3n.pythonanywhere.com/api/docs/](https://amirho3n.pythonanywhere.com/api/docs/)   |
| **مستندات API (ReDoc)**   | [amirho3n.pythonanywhere.com/api/redoc/](https://amirho3n.pythonanywhere.com/api/redoc/) |
| **پنل ادمین**             | [amirho3n.pythonanywhere.com/admin/](https://amirho3n.pythonanywhere.com/admin/)         |

---

## 📸 اسکرین‌شات

> **TODO:** اسکرین‌شات‌ها رو بعداً اضافه کن.

---

## ✨ ویژگی‌ها

### 🛍️ فروشگاه

- ✅ مدیریت محصولات (CRUD)
- ✅ دسته‌بندی محصولات
- ✅ سبد خرید کامل
- ✅ ثبت سفارش
- ✅ تاریخچه سفارش‌ها
- ✅ فیلتر، جستجو، مرتب‌سازی
- ✅ صفحه‌بندی
- ✅ گالری تصاویر (آینده)

### 👤 کاربران

- ✅ ثبت‌نام
- ✅ ورود با JWT
- ✅ پروفایل کاربر
- ✅ ویرایش پروفایل
- ✅ تغییر رمز
- ✅ بازیابی رمز عبور
- ✅ قفل حساب بعد از ۵ تلاش ناموفق
- ✅ Logout امن (Blacklist)

### 🎨 فرانت‌اند

- ✅ طراحی راست‌چین (RTL)
- ✅ ریسپانسیو (موبایل، تبلت، دسکتاپ)
- ✅ حالت تاریک (Dark Mode) با آفتابگردان
- ✅ اسکرول نرم (Lenis)
- ✅ Reveal on Scroll
- ✅ Parallax
- ✅ Skeleton Loading
- ✅ انیمیشن Add to Cart
- ✅ Toast Notification
- ✅ منوی موبایل
- ✅ صفحه ۴۰۴ و ۵۰۰ سفارشی

### 🔐 امنیت

- ✅ JWT (Access + Refresh + Blacklist)
- ✅ Argon2id (هش رمز)
- ✅ قفل حساب بعد از ۵ تلاش
- ✅ Rate Limiting (DRF Throttling)
- ✅ CSRF Protection
- ✅ XSS Protection (`escapeHTML`)
- ✅ HTTPS
- ✅ HSTS
- ✅ CORS
- ✅ Secret Management (`.env`)
- ✅ Logging

### 📚 مستندات

- ✅ Swagger UI
- ✅ ReDoc
- ✅ OpenAPI 3.0 Schema
- ✅ ۳۰ تست Unit

---

## 🛠️ تکنولوژی‌ها

### Backend

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
| Argon2                | 23+   | هش رمز            |

### Frontend

| تکنولوژی     | کاربرد       |
| ------------ | ------------ |
| Tailwind CSS | استایل (CDN) |
| Vazirmatn    | فونت فارسی   |
| Lenis        | اسکرول نرم   |
| Vanilla JS   | منطق         |

### Database

| تکنولوژی | کاربرد                     |
| -------- | -------------------------- |
| SQLite   | دیتابیس (لوکال + پروداکشن) |

---

## 📂 ساختار پروژه

project3/
├── config/
│ ├── settings.py # تنظیمات
│ ├── urls.py # URLهای اصلی
│ └── ...
├── shop/
│ ├── models.py # مدل‌ها
│ ├── serializers.py # سریالایزرها
│ ├── views.py # API ViewSetها
│ ├── urls.py # URLهای API
│ ├── web_views.py # ویوهای HTML
│ ├── web_urls.py # URLهای HTML
│ ├── admin.py # پنل ادمین
│ ├── tests.py # ۳۰ تست
│ ├── templates/
│ │ └── shop/
│ │ ├── base.html # تمپلیت پایه
│ │ ├── home.html
│ │ ├── product_list.html
│ │ ├── product_detail.html
│ │ ├── category_list.html
│ │ ├── cart.html
│ │ ├── orders.html
│ │ ├── login.html
│ │ ├── register.html
│ │ ├── profile.html
│ │ ├── about.html
│ │ ├── contact.html
│ │ ├── faq.html
│ │ ├── shipping.html
│ │ ├── privacy.html
│ │ ├── 404.html
│ │ └── 500.html
│ └── static/
│ └── shop/
│ ├── css/style.css
│ ├── js/main.js
│ └── img/logo.png
├── templates/
│ └── registration/ # تمپلیت‌های Password Reset
├── docs/
│ └── security/ # کیت امنیتی
├── logs/ # لاگ‌ها
├── media/ # فایل‌های آپلودی
├── staticfiles/ # فایل‌های استاتیک (collectstatic)
├── .env # متغیرهای محیطی (تو گیت نیست)
├── .env.example # نمونه
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md

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
