from rest_framework import viewsets

from .models import Claim, Comment, Item
from .serializers import ClaimSerializer, CommentSerializer, ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by("-created_at")
    serializer_class = ItemSerializer


class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all().order_by("-created_at")
    serializer_class = ClaimSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer