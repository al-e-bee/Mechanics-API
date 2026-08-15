import unittest
from app import create_app
from app.models import db, Customer, Service_Ticket
from app.utils.util import encode_token

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            # Seed test customer
            self.customer = Customer(
                name="Jane Doe",
                email="jane@email.com",
                password="password123",
                phone="555-123-4567"
            )
            db.session.add(self.customer)
            db.session.commit()
            self.customer_id = self.customer.id

            # Seed a service ticket with exact matching model fields
            self.ticket = Service_Ticket(
                VIN="1HGCR2F83HA123456",
                service_date="2026-08-15",
                service_desc="Oil change and tire rotation",
                customer_id=self.customer_id
            )
            db.session.add(self.ticket)
            db.session.commit()

        self.client = self.app.test_client()
        self.customer_token = encode_token(self.customer_id, 'customer')
        self.other_customer_token = encode_token(999, 'customer')
        self.mechanic_token = encode_token(1, 'mechanic')

    # --- CUSTOMER LOGIN ---
    def test_login_customer_success(self):
        payload = {
            "email": "jane@email.com",
            "password": "password123"
        }
        response = self.client.post('/customers/login', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertIn('token', response.json)

    def test_login_customer_invalid_credentials(self):
        payload = {
            "email": "jane@email.com",
            "password": "wrongpassword"
        }
        response = self.client.post('/customers/login', json=payload)
        self.assertEqual(response.status_code, 401)

    # --- CREATE NEW CUSTOMER ---
    def test_create_customer_success(self):
        payload = {
            "name": "John Smith",
            "email": "john@email.com",
            "password": "securepassword",
            "phone": "555-987-6543"
        }
        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Smith")

    def test_create_customer_duplicate_email(self):
        payload = {
            "name": "Jane Copy",
            "email": "jane@email.com",
            "password": "password123",
            "phone": "555-000-0000"
        }
        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_create_customer_missing_field(self):
        payload = {
            "name": "Incomplete User",
            "email": "incomplete@email.com",
            "password": "password123"
        }
        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['phone'], ['Missing data for required field.'])

    # --- RETRIEVE ALL / PAGINATION ---
    def test_get_customers_all(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertTrue(len(response.json) >= 1)

    def test_get_customers_paginated(self):
        response = self.client.get('/customers/?page=1&per_page=1')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 1)

    # --- GET CUSTOMER SERVICE TICKETS ---
    def test_get_my_tickets_success(self):
        headers = {"Authorization": f"Bearer {self.customer_token}"}
        response = self.client.get('/customers/my-tickets', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['service_desc'], "Oil change and tire rotation")

    def test_get_my_tickets_unauthorized_role(self):
        headers = {"Authorization": f"Bearer {self.mechanic_token}"}
        response = self.client.get('/customers/my-tickets', headers=headers)
        self.assertEqual(response.status_code, 403)

    # ---  GET SINGLE CUSTOMER BY ID ---
    def test_get_single_customer_success(self):
        response = self.client.get(f'/customers/{self.customer_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Jane Doe")

    def test_get_single_customer_not_found(self):
        response = self.client.get('/customers/9999')
        self.assertEqual(response.status_code, 404)

    # --- UPDATE CUSTOMER ---
    def test_update_customer_success(self):
        payload = {"name": "Jane Updated"}
        headers = {"Authorization": f"Bearer {self.customer_token}"}
        response = self.client.put(f'/customers/{self.customer_id}', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Jane Updated")

    def test_update_customer_forbidden_other_account(self):
        payload = {"name": "Hacker Update"}
        headers = {"Authorization": f"Bearer {self.other_customer_token}"}
        response = self.client.put(f'/customers/{self.customer_id}', json=payload, headers=headers)
        self.assertEqual(response.status_code, 403)

    # --- DELETE CUSTOMER BY ID ---
    def test_delete_customer_success(self):
        headers = {"Authorization": f"Bearer {self.customer_token}"}
        response = self.client.delete(f'/customers/{self.customer_id}', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_customer_forbidden_other_account(self):
        headers = {"Authorization": f"Bearer {self.other_customer_token}"}
        response = self.client.delete(f'/customers/{self.customer_id}', headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_delete_customer_missing_token(self):
        response = self.client.delete(f'/customers/{self.customer_id}')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()