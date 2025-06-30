# generate_fake_data.py

from events.models import Event, Category, Participant
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def generate_description(word_count=200):
    return " ".join(fake.paragraphs(nb=word_count // 5))

def create_categories():
    categories = {
        "TODAY": Category.objects.create(category_name="TODAY", category_description=fake.text(100)),
        "UPCOMING": Category.objects.create(category_name="UPCOMING", category_description=fake.text(100)),
        "PAST": Category.objects.create(category_name="PAST", category_description=fake.text(100)),
    }
    return categories

def create_events(categories, num_events=10):
    events = []
    for i in range(num_events):
        if i % 3 == 0:
            date = datetime.today().date()
            category = categories["TODAY"]
        elif i % 3 == 1:
            date = datetime.today().date() + timedelta(days=random.randint(1, 30))
            category = categories["UPCOMING"]
        else:
            date = datetime.today().date() - timedelta(days=random.randint(1, 30))
            category = categories["PAST"]

        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=generate_description(),
            date=date,
            time=fake.time(pattern="%I:%M %p"),  # 08:00 AM format
            location=fake.address(),
            category=category,
        )
        events.append(event)
    return events

def create_participants(events, num_participants=15):
    for _ in range(num_participants):
        participant = Participant.objects.create(
            participant_name=fake.name(),
            participant_email=fake.unique.email(),
        )
        # Each participant is registered in 1 to 3 events randomly
        selected_events = random.sample(events, random.randint(1, 3))
        participant.registered_event.add(*selected_events)

def run():
    print("Generating fake data...")
    Category.objects.all().delete()
    Event.objects.all().delete()
    Participant.objects.all().delete()

    categories = create_categories()
    events = create_events(categories)
    create_participants(events)
    print("Data generation complete.")