from django.contrib import admin
from .models import Blog, Contact, Education, Personnel, Works, WorksCategory

# Register your models here.

class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('name',)

class EducationAdmin(admin.ModelAdmin):
    list_display = ("name", "school", "degree", "section", "graduation")

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name',"mail","phone_number")

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title',"publish_date")

class WorksCategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)

class WorksAdmin(admin.ModelAdmin):
    list_display = ('title',"publish_date")

admin.site.register(Personnel, PersonnelAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Works, WorksAdmin)
admin.site.register(WorksCategory, WorksCategoryAdmin)