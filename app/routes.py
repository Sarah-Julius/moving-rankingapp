from flask import Blueprint, render_template, request, redirect, url_for
from .models import Movie, Review
from . import db  # SQLAlchemy instance

main = Blueprint('main', __name__)

@main.route('/')
def home():
    movies = Movie.query.limit(10).all()
    return render_template('home.html', movies=movies)

@main.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template('detail.html', movie=movie)

@main.route('/movie/<int:movie_id>/review', methods=['POST'])
def add_review(movie_id):
    reviewer_name = request.form['reviewer_name']
    rating = int(request.form['rating'])
    comment = request.form['comment']

    new_review = Review(movie_id=movie_id, reviewer_name=reviewer_name, rating=rating, comment=comment)
    db.session.add(new_review)
    db.session.commit()

    return redirect(url_for('main.movie_detail', movie_id=movie_id))

@main.route('/compare', methods=['GET', 'POST'])
def compare_movies():
    movies = Movie.query.order_by(Movie.title).all()

    if request.method == 'POST':
        movie1_id = int(request.form['movie1'])
        movie2_id = int(request.form['movie2'])
        movie1 = Movie.query.get(movie1_id)
        movie2 = Movie.query.get(movie2_id)
        return render_template('compare_result.html', movie1=movie1, movie2=movie2)

    return render_template('compare.html', movies=movies)

@main.route('/api/compare/<int:id1>/<int:id2>')
def compare_movies_json(id1, id2):
    movie1 = Movie.query.get_or_404(id1)
    movie2 = Movie.query.get_or_404(id2)

    data = {
        "movie1": {
            "title": movie1.title,
            "rating": movie1.vote_average,
            "votes": movie1.vote_count
        },
        "movie2": {
            "title": movie2.title,
            "rating": movie2.vote_average,
            "votes": movie2.vote_count
        }
    }
    return data  # Flask automatically returns JSON
