from django.contrib import admin
from .models import Immobilier, Reservation, Notification

class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0
    readonly_fields = ('user', 'created_at')

@admin.register(Immobilier)
class ImmobilierAdmin(admin.ModelAdmin):
    list_display = ('titre', 'prix', 'disponible', 'reservation_count', 'date_ajout')
    list_editable = ('disponible',)
    list_filter = ('disponible',)
    search_fields = ('titre', 'adresse')
    inlines = [ReservationInline]  
    
    def reservation_count(self, obj):
        return obj.reserved_by.count()
    reservation_count.short_description = 'Réservations'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'seen', 'created_at')
    list_filter = ('seen', 'created_at')
    actions = ['mark_as_seen']
    
    def mark_as_seen(self, request, queryset):
        queryset.update(seen=True)
    mark_as_seen.short_description = "Mark selected notifications as seen"

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'immobilier', 'created_at', 'notification_status')
    
    def notification_status(self, obj):
        return obj.notification.seen
    notification_status.boolean = True
    notification_status.short_description = 'Notification Seen'

