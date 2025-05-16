from flask import Blueprint, render_template, request, redirect, url_for
from .models import Movie, Review, Genre
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    genre_id = request.args.get('genre')
    genres = Genre.query.all()

    if genre_id:
        movies = Movie.query.join(Movie.genres).filter(Genre.id == genre_id).paginate(page=page, per_page=10)
    else:
        movies = Movie.query.paginate(page=page, per_page=50)

    return render_template('home.html', movies=movies, genres=genres)

@main.route('/search')
def search():
    query = request.args.get('query', '')
    if query:
        results = Movie.query.filter(Movie.title.ilike(f"%{query}%")).all()
    else:
        results = []
    return render_template('search_results.html', query=query, results=results)

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

    return {
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

@main.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    genres = Genre.query.all()

    if request.method == 'POST':
        title = request.form['title']
        release_date = request.form['release_date']
        popularity = float(request.form['popularity'])
        vote_average = float(request.form['vote_average'])
        vote_count = int(request.form['vote_count'])

        genre_ids = request.form.getlist('genres')
        selected_genres = Genre.query.filter(Genre.id.in_(genre_ids)).all()

        new_movie = Movie(
            title=title,
            release_date=release_date,
            popularity=popularity,
            vote_average=vote_average,
            vote_count=vote_count,
            genres=selected_genres
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template('add_movie.html', genres=genres)
