from django.urls import path
from events.views import create_event, update_event, view_events, view_event_details, delete_event, create_participant, view_participant, update_participant
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('create-event/', create_event, name="create-event"),
    path('update-event/<int:id>', update_event, name="update-event"),
    path('view-all-events/', view_events, name='view-events'),
    path('view-event-details/<int:id>/', view_event_details, name='view-event-details'),
    path('delete-event/<int:id>', delete_event, name='delete-event'),
    path('register-participant/event-id=<int:id>', create_participant, name='register-participant'),
    path('view-participants/', view_participant, name='view-participants'),
    path('update-participant/<int:id>', update_participant, name='update-participant'),
] + debug_toolbar_urls()
