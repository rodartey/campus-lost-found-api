from rest_framework import serializers

from .models import Claim, Comment, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "title", "description", "location", "status",
                  "reported_by", "watchers", "created_at"]
        read_only_fields = ["created_at"]

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters.")
        return value


class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ["id", "item", "claimant", "message", "status", "created_at"]
        read_only_fields = ["created_at"]

    def validate_message(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters.")
        return value

    def validate(self, data):
        item = data.get("item")
        claimant = data.get("claimant")
        if item and claimant and item.reported_by == claimant:
            raise serializers.ValidationError("You cannot claim an item you reported.")
        return data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "item", "author", "text", "created_at"]
        read_only_fields = ["created_at"]

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment cannot be empty.")
        return value