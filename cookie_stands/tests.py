# from django.test import TestCase
#
# # Create your tests here.
#
# class CookieStandsTests(TestCase):
#     # TODO: test your app
#     def test_your_app(self):
#         self.assertEqual("I have many tests", "I have no tests")
#
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import CookieStand


class CookieStandTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_cookie_stand = CookieStand.objects.create(
            location="seattle",
            owner=testuser1,
            description="Better for collecting leaves than a shovel.",
        )
        test_cookie_stand.save()

    def setUp(self):
        self.client.login(username="testuser1", password="pass")

    def test_cookie_stands_model(self):
        cookie_stand = CookieStand.objects.get(id=1)
        actual_owner = str(cookie_stand.owner)
        actual_location = str(cookie_stand.location)
        actual_description = str(cookie_stand.description)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_location, "seattle")
        self.assertEqual(
            actual_description, "Better for collecting leaves than a shovel."
        )

    def test_get_cookie_stand_list(self):
        url = reverse("cookie_stand_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cookie_stands = response.data
        self.assertEqual(len(cookie_stands), 1)
        self.assertEqual(cookie_stands[0]["location"], "seattle")

    def test_get_cookie_stand_by_id(self):
        url = reverse("cookie_stand_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cookie_stand = response.data
        self.assertEqual(cookie_stand["location"], "seattle")

    def test_create_cookie_stand(self):
        url = reverse("cookie_stand_list")
        data = {"owner": 1, "location": "seattle", "description": "good for cereal and soup"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cookie_stands = CookieStand.objects.all()
        self.assertEqual(len(cookie_stands), 2)
        self.assertEqual(CookieStand.objects.get(id=2).location, "seattle")

    def test_update_cookie_stand(self):
        url = reverse("cookie_stand_detail", args=(1,))
        data = {
            "owner": 1,
            "location": "seattle",
            "description": "pole with a crossbar toothed like a comb.",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cookie_stand = CookieStand.objects.get(id=1)
        self.assertEqual(cookie_stand.location, data["location"])
        self.assertEqual(cookie_stand.owner.id, data["owner"])
        self.assertEqual(cookie_stand.description, data["description"])

    def test_delete_cookie_stand(self):
        url = reverse("cookie_stand_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        cookie_stands = CookieStand.objects.all()
        self.assertEqual(len(cookie_stands), 0)

    def test_authentication_required(self):
        self.client.logout()
        url = reverse("cookie_stand_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
