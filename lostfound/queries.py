from django.contrib.auth import get_user_model
from django.db.models import Count, Q

from .models import Item

User = get_user_model()


def items_with_most_claims():
    """Items that have at least one claim, most-claimed first."""
    return (
        Item.objects.annotate(claim_count=Count("claims"))
        .filter(claim_count__gt=0)
        .order_by("-claim_count", "title")
    )


def most_active_users():
    """Users ranked by how many items they reported plus comments they wrote."""
    return (
        User.objects.annotate(
            reported=Count("reported_items", distinct=True),
            commented=Count("comments", distinct=True),
        )
        .annotate(activity=Count("reported_items", distinct=True) + Count("comments", distinct=True))
        .order_by("-activity")[:3]
    )


def open_items_with_pending_claims():
    """Lost or found items that still have a pending claim waiting for review."""
    return (
        Item.objects.filter(status__in=[Item.Status.LOST, Item.Status.FOUND])
        .filter(claims__status="pending")
        .distinct()
    )