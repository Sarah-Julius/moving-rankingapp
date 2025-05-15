import os
import pandas as pd
from app import create_app
from app.models import db, Movie  # 🔍 Only import Movie, NOT Review

# Remove old DB file
if os.path.exists("movies.db"):
    os.remove("movies.db")
    print("🗑️ Deleted old database.")

# Create app and context
app = create_app()
app.app_context().push()

# Create tables
db.create_all()

# Load cleaned movie data
df = pd.read_csv('data/cleaned_movies.csv')

# Insert movie records
for _, row in df.iterrows():
    movie = Movie(
        id=row['id'],
        title=row['title'],
        release_date=row['release_date'],
        popularity=row['popularity'],
        vote_average=row['vote_average'],
        vote_count=row['vote_count']
    )
    db.session.add(movie)

db.session.commit()
print("✅ Inserted movies into database.")
