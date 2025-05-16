import os
import pandas as pd
import random
from faker import Faker
from app import create_app
from app.models import db, Movie, Review

faker = Faker()

# 🗑️ Delete old database
db_path = "app/movies.db"
if os.path.exists(db_path):
    os.remove(db_path)
    print("🗑️ Deleted old app/movies.db")

# 🚀 Create app context
app = create_app()
app.app_context().push()

# 📦 Create tables
db.create_all()

# 📊 Load and sample movie data
df = pd.read_csv('data/cleaned_movies.csv')
df = df.sample(n=7000, random_state=42).reset_index(drop=True)  # Random 7000 movies
print(f"🎬 Randomly selected {len(df)} movies from CSV.")

# 🎬 Insert movies and fake reviews
for _, row in df.iterrows():
    movie = Movie(
        title=row['title'],
        release_date=row['release_date'],
        popularity=round(random.uniform(0.0, 100.0), 2),       # realistic popularity
        vote_average=round(random.uniform(1.0, 10.0), 1),       # 1.0 to 10.0 rating
        vote_count=random.randint(10, 10000)                    # 10 to 10,000 votes
    )
    db.session.add(movie)
    db.session.flush()  # get movie.id before committing

    # Add 2–5 fake reviews
    for _ in range(random.randint(5, 25)):
        review = Review(
            movie_id=movie.id,
            reviewer_name=faker.first_name(),
            rating=random.randint(10, 20),
            comment=faker.sentence()
        )
        db.session.add(review)

db.session.commit()
print("✅ 7,000 random movies with realistic ratings and reviews inserted.")
