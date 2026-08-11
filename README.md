# Mechanics API

A Flask RESTful API built with SQLAlchemy, Marshmallow, and the Application Factory pattern for managing mechanics, customers, and service tickets.

## Features & Endpoints

- **Customers:** Create, view, update, and delete customer records (`/customers`)
- **Mechanics:** Create, view, update, and delete mechanic profiles (`/mechanics`)
- **Service Tickets:** Manage vehicle service tickets and assign mechanics (`/service_tickets`)

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
