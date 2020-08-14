from django.contrib import admin
from .models import Role , Student, Employee, Study, Thesis, Notification,MemberOfThesisComitee

# Register your models here.
admin.site.register(Role)
admin.site.register(Student)
admin.site.register(Employee)
admin.site.register(Study)
admin.site.register(Thesis)
admin.site.register(Notification)
admin.site.register(MemberOfThesisComitee)


