from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.forms import EventModelForm, CategoryModelForm, ParticipantModelForm
from events.models import Event, Category
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

def update_event(request, id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance=event)

    try:
        event_category = event.category
    except Category.DoesNotExist:
        event_category = None
    
    category_form = CategoryModelForm(instance=event_category)

    if request.method == 'POST':
        event_form = EventModelForm(request.POST, instance=event)
        category_form = CategoryModelForm(request.POST, instance=event_category)

        if event_form.is_valid() and category_form.is_valid():
            saved_category = category_form.save()

            updated_event = event_form.save(commit=False)
            updated_event.category = saved_category
            updated_event.save()

            messages.success(request, "Event updated successfully!")

        else:
            messages.error(request, "Something went wrong! Try again later")
    
    return render(request, 'pages/update-event.html', {
        'event_form': event_form,
        'category_form': category_form,
        'event': event,
    })

def view_events(request):
    events = Event.objects.select_related('category').prefetch_related('registered_event').annotate(total_participants=Count('registered_event')).all()

    return render(request, 'pages/view-all-events.html', context={
        'events': events,
    })

def delete_event(request, id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        
        messages.success(request, 'Event deleted successfully')
        return redirect('view-events')
    else:
        return redirect('view-events')

# Event details
def view_event_details(request, id):
    # event = Event.objects.get(id=id)
    event = Event.objects.prefetch_related('registered_event').get(id=id)

    similar_events = (
        Event.objects
        .filter(date=event.date)
        .exclude(id=event.id)
        .select_related('category')
    )

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