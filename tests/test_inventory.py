import unittest
from app import create_app
from app.models import db, Inventory
from app.utils.util import encode_token

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            # Seed initial test inventory item
            self.item = Inventory(name="Oil Filter", price=12.99)
            db.session.add(self.item)
            db.session.commit()
            self.item_id = self.item.id

        self.client = self.app.test_client()
        # Tokens using (user_id, role)
        self.mechanic_token = encode_token(1, 'mechanic')
        self.customer_token = encode_token(1, 'customer')
        
    # --- CREATE INVENTORY ITEM ---
    def test_create_inventory_success(self):
        payload = {"name": "Brake Pads", "price": 45.50}
        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Brake Pads")

    def test_create_inventory_duplicate(self):
        payload = {"name": "Oil Filter", "price": 12.99}
        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 200)
        
    # --- GET ALL INVENTORY ---
    def test_get_all_inventory(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertTrue(len(response.json) >= 1)
        
    # --- GET SINGLE INVENTORY ITEM ---
    def test_get_single_inventory(self):
        response = self.client.get(f'/inventory/{self.item_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Oil Filter")

    def test_get_single_inventory_not_found(self):
        response = self.client.get('/inventory/9999')
        self.assertEqual(response.status_code, 404)
    
    # --- UPDATE INVENTORY ITEM ---
    def test_update_inventory_success(self):
        payload = {"name": "Premium Oil Filter", "price": 15.99}
        headers = {"Authorization": f"Bearer {self.mechanic_token}"}
        response = self.client.put(f'/inventory/{self.item_id}', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Premium Oil Filter")

    def test_update_inventory_unauthorized_role(self):
        payload = {"name": "Unauthorized Change"}
        headers = {"Authorization": f"Bearer {self.customer_token}"}
        response = self.client.put(f'/inventory/{self.item_id}', json=payload, headers=headers)
        self.assertEqual(response.status_code, 403)

    # --- DELETE INVENTORY ITEM ---
    def test_delete_inventory_success(self):
        headers = {"Authorization": f"Bearer {self.mechanic_token}"}
        response = self.client.delete(f'/inventory/{self.item_id}', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_inventory_forbidden(self):
        headers = {"Authorization": f"Bearer {self.customer_token}"}
        response = self.client.delete(f'/inventory/{self.item_id}', headers=headers)
        self.assertEqual(response.status_code, 403)
        
if __name__ == '__main__':
    unittest.main()