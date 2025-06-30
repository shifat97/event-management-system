from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.forms import EventModelForm, CategoryModelForm, ParticipantModelForm
from events.models import Event, Category, Participant
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
from django.db.models import Q

def create_participant(request, id):
    event = Event.objects.get(id=id)

    if request.method == 'POST':
        participant_form = ParticipantModelForm(request.POST)
        if participant_form.is_valid():
            email = participant_form.cleaned_data['participant_email']
            name = participant_form.cleaned_data['participant_name']

            participant, created = Participant.objects.get_or_create(
                participant_email=email,
                participant_name=name,
            )

            if event in participant.registered_event.all():
                messages.warning(request, 'You are already registered for this event.')
            else:
                participant.registered_event.add(event)
                messages.success(request, 'Registration Successful!')
    else:
        participant_form = ParticipantModelForm()

    return render(request, 'pages/create-participant.html', {
        'participant_form': participant_form,
        'event': event,
    })


def view_participant(request):
    participants = Participant.objects.prefetch_related('registered_event').all()

    return render(request, 'pages/view-participants.html', {'participants': participants})

def update_participant(request, id):
    participant = Participant.objects.get(id=id)

    if request.method == 'POST':
        participant_form = ParticipantModelForm(request.POST, instance=participant)

        if participant_form.is_valid():
            participant_form.save()
            messages.success(request, 'Update successful')
        else:
            messages.error(request, 'Something went wrong! Try again later')
    else:
        participant_form = ParticipantModelForm(instance=participant)

    return render(request, 'pages/update-participant.html', {
        'participant_form': participant_form
    })

def delete_participant(request, id):
    if request.method == 'POST':
        participant = Participant.objects.get(id=id)
        participant.delete()
        
        return redirect('view-participants')
    else:
        return redirect('view-participants')

