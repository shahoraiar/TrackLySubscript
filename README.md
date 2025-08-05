# TracklySubscript

TracklySubscript is a Django-based subscription management application that uses JWT authentication, Redis, Celery, and AJAX for a responsive and real-time experience. Users can subscribe to different plans, view exchange rates, and manage their subscriptions.

---

## 🚀 Features

- ✅ JWT-based authentication (access & refresh tokens)
- ✅ Subscription creation and cancellation with partial refund logic
- ✅ Currency conversion using USD to BDT with exchange rate fetched via Celery task
- ✅ Redis as Celery broker
- ✅ Admin-facing AJAX-powered dashboards:
  - Exchange rate logs
  - All user subscription list
- ✅ Wallet management for users
- ✅ API responses in JSON

---

## ⚙️ Technologies Used

- Python (Django)
- Django REST Framework
- Celery + Redis
- Django Celery Beat
- PostgreSQL / SQLite (your choice)
- AJAX (for data tables)
- JWT (using SimpleJWT)

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shahoraiar/TrackLySubscript.git
cd TracklySubscript
```
### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
### 3. Install Requirements
```bash
pip install -r requirements.txt
```
### 4. Run Migrations
```bash
python manage.py migrate
```
### 5. Create Superuser (optional)
```bash
python manage.py createsuperuser
```
### 6. Run the Server
```bash
python manage.py runserver
```
## 🔁 Celery Setup

### 1. Start Redis Server
Make sure Redis is running locally on port 6379:
```bash
redis-server
```
### 2. Start Celery Worker
```bash
celery -A subscription_project_jwt worker -l info
```
### 3. Start Celery Beat (for periodic tasks)
```bash
celery -A subscription_project_jwt beat -l info
```
## 🔑 JWT Authentication
TracklySubscript uses Simple JWT for token-based auth.

## 🔌 API Endpoints
🔐 Auth APIs
| Endpoint         | Method | Description                                   |
| ---------------- | ------ | --------------------------------------------- |
| `/api/register`  | POST   | Register new user                             |
| `/api/login`     | POST   | Login and receive JWT tokens                  |
| `/api/user/info` | GET    | Get current user's data + subscription status |

💳 Subscription APIs
| Endpoint                   | Method | Description                                       |
| -------------------------- | ------ | ------------------------------------------------- |
| `/api/plan/info`           | GET    | List all available subscription plans             |
| `/api/subscription`        | POST   | Subscribe to a plan (deducts from wallet)         |
| `/api/cancel/subscription` | POST   | Cancel subscription and refund based on days used |
💱 Exchange Rate
| Endpoint             | Method | Description                           |
| -------------------- | ------ | ------------------------------------- |
| `/`                  | POST   | AJAX-based ExchangeRateLog table      |
| `/subscription/list` | POST   | AJAX-based all-user subscription list |


# Subscription Management System (Django + DRF)

## 🔁 Background Task
- **Task:** `fetch_usd_to_bdt_rate` — A Celery task that fetches USD to BDT conversion rate using a free API and stores it in `ExchangeRateLog`.

## 📊 AJAX Tables
- **Exchange Rate List:** `/` — Renders a paginated table of historical exchange rates using AJAX.  
- **All User Subscription List:** `/subscription/list` — Shows all users' subscription details (username, plan, status, etc.).

## 💰 Wallet Logic
- Every new user starts with a balance of **1000 BDT**.  
- Subscribing deducts money from wallet based on the current **USD → BDT** rate.  
- Cancelling a subscription within **7 days** returns **full refund**, otherwise refund is **prorated** by day.

👨‍💻 Developer
Built with ❤️ by Shahoraiar Hossain
