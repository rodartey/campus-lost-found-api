from django.contrib import admin

from .models import Claim, Comment, Item


class ClaimInline(admin.TabularInline):
    model = Claim
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "location", "reported_by", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "description", "location")
    filter_horizontal = ("watchers",)
    inlines = [ClaimInline, CommentInline]


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ("item", "claimant", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("item__title", "claimant__username")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("item", "author", "created_at")
    search_fields = ("text", "author__username")