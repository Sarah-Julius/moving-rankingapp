from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Movie, Review, Genre
from flask_login import current_user
from flask_login import login_required
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    movies = Movie.query.paginate(page=page, per_page=10)
    return render_template('home.html', movies=movies)

@main.route('/autocomplete')
def autocomplete():
    query = request.args.get('q', '')
    results = []
    if query:
        results = Movie.query.filter(Movie.title.ilike(f'%{query}%')).limit(10).all()
    return jsonify([{"id": m.id, "title": m.title} for m in results])

# Search route with pagination
@main.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)

    if query:
        movies = Movie.query.filter(Movie.title.ilike(f"%{query}%")).paginate(page=page, per_page=50)
    else:
        movies = Movie.query.paginate(page=page, per_page=50)

    return render_template('search_results.html', query=query, movies=movies)



@main.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('main.home'))

    users = User.query.all()
    movies = Movie.query.order_by(Movie.id.desc()).limit(10).all()
    reviews = Review.query.order_by(Review.id.desc()).limit(10).all()

    return render_template('admin.html', users=users, movies=movies, reviews=reviews)

# Movie detail with review list
@main.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    reviews = Review.query.filter_by(movie_id=movie.id).order_by(Review.id.desc()).all()
    return render_template('detail.html', movie=movie, reviews=reviews)

# Submit a review
@main.route('/movie/<int:movie_id>/review', methods=['POST'])
def add_review(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    reviewer_name = request.form.get('reviewer_name')
    rating = request.form.get('rating')
    comment = request.form.get('comment')

    if not (reviewer_name and rating and comment):
        flash("All fields are required.", "danger")
        return redirect(url_for('main.movie_detail', movie_id=movie_id))

    new_review = Review(
        movie_id=movie_id,
        reviewer_name=reviewer_name,
        rating=int(rating),
        comment=comment
    )
    db.session.add(new_review)
    db.session.commit()

    flash("Review added successfully.", "success")
    return redirect(url_for('main.movie_detail', movie_id=movie_id))

# Compare movies via dropdown
@main.route('/compare', methods=['GET', 'POST'])
def compare_movies():
    movies = Movie.query.order_by(Movie.title).all()

    if request.method == 'POST':
        movie1_id = int(request.form['movie1'])
        movie2_id = int(request.form['movie2'])

        movie1 = Movie.query.get_or_404(movie1_id)
        movie2 = Movie.query.get_or_404(movie2_id)

        return render_template('compare_result.html', movie1=movie1, movie2=movie2)

    return render_template('compare.html', movies=movies)

# API endpoint for comparison (optional use)
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

# Add a movie manually
@main.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    genres = Genre.query.all()

    if request.method == 'POST':
        try:
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

            flash("Movie added successfully!", "success")
            return redirect(url_for('main.home'))

        except Exception as e:
            db.session.rollback()
            flash(f"Error adding movie: {str(e)}", "danger")

    return render_template('add_movie.html', genres=genres)




# Custom error pages
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
