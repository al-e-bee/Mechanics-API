# Mechanics API

A production-ready Flask RESTful API built using the Application Factory pattern, SQLAlchemy ORM, Marshmallow serialization, and JWT role-based access control (RBAC). It provides complete management of customers, mechanics, parts inventory, and vehicle service tickets.

---

## Key Features

- **JWT Role-Based Authentication:** Secure token generation and endpoint protection tailored for `customer` and `mechanic` roles.
- **Rate Limiting & Caching:** Built-in endpoint throttling via Flask-Limiter and performance caching via Flask-Caching.
- **Interactive Documentation:** Fully documented interactive Swagger UI schema.
- **Automated Unit Testing:** Test suite built with Python's native `unittest` framework covering positive, negative, and role-restricted execution paths.

---

## API Endpoints

### 1. Customers Blueprint (`/customers`)

| Method   | Endpoint                | Description                                   | Auth / Role          |
| :------- | :---------------------- | :-------------------------------------------- | :------------------- |
| `POST`   | `/customers/`           | Register a new customer                       | None                 |
| `POST`   | `/customers/login`      | Authenticate customer and obtain JWT          | None                 |
| `GET`    | `/customers/`           | Retrieve all customers (with pagination)      | None (Cached)        |
| `GET`    | `/customers/<id>`       | Retrieve a single customer profile            | None                 |
| `GET`    | `/customers/my-tickets` | Retrieve logged-in customer's service tickets | Customer             |
| `PUT`    | `/customers/<id>`       | Update customer account details               | Customer (Self Only) |
| `DELETE` | `/customers/<id>`       | Delete customer account                       | Customer (Self Only) |

### 2. Mechanics Blueprint (`/mechanics`)

| Method   | Endpoint                    | Description                                     | Auth / Role          |
| :------- | :-------------------------- | :---------------------------------------------- | :------------------- |
| `POST`   | `/mechanics/`               | Register a new mechanic                         | None                 |
| `POST`   | `/mechanics/login`          | Authenticate mechanic and obtain JWT            | None                 |
| `GET`    | `/mechanics/`               | Retrieve all mechanics                          | None                 |
| `GET`    | `/mechanics/top-performers` | Retrieve mechanics ordered by completed tickets | None                 |
| `GET`    | `/mechanics/<id>`           | Retrieve a single mechanic profile              | None                 |
| `PUT`    | `/mechanics/<id>`           | Update mechanic profile                         | Mechanic (Self Only) |
| `DELETE` | `/mechanics/<id>`           | Delete mechanic profile                         | Mechanic (Self Only) |

### 3. Inventory Blueprint (`/inventory`)

| Method   | Endpoint          | Description                      | Auth / Role |
| :------- | :---------------- | :------------------------------- | :---------- |
| `POST`   | `/inventory/`     | Add a new inventory item         | None        |
| `GET`    | `/inventory/`     | Retrieve all inventory items     | None        |
| `GET`    | `/inventory/<id>` | Retrieve a single inventory item | None        |
| `PUT`    | `/inventory/<id>` | Update part details/pricing      | Mechanic    |
| `DELETE` | `/inventory/<id>` | Remove part from inventory       | Mechanic    |

### 4. Service Tickets Blueprint (`/service-tickets`)

| Method | Endpoint                                          | Description                       | Auth / Role |
| :----- | :------------------------------------------------ | :-------------------------------- | :---------- |
| `POST` | `/service-tickets/`                               | Create a new service ticket       | None        |
| `GET`  | `/service-tickets/`                               | Retrieve all service tickets      | None        |
| `GET`  | `/service-tickets/<id>`                           | Retrieve a single service ticket  | None        |
| `PUT`  | `/service-tickets/<id>/assign-mechanic/<mech_id>` | Assign a mechanic to a ticket     | None        |
| `PUT`  | `/service-tickets/<id>/remove-mechanic/<mech_id>` | Remove a mechanic from a ticket   | None        |
| `PUT`  | `/service-tickets/<id>/edit`                      | Bulk assign/remove mechanics      | None        |
| `PUT`  | `/service-tickets/<id>/add-part/<part_id>`        | Add an inventory part to a ticket | Mechanic    |

---

## Setup & Installation

**1. Clone the repository:**

```bash
git clone [https://github.com/al-e-bee/Mechanics-API.git](https://github.com/al-e-bee/Mechanics-API.git)
cd BE-mechanics-api

```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv
```

```cmd
venv\Scripts\activate
```

- **On macOS/Linux:**

```bash
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Run the application:**

```bash
python app.py
```

---

## Interactive Documentation (Swagger UI)

Access the live interactive Swagger UI documentation directly in your browser:

[http://127.0.0.1:5000/docs/](http://127.0.0.1:5000/docs/)

---

## Running Automated Tests

Run the full automated test suite using `unittest`:

```bash
# Run all discovered tests
python -m unittest discover tests

# Or run individual test modules
python -m unittest tests/test_customers.py
python -m unittest tests/test_mechanics.py
python -m unittest tests/test_inventory.py
python -m unittest tests/test_service_tickets.py
```
