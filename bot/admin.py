from django.contrib import admin
from .models import UserProfile, Product, Order, Preference, Question, Contacts, ContactsLink


class ContactsLinkInline(admin.TabularInline):
    model = ContactsLink

class ContactsAdmin(admin.ModelAdmin):
    inlines = [ContactsLinkInline]


admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Preference)
admin.site.register(Question)
admin.site.register(Contacts, ContactsAdmin)
