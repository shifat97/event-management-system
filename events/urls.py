from django.urls import path
from events.views import create_event, update_event, create_perticipant, update_perticipant

urlpatterns = [
    path('create-event/', create_event, name="create-event"),
    path('update-event/', update_event, name="update-event"),
    path('create_perticipant/', create_perticipant, name="create-perticipant"),
    path('update-perticipant/', update_perticipant, name="update-perticipant"),
]
