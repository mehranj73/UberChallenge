from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
import base64
import json
User = get_user_model()


PASSWORD = "passwOrd"


def create_user(username, password, first_name, last_name):
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    user.save()
    return user


class AccountsTests(APITestCase):
    def test_can_create_account(self):
        #CREATING THE USER VIA SIGNUP
        url = reverse("signup")
        data = {
            "username" : "test@test.com",
            "password1" : PASSWORD,
            "password2" : PASSWORD,
            "first_name" : "test",
            "last_name" : "test_man",
            "group" : "RIDER"
        }
        response = self.client.post(url, data, format="json")
        #GETTING USER, LAST
        last_user = User.objects.last()
        #ASSERTING
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["group"], data["group"])
        self.assertEqual(response.data["username"], last_user.username)
        self.assertEqual(response.data["first_name"], last_user.first_name)
        self.assertIsNotNone(last_user.password)

    def test_can_retrieve_pair_token(self):
        user = create_user(
            "test@test.com",
            PASSWORD,
            "test1",
            "test2"
        )

        url = reverse("login")
        response = self.client.post(url, {"username": user.username, "password" : PASSWORD}, format="json")
        last_user = User.objects.last()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        #Open Token Payload
        access_token = response.data["access"]
        encoded_token = access_token.split(".")[1]
        decoded_token = json.loads(base64.b64decode(encoded_token + "==="))
        self.assertEqual(decoded_token["user_id"], last_user.id)
        self.assertEqual(decoded_token["username"], last_user.username)
