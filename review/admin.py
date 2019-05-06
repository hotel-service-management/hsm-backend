from django.contrib import admin

from review.models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'score', 'title', 'description', 'booking']
    list_filter = ['score']
    list_per_page = 10

    search_fields = ['title']


admin.site.register(Review, ReviewAdmin)
