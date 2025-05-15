import pandas as pd

# Load the raw dataset
df = pd.read_csv('data/movies_metadata.csv', low_memory=False)

# Keep only needed columns
df = df[['id', 'title', 'release_date', 'popularity', 'vote_average', 'vote_count']]

# Remove rows with non-numeric IDs
df = df[df['id'].apply(lambda x: str(x).isdigit())]
df['id'] = df['id'].astype(int)

# Remove duplicates by movie ID
df = df.drop_duplicates(subset='id', keep='first')

# Drop missing values
df = df.dropna()

# Convert types
df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce')
df['vote_average'] = pd.to_numeric(df['vote_average'], errors='coerce')
df['vote_count'] = pd.to_numeric(df['vote_count'], errors='coerce')

# Drop NaNs again
df = df.dropna()

# Limit to 7000 rows (or less if needed)
df = df.head(7000)

# Save the cleaned CSV
df.to_csv('data/cleaned_movies.csv', index=False)
print("✅ Cleaned data saved. Final shape:", df.shape)
