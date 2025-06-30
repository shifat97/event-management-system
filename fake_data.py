# fake_data.py at project root
from events.models import Event, Category, Participant
from faker import Faker
import random

def generate_fake_data():
    fake = Faker()

    categories = []
    category_names = ["SPORTS", "FESTIVAL", "SEMINAR"]
    for name in category_names:
        category, _ = Category.objects.get_or_create(
            category_name=name,
            defaults={"category_description": fake.text()}
        )
        categories.append(category)

    events = []
    for _ in range(20):
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.paragraph(),
            date=fake.date_between(start_date="today", end_date="+30d"),
            time=fake.time(pattern="%H:%M"),
            location=fake.city(),
            category=random.choice(categories),
        )
        events.append(event)

    for _ in range(20):
        participant = Participant.objects.create(
            participant_name=fake.name(),
            participant_email=fake.email(),
        )
        participant.registered_event.set(random.sample(events, k=random.randint(1, 3)))

    print("✅ 20 fake events and participants created.")
