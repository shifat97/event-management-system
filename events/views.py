from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.forms import EventModelForm, CategoryModelForm
from django.contrib import messages

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
        event_model_form = EventModelForm(prefix="event")
        category_model_form = CategoryModelForm(prefix="category")

    context = {
        'event_form': event_model_form,
        'category_form': category_model_form,
    }

    return render(request, 'pages/create-event.html', context=context)

def update_event():
    pass

def create_perticipant():
    pass

def update_perticipant():
    pass