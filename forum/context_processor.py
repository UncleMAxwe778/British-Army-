from .models import MessageList


def notifications_processor(request):
    if request.user.is_authenticated:
        notifications = (
            MessageList.objects
            .filter(receiver=request.user, is_read=False)
            .only("id", "name_message", "data_giving")
        )

        return {
            "global_notifications": notifications[:5],
            "notifications_count": notifications.count(),
        }


    return {
        "global_notifications": [],
        "notifications_count": 0,
    }
