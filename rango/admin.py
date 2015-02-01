from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile
# Register your models here.


# Auto-populate the slug field in the admin interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ('name', 'views', 'likes')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page)
admin.site.register(UserProfile)