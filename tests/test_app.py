import unittest

from app import create_app  # assuming you use create_app() in app/__init__.py

class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movie Rankings', response.data)  # update based on actual homepage content

    def test_404_page(self):
        response = self.app.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()

        def test_movie_detail_page(self):
        # Assuming movie with ID 1 exists from insert_movies.py
        response = self.app.get('/movie/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reviews', response.data)  # Adjust based on actual template content

    def test_add_review(self):
        # Simulate form submission for a new review
        review_data = {
            'reviewer_name': 'Test User',
            'rating': 4,
            'comment': 'This is a test review.'
        }
        response = self.app.post('/movie/1/review', data=review_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)
        self.assertIn(b'This is a test review.', response.data)

