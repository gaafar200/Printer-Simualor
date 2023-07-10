import json
import pytest
from app import app  # Import the Flask application object

class TestPrinter:
    

    def setup_method(self, method):
        app.config['TESTING'] = True
        self.client = app.test_client()


    def test_print_job_submission(self):
        with app.test_client() as client:
            data = {"text": "mahmoud"}
            response = client.post('/print', data=data, follow_redirects=True)
            assert response.status_code == 200
            response_dict = json.loads(response.data)
            assert b'Print Request Processed SucessFully' in response.data
            key = response_dict["key"]
            response = client.get("/printingTasks")
            response_dict = json.loads(response.data)
            found = False
            for item in response_dict['printingQueue']:
                if item['key'] == key:
                    found = True
                    break
            assert found, "print Task doesn't exist in printing Queue"



    def test_printer_status(self):
        # Printer initial state
        status = self.get_status()
        assert status == "idle"

        # Printer paused state
        response = self.client.post("/pause")
        assert response.status_code == 200
        assert b'paused Successfully' in response.data
        status = self.get_status()
        assert status == "Paused"

        # Printer offline state
        response = self.client.post("/offline")
        assert response.status_code == 200
        assert b'printer is now offline' in response.data.lower()
        status = self.get_status()
        assert status == 'offLine'

        # Printer back online (get last state)
        response = self.client.post("/online")
        assert response.status_code == 200
        assert b'printer is now online' in response.data.lower()
        status = self.get_status()
        assert status == 'Paused'

        # Printer resume state
        response = self.client.post("/resume")
        assert response.status_code == 200
        assert b'Resumed Successfully' in response.data
        status = self.get_status()
        assert status == 'idle'

    def get_status(self):
        response = self.client.get("status")
        assert response.status_code == 200
        response_dict = json.loads(response.data)
        return response_dict["status"]        