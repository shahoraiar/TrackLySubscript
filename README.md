# TracklySubscript

TracklySubscript is a Django-based subscription management application that uses JWT authentication, Redis, Celery, and AJAX for a responsive and real-time experience. Users can subscribe to different plans, view exchange rates, and manage their subscriptions, while admins can track user subscriptions and exchange rates.

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
