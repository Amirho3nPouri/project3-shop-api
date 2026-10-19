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

![PhemaPlant](image.png)

---

## ✨ ویژگی‌ها

### 🛍️ فروشگاه

- ✅ مدیریت محصولات (CRUD)
- ✅ دسته‌بندی محصولات
- ✅ محصولات ویژه (Featured)
- ✅ سبد خرید کامل
- ✅ ثبت سفارش
- ✅ تاریخچه سفارش‌ها
- ✅ فیلتر، جستجو، مرتب‌سازی
- ✅ صفحه‌بندی
- ✅ اسکرول افقی محصولات ویژه

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
- ✅ دکمه‌ی چشم برای رمز
- ✅ صفحه ۴۰۴ و ۵۰۰ سفارشی
- ✅ صفحه درباره ما، تماس، سوالات متداول، شرایط ارسال، حریم خصوصی

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
- ✅ کیت امنیتی کامل (`docs/security/`)

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
