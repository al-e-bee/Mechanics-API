import unittest
from decimal import Decimal
from app import create_app
from app.models import db, Mechanic, Customer, Service_Ticket
from app.utils.util import encode_token

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # Seed a customer and test mechanic
            self.customer = Customer(
                name="Customer Test",
                email="cust@email.com",
                password="password123",
                phone="555-000-1111"
            )
            self.mechanic = Mechanic(
                name="Mike Fixit",
                email="mike@email.com",
                password="password123",
                phone="555-444-3333",
                salary=Decimal("65000.00")
            )
            db.session.add_all([self.customer, self.mechanic])
            db.session.commit()

            self.mechanic_id = self.mechanic.id
            self.customer_id = self.customer.id

            # Seed a service ticket assigned to the mechanic for top-performers check
            self.ticket = Service_Ticket(
                VIN="1HGCR2F83HA123456",
                service_date="2026-08-15",
                service_desc="Brake Repair",
                customer_id=self.customer_id
            )
            self.ticket.mechanics.append(self.mechanic)
            db.session.add(self.ticket)
            db.session.commit()

        self.client = self.app.test_client()
        self.mechanic_token = encode_token(self.mechanic_id, 'mechanic')
        self.other_mechanic_token = encode_token(999, 'mechanic')
        self.customer_token = encode_token(self.customer_id, 'customer')

    # --- LOGIN MECHANIC ---
    def test_login_mechanic_success(self):
        payload = {
            "email": "mike@email.com",
            "password": "password123"
        }
        response = self.client.post('/mechanics/login', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertIn('token', response.json)

    def test_login_mechanic_invalid_credentials(self):
        payload = {
            "email": "mike@email.com",
            "password": "wrongpassword"
        }
        response = self.client.post('/mechanics/login', json=payload)
        self.assertEqual(response.status_code, 401)

    # --- CREATE MECHANIC ---
    def test_create_mechanic_success(self):
        payload = {
            "name": "Sarah Wrench",
            "email": "sarah@email.com",
            "password": "securepassword",
            "phone": "555-222-1111",
            "salary": 72000.00
        }
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Sarah Wrench")

    def test_create_mechanic_duplicate(self):
        payload = {
            "name": "Mike Clone",
            "email": "mike@email.com",
            "password": "password123",
            "phone": "555-999-8888",
            "salary": 65000.00
        }
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_create_mechanic_missing_field(self):
        payload = {
            "name": "Incomplete Mechanic",
            "email": "incomplete@email.com",
            "password": "password123"
        }
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 400)

    # --- GET ALL MECHANICS ---
    def test_get_all_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertTrue(len(response.json) >= 1)

    # --- GET TOP PERFORMING MECHANICS ---
    def test_get_top_mechanics(self):
        response = self.client.get('/mechanics/top-performers')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertTrue(len(response.json) >= 1)
        self.assertEqual(response.json[0]['name'], "Mike Fixit")

    # --- GET SINGLE MECHANIC ---
    def test_get_single_mechanic(self):
        response = self.client.get(f'/mechanics/{self.mechanic_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Mike Fixit")

    def test_get_single_mechanic_not_found(self):
        response = self.client.get('/mechanics/9999')
        self.assertEqual(response.status_code, 404)

    # --- UPDATE MECHANIC ---
    def test_update_mechanic_success(self):
        payload = {"name": "Mike Updated"}
        headers = {"Authorization": f"Bearer {self.mechanic_token}"}
        response = self.client.put(f'/mechanics/{self.mechanic_id}', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Mike Updated")

    def test_update_mechanic_forbidden_other_mechanic(self):
        payload = {"name": "Unauthorized Update"}
        headers = {"Authorization": f"Bearer {self.other_mechanic_token}"}
        response = self.client.put(f'/mechanics/{self.mechanic_id}', json=payload, headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_update_mechanic_forbidden_customer_role(self):
        payload = {"name": "Customer Attempting Update"}
        headers = {"Authorization": f"Bearer {self.customer_token}"}
        response = self.client.put(f'/mechanics/{self.mechanic_id}', json=payload, headers=headers)
        self.assertEqual(response.status_code, 403)

    # --- DELETE MECHANIC ---
    def test_delete_mechanic_success(self):
        headers = {"Authorization": f"Bearer {self.mechanic_token}"}
        response = self.client.delete(f'/mechanics/{self.mechanic_id}', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_mechanic_forbidden_other_mechanic(self):
        headers = {"Authorization": f"Bearer {self.other_mechanic_token}"}
        response = self.client.delete(f'/mechanics/{self.mechanic_id}', headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_delete_mechanic_missing_token(self):
        response = self.client.delete(f'/mechanics/{self.mechanic_id}')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()