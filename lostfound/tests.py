from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Item

User = get_user_model()


class ItemAPITests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="pass12345")
        self.other = User.objects.create_user(username="other", password="pass12345")
        self.item = Item.objects.create(
            title="Black backpack",
            description="Black Jansport",
            location="Main Library",
            reported_by=self.owner,
        )

    def test_list_items_is_paginated(self):
        for i in range(6):
            Item.objects.create(
                title=f"Item {i}", location="Library", reported_by=self.owner
            )
        response = self.client.get("/api/items/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 7)
        self.assertEqual(len(response.data["results"]), 5)

    def test_create_item(self):
        payload = {
            "title": "Blue umbrella",
            "description": "Large umbrella",
            "location": "Science Block",
            "status": "found",
            "reported_by": self.owner.id,
        }
        response = self.client.post("/api/items/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)

    def test_create_item_with_short_title_fails(self):
        payload = {
            "title": "ab",
            "location": "Science Block",
            "reported_by": self.owner.id,
        }
        response = self.client.post("/api/items/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_cannot_claim_own_item(self):
        payload = {
            "item": self.item.id,
            "claimant": self.owner.id,
            "message": "This is definitely my backpack.",
        }
        response = self.client.post("/api/claims/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)