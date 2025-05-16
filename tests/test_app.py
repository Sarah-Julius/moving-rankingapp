import unittest
import sys
import os
import random
from faker import Faker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db, Movie, Genre, Review
from datetime import datetime, timedelta

faker = Faker()

class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Add genres
        self.genres = []
        for _ in range(3):
            genre = Genre(name=faker.word().capitalize())
            db.session.add(genre)
            self.genres.append(genre)
        db.session.commit()

        # Add a movie with genres
        self.fake_movie = Movie(
            id=1,
            title=faker.catch_phrase(),
            release_date=faker.date_between(start_date='-2y', end_date='today'),
            popularity=round(random.uniform(1.0, 10.0), 2),
            vote_average=round(random.uniform(1.0, 10.0), 1),
            vote_count=random.randint(10, 1000),
            genres=random.sample(self.genres, k=2)
        )
        db.session.add(self.fake_movie)
        db.session.commit()

        # Add a review with timestamp
        self.fake_review = Review(
            movie_id=self.fake_movie.id,
            reviewer_name=faker.first_name(),
            rating=random.randint(1, 10),
            comment=faker.sentence(),
            created_at=datetime.utcnow() - timedelta(days=1)
        )
        db.session.add(self.fake_review)
        db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movie Rankings', response.data)

    def test_404_page(self):
        response = self.client.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)

    def test_movie_detail_page(self):
        response = self.client.get(f'/movie/{self.fake_movie.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Submit a Review', response.data)
        self.assertIn(self.fake_review.reviewer_name.encode(), response.data)
        self.assertIn(self.fake_review.comment.encode(), response.data)

    def test_add_review(self):
        review_data = {
            'reviewer_name': faker.first_name(),
            'rating': random.randint(1, 10),
            'comment': faker.text(max_nb_chars=100)
        }
        response = self.client.post(
            f'/movie/{self.fake_movie.id}/review',
            data=review_data,
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(review_data['reviewer_name'].encode(), response.data)

    def test_add_movie(self):
        movie_data = {
            'title': faker.catch_phrase(),
            'release_date': '2022-01-01',
            'popularity': round(random.uniform(1.0, 10.0), 2),
            'vote_average': round(random.uniform(1.0, 10.0), 1),
            'vote_count': random.randint(1, 1000),
            'genres': [genre.id for genre in self.genres[:1]]
        }
        response = self.client.post('/add_movie', data=movie_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(movie_data['title'].encode(), response.data)

    def test_search_movies(self):
        response = self.client.get(f'/search?query={self.fake_movie.title}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.fake_movie.title.encode(), response.data)

    def test_api_compare_movies(self):
        response = self.client.get(f'/api/compare/{self.fake_movie.id}/{self.fake_movie.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['movie1']['title'], self.fake_movie.title)
        self.assertEqual(data['movie2']['title'], self.fake_movie.title)

    def test_compare_form_post(self):
        form_data = {
            'movie1': self.fake_movie.id,
            'movie2': self.fake_movie.id
        }
        response = self.client.post('/compare', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movie Comparison', response.data)

if __name__ == '__main__':
    unittest.main()
