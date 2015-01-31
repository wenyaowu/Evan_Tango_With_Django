from django.contrib import admin
from rango.models import Category, Page
# Register your models here.

# Auto-populate the slug field in the admin interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page)