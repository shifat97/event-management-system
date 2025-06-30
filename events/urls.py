from django.urls import path
from events.views import create_event, update_event, create_perticipant, update_perticipant

urlpatterns = [
    path('create-event/', create_event, name="create-event"),
    path('update-event/', update_event, name="update-event"),
    path('register-participant/', create_perticipant, name="register-participant"),
    path('update-participant/', update_perticipant, name="update-participant"),
]
