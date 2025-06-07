---
## 🍽️ Food Reserve — Restaurant Reservation System

A simple web-based food reservation system (e.g., restaurant table booking or food event ticketing) built using modern technologies. Users can browse menus, reserve tables, and manage their bookings.
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

### 🛡️ Environment Variables

Set these in `.env` files inside each service:

- **Backend**:

  ```env
  SECRET_KEY=your-secret-key
  DEBUG=True
  DB_NAME=foodreserve
  DB_USER=admin
  DB_PASSWORD=adminpass
  ```

- **Frontend**:
  ```env
  NEXT_PUBLIC_API_URL=http://localhost:8000/api
  ```

---

### 🧪 Testing

You can test the API endpoints via:

- **Swagger UI**: http://localhost/api/docs

---
