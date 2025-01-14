from django.contrib import admin
from .models import User, Event, NewsLetter, Ticket, Registration, Gallery, Blog, Comment, Contact, ContactInfo

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'category', 'uploaded_at')
    list_filter = ('media_type', 'category')
    search_fields = ('title',)


# Register your models here.
admin.site.register(User)
admin.site.register(Event)
admin.site.register(NewsLetter)
admin.site.register(Ticket)
admin.site.register(Registration)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(ContactInfo)
admin.site.register(Contact)