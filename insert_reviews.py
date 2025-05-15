from app import create_app
from app.models import db, Review
from faker import Faker
import random

app = create_app()
app.app_context().push()

faker = Faker()

# Choose a list of movie IDs to attach reviews to
movie_ids = [862, 8844, 949, 11862, 15602]  # Or dynamically pull from DB

sample_reviews = []

for movie_id in movie_ids:
    for _ in range(random.randint(2, 5)):  # 2–5 reviews per movie
        review = Review(
            movie_id=movie_id,
            reviewer_name=faker.first_name(),  # ✅ Corrected field name
            comment=faker.sentence(nb_words=10),
            rating=round(random.uniform(4.0, 9.0), 1)
        )
        sample_reviews.append(review)

db.session.bulk_save_objects(sample_reviews)
db.session.commit()

print(f"✅ Inserted {len(sample_reviews)} fake reviews.")
