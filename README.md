# 🎬 Movie Rankings App

A Flask-based web application for movie search, comparison, and user reviews. Built as part of the CS551P Advanced Programming module.

---

## 🔍 Live Link

[https://moving-rankingapp.onrender.com](https://moving-rankingapp.onrender.com)

---

## 🔹 Features

* ✅ View paginated movie listings (\~7000 records loaded)
* ✅ Search movies by title with autocomplete
* ✅ Compare two movies by popularity, rating, and vote count
* ✅ Add user reviews linked to each movie
* ✅ Register and login with secure authentication
* ✅ Responsive UI using Bootstrap 5
* ✅ 404 and 500 error handling pages

---

## 💡 Tech Stack

* **Python 3.10**
* **Flask**, **Flask-Login**, **Flask-SQLAlchemy**, **Flask-Migrate**
* **Gunicorn** (for production server)
* **Bootstrap 5** (for UI)
* **SQLite** (local database)
* **Render.com** (for deployment)

---

## 📂 Project Structure

* `MOVIE-RANKINGS-APP/`

  * `app/`

    * `__init__.py`
    * `models.py`
    * `routes.py`
    * `auth.py`
    * `templates/`

      * `home.html`
      * `detail.html`
      * `compare.html`
      * `...`
    * `static/`
    * `movies.db`
  * `run.py`
  * `requirements.txt`
  * `render.yaml`
  * `runtime.txt`
  * `README.md`
  * `final_report.pdf`
  * `git-log.txt`

---

## 📃 How to Run Locally
# Clone repo
git clone https://github.com/yourusername/movie-rankings-app.git
cd movie-rankings-app

# Set up environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run app
flask run
Visit: `http://127.0.0.1:8000`

------

🔧 Maintenance

* Code is modularized using Flask Blueprints (auth.py, routes.py) for easy scalability.
* Database changes are managed using Flask-Migrate for safe updates.
* To reset or migrate the database:
- flask db init
- flask db migrate -m "Your message"
- flask db upgrade

* Config values (e.g. SECRET_KEY) can be updated in __init__.py or environment variables.


## 🔢 Testing

* Custom test cases using `pytest`
* Sample tests for models, routes, and form validation
* Coverage reports available locally
* Use Faker to generate realistic data for reviews and users
* To run tests locally:pytest
* ocal coverage reports can be generated with: pytest --cov=app
---


---

## 🔒 License

For academic submission only.
