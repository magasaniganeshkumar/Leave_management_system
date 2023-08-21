import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Employee_Detail
from django.contrib.auth.models import User

class EmployeeAPITest(APITestCase):

    def setUp(self):
        # self.user = User.objects.create_user(username='testuser', password='testpass')
        # self.client.login(username='testuser', password='testpass')

        random_name = self.generate_random_name() + str(random.randint(1000, 9999))
        random_email = self.generate_random_email() + str(random.randint(1000, 9999))
        random_phone = self.generate_random_phone()

        self.employee_data = {
            # "Employee_Name": random_name,
            "Primary_Phone": random_phone,
            "Email": random_email,
            "password": f"RandomPass{random.randint(1000, 9999)}",
            
        }
        self.employee = Employee_Detail.objects.create(**self.employee_data)

    def generate_random_name(self):
        first_names = ["Ganesh", "Sai", "Babu", "Balaji", "Mahesh"]
        last_names = ["Magasani", "Babu", "Sai", "Reddy", "Kumar"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"

    def generate_random_phone(self):
        return random.choice(["9", "8"]) + ''.join([str(random.randint(0, 9)) for _ in range(9)])

    def generate_random_email(self):
        usernames = ["ganesh123", "ganeshuser", "ganeshmname"]
        return f"{random.choice(usernames)}@gmail.com"

    def test_create_employee(self):
        print("Employee data:", self.employee_data)
        response = self.client.post(reverse('displayemployeeapi'), self.employee_data, format='json')
        print("Response reate_employee status code:", response.status_code)
        print("Response reate_employee data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee_Detail.objects.count(), 2)
        self.assertEqual(response.data['Employee_Name'], self.employee_data['Employee_Name'])
        print("Employee creation API test passed.")



    def test_get_employee_list(self):
        response = self.client.get(reverse('displayemployeeapi'))
        print("Response get_employee_list status code:", response.status_code)
        print("Response get_employee_list data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['Employee_Detail']), Employee_Detail.objects.count())
        print("Employee list access test passed.")

    def test_get_employee_detail(self):
        response = self.client.get(reverse('update', args=[self.employee.id]))
        print("Response get_employee_detail status code:", response.status_code)
        print("Response get_employee_detail data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Employee_Detail']['Employee_Name'], self.employee_data['Employee_Name'])
        print("Employee detail retrieval test passed.")

    def test_update_employee(self):
        updated_data = {
            "Employee_Name": "Updated Employee",
            "Primary_Phone": "9876543910",
            "Email": "updated@example.com",
            "password": "UpdatedTest001@1234",
            
        }
        response = self.client.put(reverse('update', args=[self.employee.id]), updated_data, format='json')
        print("Response update_employee status code:", response.status_code)
        print("Response update_employee data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.Employee_Name, updated_data['Employee_Name'])
        print("Employee update API test passed.")

    def test_delete_employee(self):
        response = self.client.delete(reverse('update', args=[self.employee.id]))
        print("Response delete_employee status code:", response.status_code)
        print("Response delete_employee data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee_Detail.objects.count(), 0)
        print("Employee deletion API test passed.")
