from django import forms
from events.models import Event, Category, Participant

class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location']
        labels = {
            'name': '',
            'description': '',
            'location': '',
            'date': 'Select Event Date'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'px-4 py-4 rounded-md w-full bg-[#E6F0F0] focus:outline-none focus:border-none',
                'placeholder': 'e.g. Festival',
                'type': 'text',
            }),
            'description': forms.Textarea(attrs={
                'class': 'px-4 py-4 rounded-md w-full bg-[#E6F0F0] focus:outline-none focus:border-none',
                'placeholder': 'Describe about the event',
            }),
            'date': forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    'class': 'bg-[#E6F0F0] px-4 py-4 rounded-md',
                    'type': 'date',
                }, 
            ),
            'time': forms.TimeInput(attrs={
                'class': 'bg-[#E6F0F0] px-4 py-4 rounded-md',
                'type': 'time',
            }),
            'location': forms.TextInput(attrs={
                'class': 'px-4 py-4 rounded-md w-full bg-[#E6F0F0] focus:outline-none focus:border-none',
                'placeholder': 'Enter event location',
                'type': 'text',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%Y-%m-%d']

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']
        labels = {
            'category_name': 'Category',
        }
        widgets = {
            'category_name': forms.Select(attrs={
                'class': 'bg-[#E6F0F0] px-4 py-4 rounded-md border-r-[16px] border-[#E6F0F0]',
            }),
        }

class ParticipantModelForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['participant_name', 'participant_email']
        labels = {
            'participant_name': 'Your Full Name',
            'participant_email': 'Your Email Address',
        }
        widgets = {
            'participant_name': forms.TextInput(
                attrs = {
                    'class': 'px-4 py-4 rounded-md w-full bg-[#E6F0F0] focus:outline-none focus:border-none',
                    'placeholder': 'Describe about the event',
                    'type': 'text',
                    'placeholder': 'e.g. John Doe'
                }
            ),
            'participant_email': forms.EmailInput(
                attrs = {
                    'class': 'px-4 py-4 rounded-md w-full bg-[#E6F0F0] focus:outline-none focus:border-none',
                    'placeholder': 'Describe about the event',
                    'type': 'email',
                    'placeholder': 'e.g name@gmail.com'
                }
            )
        }