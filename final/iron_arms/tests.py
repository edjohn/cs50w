from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase, Client
from django.urls import reverse
from .models import Equipment, Review
from .urls import urlpatterns
from webdriver_manager.chrome import ChromeDriverManager

# Create your tests here.
class WebpageTestCase(LiveServerTestCase):

    urls = ['index', 'contact', 'location', 'equipment']

    def setUp(self):
        self.client = Client()

    def testStatusCodes(self):
        for url in self.urls:
            response = self.client.get(reverse(url))
            self.assertEqual(response.status_code, 200)


class EquipmentTestCase(LiveServerTestCase):

    EQUIPMENT_COUNT = 5

    def setUp(self):
        self.equipment = []
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.implicitly_wait(5)

        for i in range(self.EQUIPMENT_COUNT):
            name = f'SampleEquipment{i}'
            description = f'This is a sample description for SampleEquipment{i}'
            image = 'equipment/sample.png'
            self.equipment.append(Equipment.objects.create(name=name, description=description, image=image))

    def test_equipment_count(self):
        self.assertEqual(Equipment.objects.all().count(), self.EQUIPMENT_COUNT)
    
    def test_equipment_display(self):
        self.driver.get(f'{self.live_server_url}/equipment')
        equipment = self.driver.find_elements(By.CLASS_NAME, 'equipment')
        self.assertEqual(len(equipment), self.EQUIPMENT_COUNT)


class ReviewTestCase(LiveServerTestCase):

    REVIEW_COUNT = 5

    def setUp(self):
        self.reviews = []
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.implicitly_wait(5) 

        for i in range(self.REVIEW_COUNT):
            user = f'User{i}'
            description = f'This is a description from User{i}'
            stars = 5
            self.reviews.append(Review.objects.create(user=user, description=description, stars=stars))

    def test_review_count(self):
        self.assertEqual(Review.objects.all().count(), self.REVIEW_COUNT)
    
    def test_review_display(self):
        self.driver.get(f'{self.live_server_url}')
        reviews = self.driver.find_elements(By.CLASS_NAME, 'review')
        self.assertEqual(len(reviews), self.REVIEW_COUNT)
