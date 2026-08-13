# Mechanics API

A Flask RESTful API built with SQLAlchemy, Marshmallow, and the Application Factory pattern for managing mechanics, customers, service tickets, and parts inventory.

## Features & Endpoints

- **Customers:** Create, view, update, and delete customer records (`/customers`)
- **Mechanics:** Create, view, update, and delete mechanic profiles (`/mechanics`)
- **Service Tickets:** Manage vehicle service tickets, assign mechanics, and attach parts (`/service_tickets`)
- **Inventory:** Create, view, update, and delete parts inventory (`/inventory`)

### Inventory & Ticket Parts Endpoints

```
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/inventory/` | Create a new inventory item | No |
| `GET` | `/inventory/` | Retrieve all inventory items | No |
| `GET` | `/inventory/<id>` | Retrieve a specific item | No |
| `PUT` | `/inventory/<id>` | Update an inventory item | Yes (Mechanic) |
| `DELETE` | `/inventory/<id>` | Delete an inventory item | Yes (Mechanic) |
| `PUT` | `/service-tickets/<ticket_id>/add-part/<part_id>` | Add inventory part to ticket | Yes (Mechanic) |
```

## Setup & Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/al-e-bee/Mechanics-API.git
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
