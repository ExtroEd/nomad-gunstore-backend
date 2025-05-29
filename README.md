<h1 align="center">
  Nomad Gunstore Backend
</h1>

<p align="center">
  🛡️ Backend for the fictional <strong>Nomad Tactical</strong> online weapon store, inspired by real-world retailers like Palmetto State Armory.<br>
  Built as part of a thesis project at <em>Nomad College</em>.
</p>

<p align="center">
  <img src="https://res.cloudinary.com/dqvsugnvd/image/upload/v1748533103/nomad/nomad_logo.png" width="200" alt="Nomad Tactical Logo" />
</p>

---

## 🚀 Features

- 🔐 Secure user registration with email verification
- 📨 Beautiful HTML emails with Celery + Gmail SMTP
- 🧠 Token-based authentication (JWT-ready)
- 📦 PostgreSQL + Redis + Dockerized architecture
- 📁 Static/media file handling via Nginx
- 🧪 DRF-based API with auto-generated Swagger docs
- 🛠️ Admin panel + CKEditor integration

---

## 📦 Tech Stack

- **Python 3.12**
- **Django 4.x**
- **Django REST Framework**
- **Celery + Redis**
- **PostgreSQL**
- **Docker & Docker Compose**
- **Nginx**
- **Cloudinary** for media delivery

---

## ⚙️ Installation

```bash
git clone https://github.com/yourname/nomad-gunstore-backend.git
cd nomad-gunstore-backend
cp .env.example .env  # add your secrets
docker-compose up --build
```

---

## 🧠 Environment Variables (.env)

<details>
<summary>Click to expand</summary>

```env
# Email (Gmail SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Database
POSTGRES_DB=your_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis (Celery broker)
CELERY_BROKER_URL=redis://redis:6379/0

# Cloudinary
CLOUDINARY_NAME=your_cloud_name
CLOUDINARY_KEY=your_api_key
CLOUDINARY_SECRET=your_secret
LOGO_URL=https://res.cloudinary.com/your_cloud/image/upload/vXXX/logo.png
```
