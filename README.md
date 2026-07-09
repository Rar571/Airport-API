# ✈️ Airport Management REST API

A production-ready RESTful API built with Django REST Framework (DRF) designed to automate 
and manage airport operations, flight scheduling, ticket ordering, and crew assignments. 

---

## 🚀 Key Features

* **Secure Authentication:** Complete user management cycle secured via JWT (JSON Web Tokens).
* **Comprehensive Airport Logistics:** Endpoints for managing airplanes, routes, crew members, airports, and synchronized flight schedules.
* **Order & Ticket Processing:** Atomic transaction handling for booking tickets, calculating capacities, and managing user orders.
* **Advanced Filtering & Search:** Optimized API lookup allowing clients to filter flights by airplane specifications, route origins, and destinations.
* **Media Management:** Built-in endpoint capabilities for handling secure multipart form-data image uploads for airplanes.
* **Self-Documenting API:** Fully integrated Interactive Swagger UI and ReDoc documentation.

---

## 🛠 Tech Stack

* **Backend Framework:** Python 3.x, Django, Django REST Framework (DRF)
* **Authentication:** Simple JWT (JSON Web Token)
* **Database:** PostgreSQL (Production-ready relational storage)
* **Containerization:** Docker & Docker Compose
* **API Documentation:** Interactive Swagger (drf-spectacular / drf-yasg)

---

## 🔒 API Access & Authentication

This API enforces token-based security. To interact with protected endpoints, follow this lifecycle:

1.  **Registration:** Send a `POST` request with user credentials to `/api/user/register/`.
2.  **Token Generation:** Send a `POST` request to `/api/user/token/` to obtain your access and refresh JWT pairs.
3.  **Authorized Requests:** Include the access token in your HTTP headers:
    ```http
    Authorization: Bearer <your_access_token>
    ```

Full interactive endpoint testing is available at: `/api/swagger/` or `/api/doc/`.

---

## 🐳 Quick Start with Docker (Recommended)

Make sure you have [Docker](https://docs.docker.com/get-docker/) and 
[Docker Compose](https://docs.docker.com/compose/install/) installed.

1. **Clone the Repository:**
```bash
git clone https://github.com/Rar571/Airport-API.git
cd Airport-API
```
2. **Configure Environment Variables:**

Create a .env file in the root directory and define your credentials (refer to .env.sample if available):
```bash
POSTGRES_DB=airport_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=db
SECRET_KEY=your_django_secret_key
```
3. **Spin Up the Containers:**
```bash
docker-compose up --build
```
This single command builds the application image, downloads PostgreSQL,
sets up volume bindings, executes migrations, and starts the Django development server.
## ⚙️ Manual Local Installation
If you prefer to run the application outside of Docker:
1. **Set Up Virtual Environment:**
```bash
python -m venv venv
    
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```
2. **Install Dependencies & Configure Environment**
```bash
pip install -r requirements.txt

# Windows (Command Prompt)
set POSTGRES_HOST=localhost
set POSTGRES_DATABASE=your_db_name
set POSTGRES_USER=your_username
set POSTGRES_PASSWORD=your_password
set SECRET_KEY=your_secret_key

# Linux / macOS (Terminal)
export POSTGRES_HOST=localhost
```
3. **Initialize Database & Run**
```bash
python manage.py migrate
python manage.py runserver
The server will be available at http://127.0.0.1:8000/
```
