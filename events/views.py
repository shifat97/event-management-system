from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.forms import EventModelForm, CategoryModelForm, ParticipantModelForm
from events.models import Event
from django.contrib import messages
from django.db.models import Count

# Create your views here.

# Create event
def create_event(request):
    if request.method == 'POST':
        event_model_form = EventModelForm(request.POST, prefix="event")
        category_model_form = CategoryModelForm(request.POST, prefix="category")

        if event_model_form.is_valid() and category_model_form.is_valid():
            category_instance = category_model_form.save()
            
            event_instance = event_model_form.save(commit=False)
            event_instance.category = category_instance
            event_instance.save()

            event_model_form.save_m2m()

            messages.success(request, 'Event created successfully')

            return redirect('create-event')

        else:
            messages.error(request, 'Something went wrong! Check your inputs')

    else:
        event_model_form = EventModelForm(prefix="event")
        category_model_form = CategoryModelForm(prefix="category")

    context = {
        'event_form': event_model_form,
        'category_form': category_model_form,
    }

    return render(request, 'pages/create-event.html', context=context)

def update_event():
    pass

def view_events(request):
    events = Event.objects.select_related('category').prefetch_related('registered_event').annotate(total_participants=Count('registered_event')).all()

    return render(request, 'pages/view-all-events.html', context={
        'events': events,
    })

# Event details
def view_event_details(request, id):
    event = Event.objects.get(id=id)

    similar_events = (
        Event.objects
        .filter(date=event.date)
        .exclude(id=event.id)
        .select_related('category')
        .prefetch_related('registered_event')
    )

    print(event.date)
    print(Event.objects.filter(date=event.date).exclude(id=event.id).exists())


    return render(request, 'pages/view-event-details.html', context={
        'event': event,
        'similar_events': similar_events,
    })

# Create Perticipant
def create_perticipant(request):
    if request.method == 'POST':
        participant_model_form = ParticipantModelForm(request.POST)

        if participant_model_form.is_valid():
            participant_model_form.save();
            messages.success(request, 'Registration Successful')
            
            return redirect('create-participant')
    else:
        participant_model_form = ParticipantModelForm()
    
    return render(request, 'pages/create-participant.html', {
        'participant_form': participant_model_form
    })

def update_perticipant():
    pass