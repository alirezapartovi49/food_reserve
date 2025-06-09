---
## 🍽️ Food Reserve — Restaurant Reservation System

#### A simple web-based food reservation system (e.g., restaurant table booking or food event ticketing) built using modern technologies. Users can browse menus, reserve tables, and manage their bookings.
---

### 🔧 Tech Stack

- **Backend**: [Django](https://www.djangoproject.com/) + Django REST Framework (DRF)
- **Frontend**: [Next.js](https://nextjs.org/)
- **Web Server**: [Nginx](https://nginx.org/) (Reverse Proxy)
- **Containerization**: [Docker & Docker Compose](https://www.docker.com/)

---

### 📦 Features

- Browse menu items
- View available time slots
- Book/reserve a table
- User authentication (login/register)
- Admin dashboard to manage reservations and menus
- Clean, responsive UI

---

### 🚀 Getting Started

#### 1. Clone the repository

```bash
git clone https://github.com/yourusername/food_reserve.git
cd food_reserve
```

#### 2. Build and run with Docker Compose

```bash
docker-compose up --build
```

Once successfully running:

- **Frontend**: http://localhost
- **Admin Panel**: http://localhost/api/admin  
  _(Use Django superuser credentials to log in)_

#### 3. Create a superuser (optional)

```bash
docker-compose exec backend python manage.py createsuperuser
```

---

### 📁 Project Structure

```
food_reserve/
│
├── backend/            # Django API
├── frontend/           # Next.js App
├── nginx/              # Nginx config
├── docker-compose.yml  # Multi-container orchestration
└── README.md
```

---

### 🧪 Testing

the api docs is in this link and you can run backend tests with python manage.py test {{app_name}}

```
cd backend
python manage.py test accounts # and more like auth, food, reserve
```

- **Swagger UI**: http://localhost/api/docs

---
