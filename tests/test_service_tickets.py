import unittest
from decimal import Decimal
from app import create_app
from app.models import db, Customer, Mechanic, Inventory, Service_Ticket
from app.utils.util import encode_token

class TestServiceTicket(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # Seed customer, mechanics, and parts
            self.customer = Customer(
                name="John Doe",
                email="john@email.com",
                password="password123",
                phone="555-111-2222"
            )
            self.mechanic1 = Mechanic(
                name="Bob Wrench",
                email="bob@email.com",
                password="password123",
                phone="555-333-4444",
                salary=Decimal("60000.00")
            )
            self.mechanic2 = Mechanic(
                name="Dave Tool",
                email="dave@email.com",
                password="password123",
                phone="555-555-6666",
                salary=Decimal("62000.00")
            )
            self.part = Inventory(
                name="Spark Plug",
                price=9.99
            )

            db.session.add_all([self.customer, self.mechanic1, self.mechanic2, self.part])
            db.session.commit()

            self.customer_id = self.customer.id
            self.mechanic1_id = self.mechanic1.id
            self.mechanic2_id = self.mechanic2.id
            self.part_id = self.part.id

            # Seed initial service ticket
            self.ticket = Service_Ticket(
                VIN="1FA6P8CF5H5000000",
                service_date="2026-08-15",
                service_desc="Transmission Inspection",
                customer_id=self.customer_id
            )
            db.session.add(self.ticket)
            db.session.commit()
            self.ticket_id = self.ticket.id

        self.client = self.app.test_client()
        self.customer_token = encode_token(self.customer_id, 'customer')
        self.mechanic_token = encode_token(self.mechanic1_id, 'mechanic')

    # --- CREATE SERVICE TICKET ---
    def test_create_service_ticket_success(self):
        payload = {
            "VIN": "1HGCR2F83HA999999",
            "service_date": "2026-08-20",
            "service_desc": "Brake Replacement",
            "customer_id": self.customer_id
        }
        response = self.client.post('/service-tickets/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['VIN'], "1HGCR2F83HA999999")

    def test_create_service_ticket_missing_field(self):
        payload = {
            "VIN": "1HGCR2F83HA999999",
            "service_desc": "Missing date and customer"
        }
        response = self.client.post('/service-tickets/', json=payload)
        self.assertEqual(response.status_code, 400)

    # --- GET ALL SERVICE TICKETS ---
    def test_get_all_service_tickets(self):
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertTrue(len(response.json) >= 1)

    # --- GET SINGLE SERVICE TICKET ---
    def test_get_single_service_ticket_success(self):
        response = self.client.get(f'/service-tickets/{self.ticket_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['VIN'], "1FA6P8CF5H5000000")

    def test_get_single_service_ticket_not_found(self):
        response = self.client.get('/service-tickets/9999')
        self.assertEqual(response.status_code, 404)

    # --- ASSIGN MECHANIC TO SERVICE TICKET ---
    def test_assign_mechanic_success(self):
        response = self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic1_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("successfully assigned", response.json['message'])

    def test_assign_mechanic_already_assigned(self):
        # Assign mechanic first
        self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic1_id}')
        
        # Attempt assigning the same mechanic again
        response = self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic1_id}')
        self.assertEqual(response.status_code, 400)
        self.assertIn("already assigned", response.json['message'])

    # --- REMOVE MECHANIC FROM SERVICE TICKET ---
    def test_remove_mechanic_success(self):
        # Assign first so there is a mechanic to remove
        self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic1_id}')

        response = self.client.put(f'/service-tickets/{self.ticket_id}/remove-mechanic/{self.mechanic1_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("successfully removed", response.json['message'])

    def test_remove_mechanic_not_assigned(self):
        response = self.client.put(f'/service-tickets/{self.ticket_id}/remove-mechanic/{self.mechanic2_id}')
        self.assertEqual(response.status_code, 400)
        self.assertIn("not assigned", response.json['message'])

    # --- EDIT TICKET MECHANICS (BULK ADD / REMOVE) ---
    def test_edit_ticket_mechanics_bulk(self):
        # Pre-assign mechanic 1
        self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic1_id}')

        payload = {
            "add_ids": [self.mechanic2_id],
            "remove_ids": [self.mechanic1_id]
        }
        response = self.client.put(f'/service-tickets/{self.ticket_id}/edit', json=payload)
        self.assertEqual(response.status_code, 200)

    # --- ADD PART TO SERVICE TICKET ---
    def test_add_part_success(self):
        headers = {"Authorization": f"Bearer {self.mechanic_token}"}
        response = self.client.put(f'/service-tickets/{self.ticket_id}/add-part/{self.part_id}', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_add_part_unauthorized_role(self):
        headers = {"Authorization": f"Bearer {self.customer_token}"}
        response = self.client.put(f'/service-tickets/{self.ticket_id}/add-part/{self.part_id}', headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_add_part_duplicate(self):
        headers = {"Authorization": f"Bearer {self.mechanic_token}"}
        # Add the part once
        self.client.put(f'/service-tickets/{self.ticket_id}/add-part/{self.part_id}', headers=headers)
        
        # Add the same part again
        response = self.client.put(f'/service-tickets/{self.ticket_id}/add-part/{self.part_id}', headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn("already added", response.json['message'])

if __name__ == '__main__':
    unittest.main()