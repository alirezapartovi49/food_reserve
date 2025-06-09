from datetime import date, timedelta
import json

from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse

from food.models import Food, FoodDate, PredefinedFood
from accounts.tests import FullFlowAccountTest
from accounts.models import Student, Self
from reserve.models import Reserve

User = get_user_model()


class ReserveTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test user and get auth token
        account_test = FullFlowAccountTest()
        account_test.client = self.client
        account_test.create_user()
        account_test.login()

        self.user_data = account_test.user_data
        del self.user_data["refresh"]
        del self.user_data["access"]
        del self.user_data["token"]
        self.user = User(**self.user_data)
        self.auth_header = account_test.auth_header

        # Create test data
        today = date.today()
        self.food_date = FoodDate.objects.create(date=today + timedelta(days=1))
        self.predefined_food = PredefinedFood.objects.create(
            name="Test Food", food_type="pl", description="Test description"
        )
        self.food = Food.objects.create(
            food_date=self.food_date,
            predefined_food=self.predefined_food,
            food_type="pl",
        )

        # create self
        self.uni_self = Self.objects.create(
            name="شمسی پور", code="bhdbchb4", address="تهران محله دماوند"
        )  # univercity_self

        # Create student record
        self.student = Student.objects.create(
            user=self.user, has_dormitory=True, university=self.uni_self
        )

    def test_create_reserve(self):
        url = reverse("reserves-list")
        data = {"food": self.food.id, "date": self.food_date.date.isoformat()}

        response = self.client.post(url, data, format="json", headers=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reserve.objects.count(), 1)

        # Verify user is automatically set
        reserve = Reserve.objects.first()
        self.assertEqual(reserve.user, self.user)

    def test_create_reserve_invalid_food_date(self):
        url = reverse("reserves-list")
        invalid_date = date.today() + timedelta(days=2)
        data = {
            "food": self.food.id,
            "date": invalid_date.isoformat(),  # Food not available on this date
        }

        response = self.client.post(url, data, format="json", headers=self.auth_header)
        data: dict = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("تاریخ انتخابی", str(data))

    def test_reserve_limit_for_dormitory_student(self):
        # First reserve should succeed
        data = {"food": self.food.id, "date": self.food_date.date.isoformat()}
        response = self.client.post(
            reverse("reserves-list"), data, format="json", headers=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create second food option
        food2 = Food.objects.create(
            food_date=self.food_date,
            predefined_food=self.predefined_food,
            food_type="br",
        )

        # Second reserve should succeed for dormitory student
        data["food"] = food2.id
        response = self.client.post(
            reverse("reserves-list"), data, format="json", headers=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Third reserve should fail
        food3 = Food.objects.create(
            food_date=self.food_date,
            predefined_food=self.predefined_food,
            food_type="di",
        )
        data["food"] = food3.id
        response = self.client.post(
            reverse("reserves-list"), data, format="json", headers=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("انتخاب های روزانه", str(response.data))

    def test_reserve_limit_for_non_dormitory_student(self):
        # Update student to non-dormitory
        self.student.has_dormitory = False
        self.student.save()

        # First reserve should succeed
        data = {"food": self.food.id, "date": self.food_date.date.isoformat()}
        response = self.client.post(
            reverse("reserves-list"), data, format="json", headers=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Second reserve should fail
        food2 = Food.objects.create(
            food_date=self.food_date,
            predefined_food=self.predefined_food,
            food_type="br",
        )
        data["food"] = food2.id
        response = self.client.post(
            reverse("reserves-list"), data, format="json", headers=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_reserves_with_date_filter(self):
        # Create test reserves
        reserve1 = Reserve.objects.create(
            user=self.user, food=self.food, date=self.food_date.date
        )

        # Create reserve for next week (outside filter range)
        next_week_date = self.food_date.date + timedelta(days=7)
        next_week_food_date = FoodDate.objects.create(date=next_week_date)
        next_week_food = Food.objects.create(
            food_date=next_week_food_date,
            predefined_food=self.predefined_food,
            food_type="pl",
        )
        reserve2 = Reserve.objects.create(
            user=self.user, food=next_week_food, date=next_week_date
        )

        # Test without filter - should return all reserves
        response = self.client.get(reverse("reserves-list"), headers=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Test with date filter - should only return reserve from this week
        response = self.client.get(
            reverse("reserves-list") + f"?start-date={self.food_date.date.isoformat()}",
            headers=self.auth_header,
        )
        data = response.data  # Using response.data instead of json.loads

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(data),
            1,
            f"Expected 1 reserve, got {len(data)}. "
            f"Filtered for week starting {self.food_date.date}, "
            f"but got reserves for dates: {[r['date'] for r in data]}",
        )
        self.assertEqual(data[0]["id"], reserve1.id)

    def test_today_view_without_reserves(self):
        response = self.client.get(reverse("today-reserves"), headers=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        # Test create
        url = reverse("reserves-list")
        data = {"food": self.food.id, "date": self.food_date.date.isoformat()}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test list
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test today view
        response = self.client.get(reverse("today-reserves"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
