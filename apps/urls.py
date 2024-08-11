from django.urls import path, include

urlpatterns = [
    path('', include("apps.core.urls")),
    path('words/', include("apps.words.urls")),
    path('telegram-users/', include("apps.telegram_users.urls")),
    path('categories/', include("apps.categories.urls")),
]
