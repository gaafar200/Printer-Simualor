import unittest
from app import app
import json
class TestPrinter(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()



    def test_print_job_submistion(self):
        with app.test_client() as client:
            data = {"text":"mahmoud"}
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
            assert found, "print Task doesn't exists in printing Queue"

    def test_printer_status(self):
        #printer initial State
        status = self.getStatus()
        assert status == "idle"
        #printer paused state
        response = self.client.post("/pause")
        assert response.status_code == 200
        assert b'paused Successfully' in response.data
        status = self.getStatus()
        assert status == "Paused"
        #printer offline state
        response = self.client.post("offline")
        assert response.status_code == 200
        assert b'Printer Is Now OffLine' in response.data
        status = self.getStatus()
        assert status == 'offLine'
        #printer back online (get Last State)
        response = self.client.post("online")
        assert response.status_code == 200
        assert b'printer Is Now Online' in response.data
        status = self.getStatus()
        assert status == 'Paused'
        #printer resume state
        response = self.client.post("/resume")
        assert response.status_code == 200
        assert b'Resumed Successfully' in response.data
        status = self.getStatus()
        assert status == 'idle'




    def getStatus(self):
        response = self.client.get("status")
        assert response.status_code == 200
        response_dict = json.loads(response.data)
        return response_dict["status"]