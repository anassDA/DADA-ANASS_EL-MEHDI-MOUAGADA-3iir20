from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(reservation__user=request.user, seen=False)
    else:
        notifications = Notification.objects.none()
    return {
        'notifications': notifications
    }