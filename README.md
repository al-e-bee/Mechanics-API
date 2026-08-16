# Mechanics API

A production-ready Flask RESTful API built using the Application Factory pattern, SQLAlchemy ORM, Marshmallow serialization, and JWT role-based access control (RBAC). It provides complete management of customers, mechanics, parts inventory, and vehicle service tickets.

The application is deployed on **Render** with a managed **PostgreSQL** database and includes an automated **CI/CD pipeline** via **GitHub Actions** for continuous testing and deployment.

---

## Live Links & Documentation

- **Live API Base URL:** [https://mechanics-api-1p5p.onrender.com](https://mechanics-api-1p5p.onrender.com)
- **Interactive Swagger UI:** [https://mechanics-api-1p5p.onrender.com/api/docs/](https://mechanics-api-1p5p.onrender.com/api/docs/)

> **Note:** Visiting the root URL automatically redirects directly to the Swagger UI documentation interface.

---

## Key Features

- **JWT Role-Based Access Control (RBAC):** Token generation and route protection for `customer` and `mechanic` roles.
- **Rate Limiting & In-Memory Caching:** Endpoint throttling via Flask-Limiter and response caching via Flask-Caching.
- **Interactive Documentation:** Fully documented OpenAPI/Swagger 2.0 interface.
- **Automated Unit Testing:** 53 unit tests using Python's `unittest` framework covering CRUD operations, validation schemas, and role restrictions.
- **CI/CD Pipeline:** Automated GitHub Actions workflow running tests on every push/PR and triggering deployment to Render only when all tests pass.
- **Production Architecture:** Served using Gunicorn WSGI server and connected to a hosted PostgreSQL database on Render.

---

## CI/CD Workflow & Deployment Pipeline

```text
Push to main / master
         │
         ▼
 ┌───────────────┐
 │   Test Job    │ ───► Executes 53 unit tests in an isolated Python 3.12 runner
 └───────┬───────┘
         │ (Pass)
         ▼
 ┌───────────────┐
 │  Deploy Job   │ ───► Triggers Render Deploy Hook via SERVICE_ID & RENDER_API_KEY
 └───────────────┘
```

1. **Continuous Integration (Test Job):** Checks out code, sets up Python 3.12, installs dependencies from `requirements.txt`, and runs all unit tests.
2. **Continuous Deployment (Deploy Job):** Runs conditionally (`needs: test`). If all tests pass, it uses the Render API to deploy the latest commit to production.

---

## API Endpoints

### 1. Customers Blueprint (`/customers`)

| Method | Endpoint | Description | Auth / Role |
| :--- | :--- | :--- | :--- |
| `POST` | `/customers/` | Register a new customer | None |
| `POST` | `/customers/login` | Authenticate customer and obtain JWT | None |
| `GET` | `/customers/` | Retrieve all customers (with pagination & caching) | None |
| `GET` | `/customers/<id>` | Retrieve a single customer profile | None |
| `GET` | `/customers/my-tickets` | Retrieve logged-in customer's service tickets | Customer |
| `PUT` | `/customers/<id>` | Update customer account details | Customer (Self Only) |
| `DELETE` | `/customers/<id>` | Delete customer account | Customer (Self Only) |

### 2. Mechanics Blueprint (`/mechanics`)

| Method | Endpoint | Description | Auth / Role |
| :--- | :--- | :--- | :--- |
| `POST` | `/mechanics/` | Register a new mechanic | None |
| `POST` | `/mechanics/login` | Authenticate mechanic and obtain JWT | None |
| `GET` | `/mechanics/` | Retrieve all mechanics | None |
| `GET` | `/mechanics/top-performers` | Retrieve mechanics ordered by completed tickets | None |
| `GET` | `/mechanics/<id>` | Retrieve a single mechanic profile | None |
| `PUT` | `/mechanics/<id>` | Update mechanic profile | Mechanic (Self Only) |
| `DELETE` | `/mechanics/<id>` | Delete mechanic profile | Mechanic (Self Only) |

### 3. Inventory Blueprint (`/inventory`)

| Method | Endpoint | Description | Auth / Role |
| :--- | :--- | :--- | :--- |
| `POST` | `/inventory/` | Add a new inventory item | None |
| `GET` | `/inventory/` | Retrieve all inventory items | None |
| `GET` | `/inventory/<id>` | Retrieve a single inventory item | None |
| `PUT` | `/inventory/<id>` | Update part details/pricing | Mechanic |
| `DELETE` | `/inventory/<id>` | Remove part from inventory | Mechanic |

### 4. Service Tickets Blueprint (`/service-tickets`)

| Method | Endpoint | Description | Auth / Role |
| :--- | :--- | :--- | :--- |
| `POST` | `/service-tickets/` | Create a new service ticket | None |
| `GET` | `/service-tickets/` | Retrieve all service tickets | None |
| `GET` | `/service-tickets/<id>` | Retrieve a single service ticket | None |
| `PUT` | `/service-tickets/<id>/assign-mechanic/<mech_id>` | Assign a mechanic to a ticket | None |
| `PUT` | `/service-tickets/<id>/remove-mechanic/<mech_id>` | Remove a mechanic from a ticket | None |
| `PUT` | `/service-tickets/<id>/edit` | Bulk assign/remove mechanics | None |
| `PUT` | `/service-tickets/<id>/add-part/<part_id>` | Add an inventory part to a ticket | Mechanic |


## Local Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/al-e-bee/Mechanics-API.git
cd BE-mechanics-api
```

### 2. Create and activate a virtual environment

```bash
# Windows (cmd/PowerShell)
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URI=mysql+mysqlconnector://user:password@localhost:3306/mechanics_db
SECRET_KEY=your-super-secret-jwt-key
```

### 5. Run the application

```bash
# Development server
flask --app flask_app run

# Or via Gunicorn
gunicorn flask_app:app
```

---

## Running Automated Tests

Run the full test suite locally:

```bash
# Run all 53 unit tests
python -m unittest discover -s tests -p "test_*.py"

# Or run individual test modules
python -m unittest tests/test_customers.py
python -m unittest tests/test_mechanics.py
python -m unittest tests/test_inventory.py
python -m unittest tests/test_service_tickets.py
```
