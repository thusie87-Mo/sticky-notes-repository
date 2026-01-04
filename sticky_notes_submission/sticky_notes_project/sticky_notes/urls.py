from django.urls import path, include

urlpatterns = [
    path('', include('notes.urls')),  # include your app's URLs
]
